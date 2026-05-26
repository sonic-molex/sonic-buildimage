LIBOTAI_VERSION = 1.1.0
OCSKVM_LIBOTAI_DEB = libsai-ocs-mlx-$(LIBOTAI_VERSION)-amd64.deb
$(OCSKVM_LIBOTAI_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(OCSKVM_LIBOTAI_DEB)"
$(OCSKVM_LIBOTAI_DEB)_DEPENDS += $(OCSKVM_ALLIEDVISION_DEB)

SONIC_ONLINE_DEBS += $(OCSKVM_LIBOTAI_DEB)
