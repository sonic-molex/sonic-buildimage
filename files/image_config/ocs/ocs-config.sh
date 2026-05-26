#!/bin/bash

PLATFORM=${PLATFORM:-`sonic-cfggen -d -v DEVICE_METADATA.localhost.platform`}
HWSKU=${HWSKU:-`sonic-cfggen -d -v DEVICE_METADATA.localhost.hwsku`}
OCS_CONFIG="/usr/share/sonic/device/$PLATFORM/$HWSKU/ocs_config.json"

sonic-cfggen -j /usr/share/sonic/device/$PLATFORM/ocs-metadata.json --write-to-db

# Only load OCS port definitions on a fresh device (no existing OCS_PORT config).
# On image upgrade or normal reboot, config-setup.service has already loaded the
# user's saved configuration — we must not overwrite it.
OCS_PORT_COUNT=$(sonic-db-cli CONFIG_DB KEYS "OCS_PORT|*" | grep -c "OCS_PORT")
if [ "$OCS_PORT_COUNT" -eq 0 ]; then
    echo "Fresh device detected — initializing OCS port definitions from $OCS_CONFIG"
    sonic-cfggen -j "$OCS_CONFIG" --write-to-db
else
    echo "OCS_PORT already configured ($OCS_PORT_COUNT ports) — skipping OCS initialization"
fi
