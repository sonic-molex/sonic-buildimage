#!/usr/bin/env bash

HWSKU_DIR=/usr/share/sonic/hwsku

mkdir -p /etc/sai.d/

# Create/Copy the sai.profile to /etc/sai.d/sai.profile
if [ -f $HWSKU_DIR/sai.profile.j2 ]; then
    sonic-cfggen -d -t $HWSKU_DIR/sai.profile.j2 > /etc/sai.d/sai.profile
else
    if [ -f $HWSKU_DIR/sai.profile ]; then
        cp $HWSKU_DIR/sai.profile /etc/sai.d/sai.profile
    fi
fi

# Copy RegisterFile to expected locations to support initialization for multiple devices
if [ -f $HWSKU_DIR/RegisterFile ]; then
    cp $HWSKU_DIR/RegisterFile /etc/RegisterFile-OCS-2RU
    cp $HWSKU_DIR/RegisterFile /etc/RegisterFile-CARMEL
    cp $HWSKU_DIR/RegisterFile /etc/RegisterFile-OCS
fi

# Initialize PD Card Calibration Tables (Mock for testing)
if [ -d "$HWSKU_DIR/pd_card" ]; then
    mkdir -p /var/vevice/pd_card
    cp $HWSKU_DIR/pd_card/*.bin /var/vevice/pd_card/
fi
