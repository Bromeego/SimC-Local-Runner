import os
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from threading import BoundedSemaphore
from types import SimpleNamespace
from unittest.mock import patch


APP_DIR = Path(__file__).resolve().parents[1] / "app"
sys.path.insert(0, str(APP_DIR))

import app as simc_app


class SimcWebTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        simc_app.INPUT_DIR = root / "input"
        simc_app.OUTPUT_DIR = root / "output"
        simc_app.HOST_INPUT_DIR = str(simc_app.INPUT_DIR)
        simc_app.HOST_OUTPUT_DIR = str(simc_app.OUTPUT_DIR)
        simc_app.REPORT_RETENTION_COUNT = 100
        simc_app.SIMULATION_SLOTS = BoundedSemaphore(1)
        simc_app.app.config.update(TESTING=True, MAX_CONTENT_LENGTH=2 * 1024 * 1024)
        self.client = simc_app.app.test_client()

    def tearDown(self):
        self.temp_dir.cleanup()

    def post_profile(self, **overrides):
        data = {
            "report_name": "test-run",
            "fight_style": "patchwerk",
            "iterations": "1000",
            "desired_targets": "1",
            "max_time": "300",
            "simc_text": "mage=example",
        }
        data.update(overrides)
        return self.client.post("/run", data=data)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"status": "ok"})

    def test_invalid_pull_policy_falls_back_to_always(self):
        with patch.dict(os.environ, {"TEST_PULL_POLICY": "sometimes"}):
            policy = simc_app.env_choice(
                "TEST_PULL_POLICY",
                "always",
                {"always", "missing", "never"},
            )
        self.assertEqual(policy, "always")

    def test_data_mount_args_discovers_named_volumes(self):
        details = [
            {
                "Mounts": [
                    {
                        "Type": "volume",
                        "Name": "simc-input",
                        "Source": "/var/lib/docker/volumes/simc-input/_data",
                        "Destination": "/data/input",
                    },
                    {
                        "Type": "volume",
                        "Name": "simc-output",
                        "Source": "/var/lib/docker/volumes/simc-output/_data",
                        "Destination": "/data/output",
                    },
                ]
            }
        ]
        completed = SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=json.dumps(details),
        )

        with (
            patch.object(simc_app, "HOST_INPUT_DIR", ""),
            patch.object(simc_app, "HOST_OUTPUT_DIR", ""),
            patch.dict(os.environ, {"HOSTNAME": "controller-id"}, clear=False),
            patch.object(simc_app.subprocess, "run", return_value=completed) as run,
        ):
            args = simc_app.data_mount_args()

        run.assert_called_once_with(
            ["docker", "inspect", "controller-id"],
            capture_output=True,
            text=True,
            timeout=10,
        )
        self.assertEqual(
            args,
            [
                "--mount",
                "type=volume,source=simc-input,target=/input,readonly",
                "--mount",
                "type=volume,source=simc-output,target=/output",
            ],
        )

    def test_data_mount_args_discovers_bind_mounts(self):
        details = [
            {
                "Mounts": [
                    {
                        "Type": "bind",
                        "Source": "/srv/simc-web/input",
                        "Destination": "/data/input",
                    },
                    {
                        "Type": "bind",
                        "Source": "/srv/simc-web/output",
                        "Destination": "/data/output",
                    },
                ]
            }
        ]
        completed = SimpleNamespace(
            returncode=0,
            stderr="",
            stdout=json.dumps(details),
        )

        with (
            patch.object(simc_app, "HOST_INPUT_DIR", ""),
            patch.object(simc_app, "HOST_OUTPUT_DIR", ""),
            patch.dict(os.environ, {"HOSTNAME": "controller-id"}, clear=False),
            patch.object(simc_app.subprocess, "run", return_value=completed),
        ):
            args = simc_app.data_mount_args()

        self.assertEqual(
            args,
            [
                "--mount",
                "type=bind,source=/srv/simc-web/input,target=/input,readonly",
                "--mount",
                "type=bind,source=/srv/simc-web/output,target=/output",
            ],
        )

    def test_favicon_is_served(self):
        response = self.client.get("/static/favicon.svg")
        try:
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.mimetype, "image/svg+xml")
            self.assertIn(b">SC</text>", response.data)
        finally:
            response.close()

    def test_index_renders_empty_and_loading_states(self):
        response = self.client.get("/")
        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("No reports yet", page)
        self.assertIn("Simulation running", page)
        self.assertIn("Drop a .simc file here", page)
        self.assertIn("raid-single-target", page)
        self.assertIn("SimC Nightly", page)
        self.assertIn("Version pending", page)
        self.assertIn("Docker checks for a newer nightly before every simulation.", page)
        self.assertIn('rel="icon" href="/static/favicon.svg"', page)
        self.assertNotIn("—", page)
        self.assertNotIn("–", page)

    def test_extract_simc_build_from_report_html(self):
        report_html = """
            <p>
              <a href="https://www.simulationcraft.org/">SimulationCraft 1205-01</a>
              for World of Warcraft 12.0.7.68453 Live
              (hotfix 2026-07-13/68453, git build
              <a href="https://github.com/simulationcraft/simc/commit/30e0b5f">30e0b5f</a>)
            </p>
        """

        build = simc_app.extract_simc_build(report_html)

        self.assertEqual(build["version"], "1205-01")
        self.assertEqual(build["wow_version"], "12.0.7.68453")
        self.assertEqual(build["wow_channel"], "Live")
        self.assertEqual(build["hotfix_date"], "2026-07-13")
        self.assertEqual(build["hotfix_build"], "68453")
        self.assertEqual(build["git_commit"], "30e0b5f")

    def test_extract_simc_build_from_labeled_console_output(self):
        build = simc_app.extract_simc_build(
            "SimulationCraft 1205-01 for World of Warcraft 12.0.7.68453 "
            "Live (hotfix 2026-07-13/68453, git build midnight 79cea9e)"
        )

        self.assertEqual(build["git_commit"], "79cea9e")

    def test_index_shows_latest_report_build_in_engine_badge(self):
        simc_app.ensure_data_dirs()
        report = simc_app.OUTPUT_DIR / "raid-test.html"
        report.write_text(
            "x" * (600 * 1024)
            + """
            <p>
              <a>SimulationCraft 1205-01</a> for World of Warcraft
              12.0.7.68453 Live (hotfix 2026-07-13/68453,
              git build <a>30e0b5f</a>)
            </p>
            """
        )
        simc_app.metadata_path(report.name).write_text(
            json.dumps(
                {
                    "simc_image": "simulationcraftorg/simc:latest",
                    "simc_image_resolved": (
                        "simulationcraftorg/simc@sha256:"
                        "1234567890abcdef1234567890abcdef"
                    ),
                }
            )
        )

        response = self.client.get("/")
        page = response.get_data(as_text=True)

        self.assertEqual(response.status_code, 200)
        self.assertIn("SimC Nightly", page)
        self.assertIn("1205-01", page)
        self.assertIn("12.0.7.68453 Live", page)
        self.assertIn("2026-07-13, build 68453", page)
        self.assertIn("View 30e0b5f", page)
        self.assertIn("Nightly image", page)
        self.assertIn("simulationcraftorg/simc:latest", page)
        self.assertIn(
            "https://github.com/simulationcraft/simc/commit/30e0b5f",
            page,
        )
        self.assertIn("Copy digest", page)

    def test_safe_name_and_unique_filenames(self):
        self.assertEqual(simc_app.safe_name(" My Report !! "), "my-report")
        first = simc_app.build_names("My Report")
        second = simc_app.build_names("My Report")
        self.assertNotEqual(first, second)
        self.assertTrue(first[0].endswith(".simc"))
        self.assertTrue(first[1].endswith(".html"))

    def test_web_settings_replace_profile_values(self):
        profile = "iterations=1\nmax_time=20\ndesired_targets=9\nmage=example"
        result = simc_app.apply_web_settings(profile, "patchwerk", 1000, 3, 180)
        self.assertEqual(result.count("iterations="), 1)
        self.assertIn("iterations=1000", result)
        self.assertIn("desired_targets=3", result)
        self.assertIn("max_time=180", result)

    def test_dungeon_slice_omits_time_and_targets(self):
        result = simc_app.apply_web_settings(
            "max_time=20\ndesired_targets=9\nmage=example",
            "dungeonslice",
            1000,
            3,
            180,
        )
        self.assertNotIn("desired_targets=", result)
        self.assertNotIn("max_time=", result)
        self.assertIn("fight_style=DungeonSlice", result)

    def test_subprocess_errors_are_html_escaped(self):
        failed = SimpleNamespace(
            returncode=1,
            stderr="<script>alert('nope')</script>",
            stdout="",
        )
        with patch.object(simc_app.subprocess, "run", return_value=failed):
            response = self.post_profile()

        page = response.get_data(as_text=True)
        self.assertEqual(response.status_code, 500)
        self.assertNotIn("<script>alert('nope')</script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_timeout_returns_504_and_releases_slot(self):
        timeout = subprocess.TimeoutExpired("docker", simc_app.SIMC_TIMEOUT_SECONDS)
        with patch.object(simc_app.subprocess, "run", side_effect=timeout):
            response = self.post_profile()

        self.assertEqual(response.status_code, 504)
        acquired = simc_app.SIMULATION_SLOTS.acquire(blocking=False)
        self.assertTrue(acquired)
        if acquired:
            simc_app.SIMULATION_SLOTS.release()

    def test_pull_policy_and_optional_docker_resource_limits_are_applied(self):
        original_cpus = simc_app.SIMC_CPUS
        original_memory = simc_app.SIMC_MEMORY
        simc_app.SIMC_CPUS = "3"
        simc_app.SIMC_MEMORY = "2g"

        def complete_run(command, **_kwargs):
            if command[1:3] == ["image", "inspect"]:
                return SimpleNamespace(returncode=0, stderr="", stdout="[]")
            self.assertIn("--pull=always", command)
            self.assertIn("--cpus", command)
            self.assertIn("3", command)
            self.assertIn("--memory", command)
            self.assertIn("2g", command)
            self.assertIn("--name", command)
            self.assertIn("--mount", command)
            self.assertIn("target=/input,readonly", " ".join(command))
            output_name = Path(command[-1].split("=", 1)[1]).name
            simc_app.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            (simc_app.OUTPUT_DIR / output_name).write_text(
                """
                <p>SimulationCraft 1205-01 for World of Warcraft
                12.0.7.68453 Live (hotfix 2026-07-13/68453,
                git build 30e0b5f)</p>
                """
            )
            return SimpleNamespace(returncode=0, stderr="", stdout="")

        try:
            with patch.object(simc_app.subprocess, "run", side_effect=complete_run):
                response = self.post_profile()
        finally:
            simc_app.SIMC_CPUS = original_cpus
            simc_app.SIMC_MEMORY = original_memory

        self.assertEqual(response.status_code, 302)

    def test_success_redirects_to_created_report(self):
        def complete_run(command, **_kwargs):
            if command[1:3] == ["image", "inspect"]:
                return SimpleNamespace(
                    returncode=0,
                    stderr="",
                    stdout='["simulationcraftorg/simc@sha256:abc123"]',
                )
            output_name = Path(command[-1].split("=", 1)[1]).name
            simc_app.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            (simc_app.OUTPUT_DIR / output_name).write_text(
                """
                <p>SimulationCraft 1205-01 for World of Warcraft
                12.0.7.68453 Live (hotfix 2026-07-13/68453,
                git build 30e0b5f)</p>
                """
            )
            return SimpleNamespace(
                returncode=0,
                stderr="",
                stdout="SimulationCraft 1200-01 test build",
            )

        with patch.object(simc_app.subprocess, "run", side_effect=complete_run):
            response = self.post_profile()

        self.assertEqual(response.status_code, 302)
        self.assertIn("/reports/test-run-", response.headers["Location"])
        self.assertEqual(len(list(simc_app.INPUT_DIR.glob("*.simc"))), 1)
        self.assertEqual(len(list(simc_app.OUTPUT_DIR.glob("*.html"))), 1)
        metadata_files = list(simc_app.OUTPUT_DIR.glob("*.json"))
        self.assertEqual(len(metadata_files), 1)
        metadata = json.loads(metadata_files[0].read_text())
        self.assertEqual(metadata["settings"]["fight_style"], "Patchwerk")
        self.assertEqual(metadata["settings"]["iterations"], 1000)
        self.assertEqual(metadata["simc_pull_policy"], "always")
        self.assertEqual(metadata["simc_version"], "SimulationCraft 1200-01 test build")
        self.assertEqual(metadata["schema_version"], 2)
        self.assertEqual(metadata["simc_build"]["version"], "1205-01")
        self.assertEqual(metadata["simc_build"]["wow_version"], "12.0.7.68453")
        self.assertEqual(metadata["simc_build"]["git_commit"], "30e0b5f")
        self.assertEqual(
            metadata["simc_image_resolved"],
            "simulationcraftorg/simc@sha256:abc123",
        )

    def test_retention_deletes_oldest_report_and_matching_input(self):
        simc_app.ensure_data_dirs()
        simc_app.REPORT_RETENTION_COUNT = 2

        for index in range(3):
            report = simc_app.OUTPUT_DIR / f"run-{index}.html"
            profile = simc_app.INPUT_DIR / f"run-{index}.simc"
            metadata = simc_app.OUTPUT_DIR / f"run-{index}.json"
            report.write_text("report")
            profile.write_text("profile")
            metadata.write_text("{}")
            os.utime(report, (index + 1, index + 1))

        simc_app.prune_old_reports()

        self.assertFalse((simc_app.OUTPUT_DIR / "run-0.html").exists())
        self.assertFalse((simc_app.INPUT_DIR / "run-0.simc").exists())
        self.assertFalse((simc_app.OUTPUT_DIR / "run-0.json").exists())
        self.assertEqual(len(list(simc_app.OUTPUT_DIR.glob("*.html"))), 2)

    def test_delete_route_removes_report_and_input(self):
        simc_app.ensure_data_dirs()
        (simc_app.OUTPUT_DIR / "saved.html").write_text("report")
        (simc_app.INPUT_DIR / "saved.simc").write_text("profile")
        (simc_app.OUTPUT_DIR / "saved.json").write_text("{}")

        response = self.client.post("/reports/saved.html/delete")

        self.assertEqual(response.status_code, 302)
        self.assertFalse((simc_app.OUTPUT_DIR / "saved.html").exists())
        self.assertFalse((simc_app.INPUT_DIR / "saved.simc").exists())
        self.assertFalse((simc_app.OUTPUT_DIR / "saved.json").exists())

    def test_report_details_include_saved_run_summary(self):
        simc_app.ensure_data_dirs()
        report = simc_app.OUTPUT_DIR / "raid-test.html"
        report.write_text("report")
        simc_app.metadata_path(report.name).write_text(
            json.dumps(
                {
                    "duration_seconds": 12.34,
                    "simc_image_resolved": "simc@example",
                    "settings": {
                        "fight_style": "Patchwerk",
                        "iterations": 10000,
                    },
                }
            )
        )

        details = simc_app.report_details(report)

        self.assertEqual(details["summary"], "Patchwerk / 10,000 iterations / 12.3s")
        self.assertEqual(details["image"], "simc@example")

    def test_large_request_uses_friendly_error_page(self):
        simc_app.app.config["MAX_CONTENT_LENGTH"] = 128
        response = self.post_profile(simc_text="x" * 1024)
        self.assertEqual(response.status_code, 413)
        self.assertIn("Profile is too large", response.get_data(as_text=True))


if __name__ == "__main__":
    unittest.main()
