#!/usr/bin/env bash

INSTALL_DIR=${1:-""}

echo "Stopping systemd service..."
sudo systemctl stop bno-to-nettables

echo "Removing systemd service from $INSTALL_DIR/lib/systemd/system"
rm "$INSTALL_DIR/lib/systemd/system/bno-to-nettables.service"

echo "Removing executable file from $INSTALL_DIR/opt/FRC3786/bin"
rm "$INSTALL_DIR/opt/FRC3786/bin/bno_tables.py "

