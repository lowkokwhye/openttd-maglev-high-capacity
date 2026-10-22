#!/bin/sh
set -eu
cd "$(dirname "$0")"
nmlc --grf maglev_high_capacity_v0.1.0.grf --lang src/lang src/maglev_wagons.nml
