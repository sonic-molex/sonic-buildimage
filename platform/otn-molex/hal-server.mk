HALSERVER_VERSION = 1.1.0
MOLEX_HALSERVER_DEB = libhal-mlx-otn-molex-$(HALSERVER_VERSION)-amd64.deb
$(MOLEX_HALSERVER_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(MOLEX_HALSERVER_DEB)"

SONIC_ONLINE_DEBS += $(MOLEX_HALSERVER_DEB)
