#!/bin/bash
##
## OCS-2RU Device: Initialize Calibration Directory
##
## This script creates the persistent calibration directory.
##
## Called by sonic-platform-ocs-molex.postinst during package installation.
##

set -e

CALIBRATION_TARGET="/usr/share/sonic/calibration"

# Only run for OCS-2RU device
if [[ "${HWSKU}" != *"OCS-2RU"* ]]; then
    echo "Not an OCS-2RU device, skipping initialization"
    exit 0
fi

echo "Initializing configuration for ${HWSKU}..."

# Create target directory if it doesn't exist
mkdir -p "${CALIBRATION_TARGET}"

# Define source directory (from the read-only image)
HWSKU_DIR="/usr/share/sonic/device/${PLATFORM}/${HWSKU}"
CALIBRATION_SOURCE="${HWSKU_DIR}/calibration"

# Copy calibration tables if source exists
if [[ -d "${CALIBRATION_SOURCE}" ]]; then
    echo "Syncing calibration tables from ${CALIBRATION_SOURCE}..."
    for table in "${CALIBRATION_SOURCE}"/*.bin; do
        if [[ -f "${table}" ]]; then
            table_name=$(basename "${table}")
            # Copy if missing or if source image has a newer version
            if [[ ! -f "${CALIBRATION_TARGET}/${table_name}" ]] || \
               [[ "${table}" -nt "${CALIBRATION_TARGET}/${table_name}" ]]; then
                echo "  Installing ${table_name}..."
                cp "${table}" "${CALIBRATION_TARGET}/"
            fi
        fi
    done
fi

# Set proper permissions
chmod -R 755 "${CALIBRATION_TARGET}"

echo "✓ OCS-2RU initialization complete"

exit 0
