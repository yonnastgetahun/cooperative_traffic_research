#!/bin/sh
# Frozen M3 harness qualification: NO held-out seed mode or dispatch.
set -eu
test -n "$SEED" && test -n "$WINDOW"
test "$SEED" = "2101" || { echo 'Disallowed seed; stop before generation' >&2; exit 40; }
case "$WINDOW" in 200|600|1200);; *) echo 'Disallowed window' >&2; exit 40;; esac
mkdir -p results
FROZEN_EXPECTED="be2e8d27c78c8b6de4891115d6d951edc877ac6e"

python3 experiments/experiment_002/m3_qualification/guard_v01.py \
  --seed "$SEED" --window "$WINDOW" --frozen-root frozen \
  --report results/frozen-source-integrity.json
test "$(git -C frozen rev-parse HEAD)" = "$FROZEN_EXPECTED" || {
  echo 'Frozen source checkout mismatch' >&2; exit 41;
}
python3 - <<'PY'
import json,os
s=json.load(open('source/scenario.json'))
assert s["seed"]==int(os.environ["SEED"])==2101
assert s["window_seconds"]==int(os.environ["WINDOW"])
assert s["vehicles"]==1000 and s["no_holdout"] is True
PY

# Generate the original fixed topology and OD demand, compare to M2 archive.
netgenerate --grid --grid.number 10 --grid.length 200 --output-file results/regenerated.net.xml
python3 frozen/experiments/experiment_002/fixed_demand_v01.py \
 --net results/regenerated.net.xml --out results/regenerated.trips.xml \
 --manifest results/regenerated-scenario.json --seed "$SEED" --window "$WINDOW"
python3 experiments/experiment_002/m3_qualification/verify_inputs_v01.py \
 --archived-net source/network.net.xml --regenerated-net results/regenerated.net.xml \
 --archived-trips source/trips.xml --regenerated-trips results/regenerated.trips.xml \
 --seed "$SEED" --window "$WINDOW" \
 --report results/seed-and-topology-integrity.json

# Choose routes with approved frozen equations, before any SUMO observations.
python3 frozen/experiments/experiment_002/time_aware.py \
 --net source/network.net.xml --trips source/trips.xml \
 --out results/control.rou.xml --audit results/control-audit.csv \
 --manifest results/control-manifest.json
cmp results/control.rou.xml source/original.rou.xml
cmp results/control-audit.csv source/original-audit.csv

# Reproduce frozen chosen-route cost equations; route/audit cannot differ.
python3 frozen/experiments/experiment_002/trace_actual_predictor.py \
 --net source/network.net.xml --trips source/trips.xml \
 --out results/traced.rou.xml --audit results/traced-audit.csv \
 --manifest results/traced-manifest.json \
 --trace results/chosen-decision-trace.csv \
 --candidate-trace results/candidate-decision-trace.csv \
 --decision-trace results/route-decisions.csv
cmp results/control.rou.xml results/traced.rou.xml
cmp results/control-audit.csv results/traced-audit.csv
cmp results/chosen-decision-trace.csv source/chosen-decision-trace.csv

# Observe all original search-time route-assignment counter reads.
python3 frozen/experiments/experiment_002/g3_live_search_capture_v01.py \
 --net source/network.net.xml --trips source/trips.xml \
 --out results/lookup.rou.xml --audit results/lookup-audit.csv \
 --manifest results/lookup-manifest.json \
 --events results/search-lookups.jsonl.gz --summary results/search-events.json
cmp results/control.rou.xml results/lookup.rou.xml
cmp results/control-audit.csv results/lookup-audit.csv
python3 frozen/experiments/experiment_002/g3_search_event_audit_v01.py \
 --events results/search-lookups.jsonl.gz --routes results/control.rou.xml \
 --report results/search-lookup-integrity.json

cat > results/measurement.add.xml <<'XML'
<additional>
  <edgeData id="external" file="native-external.xml" period="30" excludeEmpty="false" withInternal="false"/>
</additional>
XML

# SUMO receives frozen route choices as input: no policy action after observation.
sumo -n source/network.net.xml -r results/control.rou.xml \
 --additional-files results/measurement.add.xml \
 --fcd-output results/observed-fcd.xml \
 --device.fcd.period 1 --fcd-output.attributes lane,speed,pos \
 --vehroute-output results/native-vehroute.xml \
 --vehroute-output.exit-times true --vehroute-output.internal true \
 --statistic-output results/statistics.xml --summary-output results/summary.xml \
 --collision-output results/collisions.xml \
 --tripinfo-output results/tripinfo.xml \
 --seed "$SEED" --no-step-log true --log results/sumo.log
sumo --version > results/sumo-version.txt

python3 frozen/experiments/experiment_002/g3_tripinfo_invariance_v01.py \
 --baseline source/observed-tripinfo.xml --observed results/tripinfo.xml \
 --report results/tripinfo-invariance.json
python3 frozen/experiments/experiment_002/g3_native_vehroute_v01.py \
 --vehroute results/native-vehroute.xml --planned-routes results/control.rou.xml \
 --tripinfo results/tripinfo.xml --events results/native-events.csv \
 --report results/native-event-integrity.json
python3 frozen/experiments/experiment_002/g3_timing_bridge_v01.py \
 --trace results/chosen-decision-trace.csv \
 --events results/native-events.csv --fcd results/observed-fcd.xml \
 --report results/paired-reference-report.json --out results/paired-road-entry.csv

# Mechanical scoring adapter; frozen predictions/reference remain unchanged.
python3 experiments/experiment_002/m3_qualification/score_v01.py \
 --paired-road-entry results/paired-road-entry.csv --tripinfo results/tripinfo.xml \
 --archived-forecast-report source/actual-predictor-report.json \
 --seed "$SEED" --window "$WINDOW" --out results/seed-level-metrics.json
python3 frozen/experiments/experiment_002/g3_r3_exception_audit_v01.py \
 --routes results/control.rou.xml --tripinfo source/observed-tripinfo.xml \
 --replay-tripinfo results/tripinfo.xml --statistics results/statistics.xml \
 --fcd results/observed-fcd.xml --native results/native-external.xml \
 --seed "$SEED" --window "$WINDOW" --report results/r3-exception-audit.json

python3 - <<'PY'
import json
from pathlib import Path
p=Path("results")
j=lambda n:json.loads((p/n).read_text())
assert j("search-lookup-integrity.json")["status"]=="PASS"
assert j("tripinfo-invariance.json")["status"]=="PASS"
assert j("seed-and-topology-integrity.json")["status"]=="PASS"
assert j("r3-exception-audit.json")["exception_gate"]=="PASS_FOR_THIS_REPLAY"
assert j("r3-exception-audit.json")["reported_teleports"]["teleport_state"]=="ZERO_CONFIRMED"
assert j("paired-reference-report.json")["matched"]==j("paired-reference-report.json")["planned_edges"]
assert j("native-event-integrity.json")["vehicles_with_parsed_events"]==1000
assert j("seed-level-metrics.json")["matches_preexisting_M2_forecast_errors"] is True
(p/"policy-invariance.txt").write_text("Original frozen route and audit byte-equal to traced, search-observed and archived development policy.\n")
print("M3 DEVELOPMENT QUALIFICATION: SCIENTIFIC GATES PASSED")
PY

echo "Qualification source: $GITHUB_SHA" > results/qualifier-provenance.txt
echo "Frozen source: $FROZEN_EXPECTED" >> results/qualifier-provenance.txt
echo "Original preinspected M2 run: 40446073958" >> results/qualifier-provenance.txt
echo "Development seed=$SEED window=$WINDOW; heldout execution prohibited" >> results/qualifier-provenance.txt
sha256sum source/network.net.xml source/trips.xml source/original.rou.xml \
 source/observed-fcd.xml source/observed-tripinfo.xml > results/archived-source-hashes.txt
sha256sum results/control.rou.xml results/chosen-decision-trace.csv \
 results/paired-road-entry.csv results/seed-level-metrics.json \
 results/native-events.csv results/statistics.xml results/tripinfo.xml \
 results/r3-exception-audit.json > results/qualification-output-hashes.txt
echo "COMPLETE DEVELOPMENT-ONLY M3 QUALIFICATION seed=$SEED window=$WINDOW"
