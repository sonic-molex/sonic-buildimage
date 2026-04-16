HALCLIENT_VERSION = 1.1.0
MOLEX_HALCLIENT_DEB = libhalplatformclient-mlx-$(HALCLIENT_VERSION)-amd64.deb
$(MOLEX_HALCLIENT_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(MOLEX_HALCLIENT_DEB)"

SONIC_ONLINE_DEBS += $(MOLEX_HALCLIENT_DEB)
