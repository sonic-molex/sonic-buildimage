HALCLIENT_VERSION = 1.1.0
OCSKVM_HALCLIENT_DEB = libhalplatformclient-mlx-$(HALCLIENT_VERSION)-amd64.deb
$(OCSKVM_HALCLIENT_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(OCSKVM_HALCLIENT_DEB)"

# NOTE: python3-thrift and thrift-compiler dependencies removed - using system Thrift 0.17.0
# These are available as Debian packages and will be installed via apt

SONIC_ONLINE_DEBS += $(OCSKVM_HALCLIENT_DEB)
