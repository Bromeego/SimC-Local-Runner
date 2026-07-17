import json
import os
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from threading import BoundedSemaphore
from uuid import uuid4

from flask import (
    Flask,
    abort,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from werkzeug.exceptions import HTTPException, RequestEntityTooLarge
from werkzeug.utils import secure_filename


def env_int(name: str, default: int, minimum: int = 1) -> int:
    try:
        value = int(os.environ.get(name, str(default)))
    except ValueError:
        return default
    return max(value, minimum)


def env_choice(name: str, default: str, choices: set[str]) -> str:
    value = os.environ.get(name, default).strip().lower()
    return value if value in choices else default


app = Flask(__name__)

INPUT_DIR = Path(os.environ.get("INPUT_DIR", "/data/input"))
OUTPUT_DIR = Path(os.environ.get("OUTPUT_DIR", "/data/output"))

HOST_INPUT_DIR = os.environ.get("HOST_INPUT_DIR", "/srv/simc-web/input")
HOST_OUTPUT_DIR = os.environ.get("HOST_OUTPUT_DIR", "/srv/simc-web/output")

SIMC_IMAGE = os.environ.get("SIMC_IMAGE", "simulationcraftorg/simc:latest")
SIMC_PULL_POLICY = env_choice(
    "SIMC_PULL_POLICY",
    "always",
    {"always", "missing", "never"},
)
SIMC_CPUS = os.environ.get("SIMC_CPUS", "").strip()
SIMC_MEMORY = os.environ.get("SIMC_MEMORY", "").strip()
SIMC_TIMEOUT_SECONDS = env_int("SIMC_TIMEOUT_SECONDS", 1800, 30)
MAX_UPLOAD_MB = env_int("MAX_UPLOAD_MB", 2)
MAX_CONCURRENT_SIMS = env_int("MAX_CONCURRENT_SIMS", 1)
REPORT_RETENTION_COUNT = env_int("REPORT_RETENTION_COUNT", 100)

app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_MB * 1024 * 1024
SIMULATION_SLOTS = BoundedSemaphore(MAX_CONCURRENT_SIMS)

ALLOWED_EXTENSIONS = {".simc", ".txt"}
FIGHT_STYLES = {
    "patchwerk": "Patchwerk",
    "hecticaddcleave": "HecticAddCleave",
    "dungeonslice": "DungeonSlice",
}


def ensure_data_dirs() -> None:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def safe_name(value: str) -> str:
    value = (value or "").strip().lower()
    value = re.sub(r"[^a-z0-9._-]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value[:80]


def allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def build_names(
    report_name: str, upload_filename: str | None = None
) -> tuple[str, str]:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_id = uuid4().hex[:8]

    base_name = safe_name(report_name)
    if not base_name and upload_filename:
        base_name = safe_name(Path(upload_filename).stem)

    if not base_name:
        base_name = "sim"

    input_name = f"{base_name}-{timestamp}-{run_id}.simc"
    output_name = f"{base_name}-{timestamp}-{run_id}.html"
    return input_name, output_name


def strip_existing_setting(profile_text: str, key: str) -> str:
    pattern = rf"(?im)^\s*{re.escape(key)}\s*=.*(?:\n|$)"
    return re.sub(pattern, "", profile_text)


def apply_web_settings(
    profile_text: str,
    fight_style_key: str,
    iterations: int,
    desired_targets: int,
    max_time: int,
) -> str:
    fight_style = FIGHT_STYLES.get(fight_style_key, "Patchwerk")

    for key in ("fight_style", "iterations", "desired_targets", "max_time"):
        profile_text = strip_existing_setting(profile_text, key)

    extra_lines = [
        "",
        "# Added by simc-web",
        f"fight_style={fight_style}",
        f"iterations={iterations}",
    ]

    if fight_style != "DungeonSlice":
        extra_lines.append(f"desired_targets={desired_targets}")
        extra_lines.append(f"max_time={max_time}")

    return profile_text.rstrip() + "\n" + "\n".join(extra_lines) + "\n"


def format_bytes(size: int) -> str:
    if size < 1024:
        return f"{size} B"
    if size < 1024 * 1024:
        return f"{size / 1024:.1f} KB"
    return f"{size / (1024 * 1024):.1f} MB"


def metadata_path(filename: str) -> Path:
    return OUTPUT_DIR / f"{Path(filename).stem}.json"


def load_run_metadata(filename: str) -> dict:
    try:
        data = json.loads(metadata_path(filename).read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError):
        return {}
    return data if isinstance(data, dict) else {}


def display_run_summary(metadata: dict) -> str:
    settings = metadata.get("settings")
    if not isinstance(settings, dict):
        return ""

    parts = []
    fight_style = settings.get("fight_style")
    if fight_style:
        parts.append(str(fight_style))

    iterations = settings.get("iterations")
    if isinstance(iterations, int):
        parts.append(f"{iterations:,} iterations")

    duration = metadata.get("duration_seconds")
    if isinstance(duration, (int, float)):
        parts.append(f"{duration:.1f}s")

    return " / ".join(parts)


def report_details(path: Path) -> dict[str, str]:
    stat = path.stat()
    created = datetime.fromtimestamp(stat.st_mtime)
    metadata = load_run_metadata(path.name)
    label = re.sub(
        r"-\d{8}-\d{6}(?:-\d{6})?(?:-[a-f0-9]{8})?$",
        "",
        path.stem,
    )
    return {
        "filename": path.name,
        "label": label or "simulation",
        "created": created.strftime("%d %b %Y, %H:%M"),
        "size": format_bytes(stat.st_size),
        "summary": display_run_summary(metadata),
        "image": str(
            metadata.get("simc_image_resolved")
            or metadata.get("simc_image")
            or ""
        ),
    }


def list_reports() -> list[dict[str, str]]:
    ensure_data_dirs()
    paths = sorted(
        OUTPUT_DIR.glob("*.html"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    return [report_details(path) for path in paths]


def report_path(filename: str) -> Path:
    if Path(filename).name != filename or Path(filename).suffix.lower() != ".html":
        abort(404, "Report not found.")
    return OUTPUT_DIR / filename


def delete_run_files(filename: str) -> None:
    output_path = report_path(filename)
    output_path.unlink(missing_ok=True)
    (INPUT_DIR / f"{output_path.stem}.simc").unlink(missing_ok=True)
    metadata_path(filename).unlink(missing_ok=True)


def prune_old_reports() -> None:
    ensure_data_dirs()
    reports = sorted(
        OUTPUT_DIR.glob("*.html"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for stale_report in reports[REPORT_RETENTION_COUNT:]:
        delete_run_files(stale_report.name)


def stop_run_container(container_name: str) -> None:
    try:
        subprocess.run(
            ["docker", "rm", "--force", container_name],
            capture_output=True,
            text=True,
            timeout=15,
        )
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass


def resolve_simc_image() -> str:
    """Return an immutable image digest when Docker has one available."""
    try:
        result = subprocess.run(
            [
                "docker",
                "image",
                "inspect",
                "--format",
                "{{json .RepoDigests}}",
                SIMC_IMAGE,
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )
        if result.returncode == 0:
            digests = json.loads(result.stdout.strip() or "[]")
            if isinstance(digests, list) and digests:
                return str(digests[0])
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError, TypeError):
        pass
    return SIMC_IMAGE


def detect_simc_version(output: str) -> str:
    match = re.search(r"(?im)^\s*(SimulationCraft[^\r\n]*)", output or "")
    return match.group(1).strip() if match else ""


def save_run_metadata(
    output_name: str,
    input_name: str,
    fight_style_key: str,
    iterations: int,
    desired_targets: int,
    max_time: int,
    duration_seconds: float,
    process_output: str,
) -> None:
    fight_style = FIGHT_STYLES[fight_style_key]
    settings = {
        "fight_style": fight_style,
        "iterations": iterations,
    }
    if fight_style != "DungeonSlice":
        settings.update(
            {
                "desired_targets": desired_targets,
                "max_time_seconds": max_time,
            }
        )

    metadata = {
        "schema_version": 1,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "duration_seconds": round(duration_seconds, 3),
        "input_file": input_name,
        "report_file": output_name,
        "simc_image": SIMC_IMAGE,
        "simc_pull_policy": SIMC_PULL_POLICY,
        "simc_image_resolved": resolve_simc_image(),
        "simc_version": detect_simc_version(process_output),
        "settings": settings,
    }

    try:
        metadata_path(output_name).write_text(
            json.dumps(metadata, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    except OSError:
        # Metadata is useful for reproducibility, but should never discard a
        # successfully generated SimulationCraft report.
        pass


def render_error(
    status_code: int,
    title: str,
    message: str,
    details: str = "",
):
    if isinstance(details, bytes):
        details = details.decode("utf-8", errors="replace")
    return (
        render_template(
            "error.html",
            status_code=status_code,
            title=title,
            message=message,
            details=details[-8000:],
        ),
        status_code,
    )


@app.get("/")
def index():
    reports = list_reports()
    return render_template(
        "index.html",
        reports=reports,
        report_count=len(reports),
        retention_count=REPORT_RETENTION_COUNT,
        timeout_minutes=max(1, round(SIMC_TIMEOUT_SECONDS / 60)),
        max_upload_mb=MAX_UPLOAD_MB,
        deleted=request.args.get("deleted") == "1",
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run")
def run_sim():
    simc_text = (request.form.get("simc_text") or "").strip()
    report_name = request.form.get("report_name", "")
    simc_file = request.files.get("simc_file")

    fight_style_key = (
        request.form.get("fight_style") or "patchwerk"
    ).strip().lower()
    if fight_style_key not in FIGHT_STYLES:
        abort(400, "Invalid fight style selected.")

    try:
        iterations = int(request.form.get("iterations", "10000"))
        desired_targets = int(request.form.get("desired_targets", "1"))
        max_time = int(request.form.get("max_time", "300"))
    except ValueError:
        abort(400, "Iterations, desired targets, and max time must be numbers.")

    if iterations < 100 or iterations > 50000:
        abort(400, "Iterations must be between 100 and 50000.")
    if desired_targets < 1 or desired_targets > 20:
        abort(400, "Desired targets must be between 1 and 20.")
    if max_time < 30 or max_time > 1800:
        abort(400, "Max time must be between 30 and 1800 seconds.")

    uploaded_filename = None
    file_text = ""

    if simc_file and simc_file.filename:
        uploaded_filename = secure_filename(simc_file.filename)
        if not allowed_file(uploaded_filename):
            abort(400, "Invalid file type. Upload a .simc or .txt file.")
        file_text = simc_file.read().decode("utf-8", errors="replace").strip()

    final_text = file_text or simc_text
    if not final_text:
        abort(400, "Upload a profile or paste SimulationCraft profile text.")

    final_text = apply_web_settings(
        profile_text=final_text,
        fight_style_key=fight_style_key,
        iterations=iterations,
        desired_targets=desired_targets,
        max_time=max_time,
    )

    if not SIMULATION_SLOTS.acquire(blocking=False):
        abort(429, "A simulation is already running. Try again when it finishes.")

    try:
        ensure_data_dirs()
        input_name, output_name = build_names(report_name, uploaded_filename)
        input_path = INPUT_DIR / input_name
        input_path.write_text(final_text, encoding="utf-8")
        run_id = Path(output_name).stem.rsplit("-", 1)[-1]
        container_name = f"simc-web-run-{run_id}"

        cmd = [
            "docker",
            "run",
            f"--pull={SIMC_PULL_POLICY}",
            "--rm",
            "--name",
            container_name,
            "-v",
            f"{HOST_INPUT_DIR}:/input",
            "-v",
            f"{HOST_OUTPUT_DIR}:/output",
        ]
        if SIMC_CPUS:
            cmd.extend(["--cpus", SIMC_CPUS])
        if SIMC_MEMORY:
            cmd.extend(["--memory", SIMC_MEMORY])
        cmd.extend(
            [
                SIMC_IMAGE,
                f"/input/{input_name}",
                f"html=/output/{output_name}",
            ]
        )

        started_at = time.monotonic()
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=SIMC_TIMEOUT_SECONDS,
            )
        except subprocess.TimeoutExpired as error:
            stop_run_container(container_name)
            details = error.stderr or error.stdout or ""
            return render_error(
                504,
                "Simulation timed out",
                f"The run exceeded the {SIMC_TIMEOUT_SECONDS}-second limit.",
                details,
            )
        except FileNotFoundError:
            return render_error(
                503,
                "Docker is unavailable",
                "The web container could not start the Docker client.",
                "Confirm that Docker is installed and the Docker socket is mounted.",
            )
        duration_seconds = time.monotonic() - started_at
    finally:
        SIMULATION_SLOTS.release()

    if result.returncode != 0:
        return render_error(
            500,
            "Simulation failed",
            "SimulationCraft stopped before producing a report.",
            result.stderr or result.stdout or "No error output was returned.",
        )

    if not (OUTPUT_DIR / output_name).is_file():
        return render_error(
            500,
            "Report was not created",
            "SimulationCraft finished without writing the expected HTML report.",
        )

    save_run_metadata(
        output_name=output_name,
        input_name=input_name,
        fight_style_key=fight_style_key,
        iterations=iterations,
        desired_targets=desired_targets,
        max_time=max_time,
        duration_seconds=duration_seconds,
        process_output="\n".join(filter(None, (result.stdout, result.stderr))),
    )
    prune_old_reports()
    return redirect(url_for("serve_report", filename=output_name))


@app.get("/reports/<path:filename>")
def serve_report(filename):
    report = report_path(filename)
    if not report.is_file():
        abort(404, "Report not found.")
    return send_from_directory(OUTPUT_DIR, report.name)


@app.post("/reports/<path:filename>/delete")
def delete_report(filename):
    report = report_path(filename)
    if not report.is_file():
        abort(404, "Report not found.")
    delete_run_files(report.name)
    return redirect(url_for("index", deleted="1"))


@app.errorhandler(RequestEntityTooLarge)
def handle_large_upload(_error):
    return render_error(
        413,
        "Profile is too large",
        f"Uploads are limited to {MAX_UPLOAD_MB} MB.",
    )


@app.errorhandler(HTTPException)
def handle_http_error(error):
    titles = {
        400: "Check the profile settings",
        404: "Nothing here",
        429: "Runner is busy",
    }
    return render_error(
        error.code or 500,
        titles.get(error.code, error.name),
        str(error.description),
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
