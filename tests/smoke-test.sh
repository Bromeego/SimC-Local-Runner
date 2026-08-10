#!/usr/bin/env sh
set -eu

SIMC_IMAGE="${SIMC_IMAGE:-simulationcraftorg/simc:latest}"
ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OUTPUT_DIR="${ROOT_DIR}/smoke-output"
PULL_ATTEMPTS="${PULL_ATTEMPTS:-5}"
PULL_SLEEP_SECONDS="${PULL_SLEEP_SECONDS:-10}"

mkdir -p "${OUTPUT_DIR}"
rm -f "${OUTPUT_DIR}/smoke.html"

attempt=1
while :; do
  if docker pull "${SIMC_IMAGE}"; then
    break
  fi

  if [ "${attempt}" -ge "${PULL_ATTEMPTS}" ]; then
    echo "Failed to pull ${SIMC_IMAGE} after ${PULL_ATTEMPTS} attempts." >&2
    exit 1
  fi

  echo "docker pull failed (attempt ${attempt}/${PULL_ATTEMPTS}); retrying in ${PULL_SLEEP_SECONDS}s..." >&2
  attempt=$((attempt + 1))
  sleep "${PULL_SLEEP_SECONDS}"
done

docker run --rm \
  --volume "${ROOT_DIR}/examples:/input:ro" \
  --volume "${OUTPUT_DIR}:/output" \
  "${SIMC_IMAGE}" \
  /input/demo.simc \
  iterations=5 \
  max_time=10 \
  vary_combat_length=0 \
  html=/output/smoke.html

test -s "${OUTPUT_DIR}/smoke.html"
grep -q "SimulationCraft" "${OUTPUT_DIR}/smoke.html"
echo "SimulationCraft smoke report created successfully."
