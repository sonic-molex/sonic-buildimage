#!/bin/bash

PLATFORM_DIR=/usr/share/sonic/platform
YANG_MODELS=/usr/models/yang
SCHEMA_BASE=/usr/sbin/schema/platform

platform_asic_file="$PLATFORM_DIR/platform_asic"
if [ ! -f "$platform_asic_file" ]; then
    logger -t cvl-gen-yin "platform_asic not found, skipping"
    exit 0
fi

platform_asic=$(cat "$platform_asic_file")
cvl_yang_dir="$PLATFORM_DIR/cvl-yang"

if [ ! -d "$cvl_yang_dir" ]; then
    logger -t cvl-gen-yin "no cvl-yang dir for $platform_asic, skipping"
    exit 0
fi

mkdir -p "$SCHEMA_BASE/$platform_asic"

for yang in "$cvl_yang_dir"/*.yang; do
    [ -f "$yang" ] || continue
    base=$(basename "$yang" .yang)
    pyang -f yin \
        -p "$YANG_MODELS" \
        -p "$cvl_yang_dir" \
        "$yang" \
        -o "$SCHEMA_BASE/$platform_asic/$base.yin"
done

logger -t cvl-gen-yin "CVL YIN schemas ready for platform_asic=$platform_asic"
