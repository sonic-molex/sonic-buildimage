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

# Initialize OCS-2RU virtual device calibration tables (if applicable)
# Copy .bin files from hwsku/pd_card/ to /var/vevice/pd_card/ where HAL expects them
if [ -d $HWSKU_DIR/pd_card ]; then
    PD_CARD_TARGET="/var/vevice/pd_card"
    mkdir -p "$PD_CARD_TARGET"
    
    echo "Initializing PD card calibration tables..."
    cp -v $HWSKU_DIR/pd_card/*.bin "$PD_CARD_TARGET/" 2>/dev/null
    
    if [ $? -eq 0 ]; then
        chmod -R 755 "$PD_CARD_TARGET"
        TABLE_COUNT=$(ls -1 $PD_CARD_TARGET/*.bin 2>/dev/null | wc -l)
        echo "✓ PD card calibration tables initialized ($TABLE_COUNT tables)"
    else
        echo "⚠ No PD card tables found or copy failed"
    fi
fi
