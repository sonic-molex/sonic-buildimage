#!/bin/bash
#
# inject_ocs_ledd.sh - Inject ocs-ledd into pmon container
#
# This script dynamically injects the ocs-ledd daemon and its supervisord
# configuration into the running pmon container. It is designed to be called
# after the pmon container starts.
#
# Usage:
#   /usr/local/bin/inject_ocs_ledd.sh
#
# Exit codes:
#   0 - Success
#   1 - pmon container not running
#   2 - Failed to copy ocs-ledd binary
#   3 - Failed to copy supervisord config
#   4 - Failed to register with supervisord

set -e

PMON_CONTAINER="pmon"
OCS_LEDD_BIN="/usr/bin/ocs-ledd"
OCS_LEDD_CONF="/etc/sonic/pmon/ocs-ledd.conf"
TARGET_BIN="/usr/local/bin/ocs-ledd"
TARGET_CONF="/etc/supervisor/conf.d/ocs-ledd.conf"

# ANSI color codes for better readability
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
    logger -t inject_ocs_ledd -p user.info "$1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
    logger -t inject_ocs_ledd -p user.warning "$1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
    logger -t inject_ocs_ledd -p user.err "$1"
}

# Check if pmon container is running
check_pmon_running() {
    if ! docker ps --format '{{.Names}}' | grep -q "^${PMON_CONTAINER}$"; then
        log_error "pmon container is not running"
        exit 1
    fi
    log_info "pmon container is running"
}

# Copy ocs-ledd binary to pmon container
copy_binary() {
    if [ ! -f "$OCS_LEDD_BIN" ]; then
        log_error "ocs-ledd binary not found at $OCS_LEDD_BIN"
        exit 2
    fi
    
    log_info "Copying ocs-ledd binary to pmon container..."
    if ! docker cp "$OCS_LEDD_BIN" "${PMON_CONTAINER}:${TARGET_BIN}"; then
        log_error "Failed to copy ocs-ledd binary"
        exit 2
    fi
    
    # Set executable permissions
    docker exec "$PMON_CONTAINER" chmod +x "$TARGET_BIN"
    
    log_info "Successfully copied ocs-ledd binary"
}

# Copy supervisord configuration to pmon container
copy_config() {
    if [ ! -f "$OCS_LEDD_CONF" ]; then
        log_error "ocs-ledd.conf not found at $OCS_LEDD_CONF"
        exit 3
    fi
    
    log_info "Copying supervisord config to pmon container..."
    if ! docker cp "$OCS_LEDD_CONF" "${PMON_CONTAINER}:${TARGET_CONF}"; then
        log_error "Failed to copy supervisord config"
        exit 3
    fi
    
    log_info "Successfully copied supervisord config"
}

# Register ocs-ledd with supervisord
register_with_supervisord() {
    log_info "Reloading supervisord configuration..."
    if ! docker exec "$PMON_CONTAINER" supervisorctl reread; then
        log_error "Failed to reread supervisord config"
        exit 4
    fi
    
    log_info "Adding ocs-ledd to supervisord..."
    # Check if ocs-ledd is already added
    if docker exec "$PMON_CONTAINER" supervisorctl status ocs-ledd &>/dev/null; then
        log_warn "ocs-ledd is already registered, updating..."
        docker exec "$PMON_CONTAINER" supervisorctl update ocs-ledd
    else
        if ! docker exec "$PMON_CONTAINER" supervisorctl add ocs-ledd; then
            log_error "Failed to add ocs-ledd to supervisord"
            exit 4
        fi
    fi
    
    log_info "Starting ocs-ledd service..."
    if ! docker exec "$PMON_CONTAINER" supervisorctl start ocs-ledd; then
        log_warn "Failed to start ocs-ledd (it may already be running)"
    fi
    
    # Wait a moment for the service to start
    sleep 2
    
    # Check status
    log_info "Checking ocs-ledd status..."
    docker exec "$PMON_CONTAINER" supervisorctl status ocs-ledd || true
}

# Main execution
main() {
    log_info "Starting ocs-ledd injection into pmon container..."
    
    check_pmon_running
    copy_binary
    copy_config
    register_with_supervisord
    
    log_info "✓ Successfully injected ocs-ledd into pmon container"
}

# Run main function
main
