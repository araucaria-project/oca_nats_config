#! /bin/bash
SCRIPT_PATH="${BASH_SOURCE:-$0}"
ABS_SCRIPT_PATH="$(realpath "${SCRIPT_PATH}")"

DIR_PATH="$(dirname "$ABS_SCRIPT_PATH")"

cd $DIR_PATH
cd ..

OLD_HEAD=$(git rev-parse HEAD)

git pull

NEW_HEAD=$(git rev-parse HEAD)

if [ "$OLD_HEAD" != "$NEW_HEAD" ]
then
        poetry update
        poetry install
        poetry run build
fi