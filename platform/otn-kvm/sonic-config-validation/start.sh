#!/usr/bin/env bash

mkdir -p /var/sonic
echo "# Config files managed by sonic-config-engine" > /var/sonic/config_status

# Generate platform-specific CVL YIN schemas from /usr/share/sonic/platform/cvl-yang
# before rest-server starts so CVL can load them during process initialization.
/usr/bin/cvl-gen-yin.sh
