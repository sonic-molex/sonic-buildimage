HALSERVER_VERSION = 1.1.0
OCSKVM_HALSERVER_DEB = libhal-mlx-ocs-kvm-$(HALSERVER_VERSION)-amd64.deb
$(OCSKVM_HALSERVER_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(OCSKVM_HALSERVER_DEB)"

SONIC_ONLINE_DEBS += $(OCSKVM_HALSERVER_DEB)
