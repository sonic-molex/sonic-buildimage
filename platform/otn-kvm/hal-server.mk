HALSERVER_VERSION = 1.1.0
OTN_KVM_HALSERVER_DEB = libhal-mlx-otn-kvm-$(HALSERVER_VERSION)-amd64.deb
$(OTN_KVM_HALSERVER_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/otn/$(OTN_KVM_HALSERVER_DEB)"


SONIC_ONLINE_DEBS += $(OTN_KVM_HALSERVER_DEB)
