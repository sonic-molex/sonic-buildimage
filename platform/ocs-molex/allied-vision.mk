ALLIEDVISION_VERSION = 1.0.0
MOLEX_ALLIEDVISION_DEB = allied-vision-$(ALLIEDVISION_VERSION)-amd64.deb
$(MOLEX_ALLIEDVISION_DEB)_URL = "https://raw.githubusercontent.com/sonic-molex/sonic-libmlx/refs/heads/ocs/$(MOLEX_ALLIEDVISION_DEB)"

SONIC_ONLINE_DEBS += $(MOLEX_ALLIEDVISION_DEB)
