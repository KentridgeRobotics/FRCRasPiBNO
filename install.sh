#!/usr/bin/env bash

INSTALL_DIR=${1:-""}

if [[ ! -d ".bno-tables-env" ]]; then
    echo "Make sure that you have setup the virtual environment before installing!!"
    exit 1
fi

mkdir -p "$INSTALL_DIR"/lib/systemd/system/ "$INSTALL_DIR"/opt/FRC3786/bin/bno/

echo "Installing systemd service to $INSTALL_DIR/lib/systemd/system"
cp bno-to-nettables.service "$INSTALL_DIR"/lib/systemd/system

echo "Installing executable file to $INSTALL_DIR/opt/FRC3786/bin/bno"
cp bno_tables.py "$INSTALL_DIR/opt/FRC3786/bin/bno"
cp -r .bno-tables-env/ "$INSTALL_DIR/opt/FRC3786/bin/bno"


sudo systemctl enable bno-to-nettables
