#!/bin/bash

cd "$( dirname "${BASH_SOURCE[0]}" )"
pushd ../src > /dev/null
export PYTHONPATH="$PWD:$PYTHONPATH"
popd > /dev/null
for file in *.py; do
  python $file ${file%.py}.png
done
