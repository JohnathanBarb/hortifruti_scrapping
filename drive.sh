#!/bin/bash
SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")
VENVACTIVATEPATH=$(dirname "$SCRIPTPATH""/venv/bin/venv")
FILEPATH=$"driveestrela.py"


source "$VENVACTIVATEPATH/activate"
python3 "$SCRIPTPATH/driveestrela.py"

