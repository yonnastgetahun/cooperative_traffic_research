#!/bin/sh
# M1/M2 measurement-only runner. Never changes original route policy or parameters.
set -eu
: "${WINDOW:?200/600/1200 required}"
: "${SEED:?development seed required}"
case "$WINDOW" in 200|600|1200);; *) echo "Invalid window" >&2;exit 2;; esac
case "$SEED" in 2001|2101|2102|2103);; *) echo "Holdout/prohibited seed" >&2;exit 2;; esac
mkdir -p results
sumo --version > results/sumo-version.txt
echo "${GITHUB_SHA:-local-development}" > results/repository-commit.txt
printf "%s\n" "${SUMO_IMAGE_REF:-ghcr.io/eclipse-sumo/sumo:latest (M1 development only)}" > results/container-image.txt
netgenerate --grid --grid.number 10 --grid.length 200 --output-file results/network.net.xml
python3 experiments/experiment_002/fixed_demand_v01.py \
  --net results/network.net.xml --out results/trips.xml \
  --manifest results/scenario.json --seed "$SEED" --window "$WINDOW"
sha256sum results/network.net.xml results/trips.xml > results/input-hashes.txt

# Traced and original policies MUST produce exactly the same route and audit bytes.
python3 experiments/experiment_002/trace_actual_predictor.py \
  --net results/network.net.xml --trips results/trips.xml \
  --out results/trace.rou.xml --audit results/trace-audit.csv \
  --manifest results/trace-manifest.json \
  --trace results/chosen-decision-trace.csv \
  --candidate-trace results/candidate-decision-trace.csv \
  --decision-trace results/route-decisions.csv
python3 experiments/experiment_002/time_aware.py \
  --net results/network.net.xml --trips results/trips.xml \
  --out results/original.rou.xml --audit results/original-audit.csv \
  --manifest results/original-manifest.json
cmp results/trace.rou.xml results/original.rou.xml
cmp results/trace-audit.csv results/original-audit.csv
printf 'Exact route and audit equality against original time_aware.py.\n' > results/policy-invariance.txt
sha256sum results/trace.rou.xml results/chosen-decision-trace.csv \
  results/route-decisions.csv > results/forecast-hashes.txt

cat > results/measurement.add.xml <<'XML'
<additional>
  <edgeData id="external" file="native-external.xml" period="30" excludeEmpty="false" withInternal="false"/>
  <edgeData id="includingInternal" file="native-with-internal.xml" period="30" excludeEmpty="false" withInternal="true"/>
</additional>
XML

# Separate independent measurements; do not modify selected routes.
sumo -n results/network.net.xml -r results/trace.rou.xml \
  --additional-files results/measurement.add.xml \
  --fcd-output results/observed-fcd.xml \
  --device.fcd.period 1 \
  --fcd-output.attributes lane,speed,pos \
  --tripinfo-output results/observed-tripinfo.xml \
  --seed "$SEED" --no-step-log true

python3 experiments/experiment_002/compare_traced_predictor.py \
  --trace results/chosen-decision-trace.csv \
  --decision-trace results/route-decisions.csv \
  --fcd results/observed-fcd.xml \
  --tripinfo results/observed-tripinfo.xml \
  --report results/actual-predictor-report.json \
  --comparison results/vehicle-edge-errors.csv \
  --occupancy-comparison results/previous-occupancy-proxy.csv

python3 experiments/experiment_002/measurement_v01.py \
  --fcd results/observed-fcd.xml \
  --native-external results/native-external.xml \
  --native-internal results/native-with-internal.xml \
  --trace results/chosen-decision-trace.csv \
  --tripinfo results/observed-tripinfo.xml \
  --report results/measurement-report.json \
  --observed results/observed-edge-bins.csv \
  --phases results/transition-phases.csv \
  --proxy results/decision-count-proxy.csv

python3 experiments/experiment_002/measurement_sensitivity_v01.py \
  --fcd results/observed-fcd.xml \
  --output results/sampling-sensitivity.csv \
  --report results/sampling-sensitivity.json

sha256sum results/native-external.xml results/native-with-internal.xml \
  results/observed-fcd.xml results/measurement-report.json > results/observation-hashes.txt
echo "MILESTONE MEASUREMENT COMPLETE: WINDOW=$WINDOW SEED=$SEED"
