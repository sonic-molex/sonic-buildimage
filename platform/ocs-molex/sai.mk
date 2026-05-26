LIBSAI_VERSION = 1.1.0
MOLEX_LIBSAI_DEB = libsai-ocs-mlx-$(LIBSAI_VERSION)-amd64.deb
$(MOLEX_LIBSAI_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(MOLEX_LIBSAI_DEB)"
$(MOLEX_LIBSAI_DEB)_DEPENDS += $(MOLEX_ALLIEDVISION_DEB)

SONIC_ONLINE_DEBS += $(MOLEX_LIBSAI_DEB)
