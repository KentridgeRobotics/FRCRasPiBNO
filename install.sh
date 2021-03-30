#!/usr/bin/env bash

INSTALL_DIR=${1:-""}

mkdir -p "$INSTALL_DIR"/lib/systemd/system/ "$INSTALL_DIR"/opt/FRC3786/bin/

echo "Installing systemd service to $INSTALL_DIR/lib/systemd/system"
cp bno-to-nettables.service "$INSTALL_DIR"/lib/systemd/system

echo "Installing executable file to $INSTALL_DIR/opt/FRC3786/bin"
cp bno_tables.py "$INSTALL_DIR/opt/FRC3786/bin"

