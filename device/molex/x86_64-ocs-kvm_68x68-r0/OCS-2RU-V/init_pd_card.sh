#!/bin/bash
##
## OCS-2RU Virtual Device: Initialize PD Card Calibration Tables
##
## This script copies calibration tables from the device SKU directory
## to /var/vevice/pd_card/ where the HAL library expects them.
##
## Called by sonic-platform-ocs-kvm-ocs-2ru-v.postinst during package installation.
##

set -e

HWSKU_DIR="/usr/share/sonic/device/${PLATFORM}/${HWSKU}"
PD_CARD_SOURCE="${HWSKU_DIR}/pd_card"
PD_CARD_TARGET="/var/vevice/pd_card"

# Only run for OCS-2RU virtual device
if [[ "${HWSKU}" != *"OCS-2RU"* ]]; then
    echo "Not an OCS-2RU device, skipping PD card initialization"
    exit 0
fi

# Check if source directory exists
if [[ ! -d "${PD_CARD_SOURCE}" ]]; then
    echo "ERROR: PD card source directory not found: ${PD_CARD_SOURCE}"
    exit 1
fi

# Create target directory if it doesn't exist
mkdir -p "${PD_CARD_TARGET}"

# Copy calibration tables (only if not already present or if source is newer)
echo "Initializing PD card calibration tables for ${HWSKU}..."
for table in "${PD_CARD_SOURCE}"/*.bin; do
    if [[ -f "${table}" ]]; then
        table_name=$(basename "${table}")
        if [[ ! -f "${PD_CARD_TARGET}/${table_name}" ]] || \
           [[ "${table}" -nt "${PD_CARD_TARGET}/${table_name}" ]]; then
            cp -v "${table}" "${PD_CARD_TARGET}/"
        else
            echo "  ${table_name} already up-to-date"
        fi
    fi
done

# Set proper permissions
chmod -R 755 "${PD_CARD_TARGET}"

echo "✓ PD card initialization complete"
echo "  Location: ${PD_CARD_TARGET}"
echo "  Tables: $(ls -1 ${PD_CARD_TARGET}/*.bin | wc -l)"

exit 0
