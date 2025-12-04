HALCLIENT_VERSION = 1.0.0
OTN_KVM_HALCLIENT_DEB = libhalplatformclient-mlx-$(HALCLIENT_VERSION)-amd64.deb
$(OTN_KVM_HALCLIENT_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/otn/$(OTN_KVM_HALCLIENT_DEB)"

SONIC_ONLINE_DEBS += $(OTN_KVM_HALCLIENT_DEB)
