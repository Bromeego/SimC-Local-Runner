#!/usr/bin/env sh
set -eu

SIMC_IMAGE="${SIMC_IMAGE:-simulationcraftorg/simc:latest}"
ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
OUTPUT_DIR="${ROOT_DIR}/smoke-output"

mkdir -p "${OUTPUT_DIR}"
rm -f "${OUTPUT_DIR}/smoke.html"

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
