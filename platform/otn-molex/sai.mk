LIBSAI_VERSION = 1.3.0
MOLEX_LIBSAI_DEB = libsai-otn-mlx-$(LIBSAI_VERSION)-amd64.deb
$(MOLEX_LIBSAI_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/otn/$(MOLEX_LIBSAI_DEB)"

SONIC_ONLINE_DEBS += $(MOLEX_LIBSAI_DEB)
