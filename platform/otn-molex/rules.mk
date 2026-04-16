# NOTE: include $(PLATFORM_PATH)/thrift.mk is REMOVED - using system Thrift 0.17.0
include $(PLATFORM_PATH)/otn-libs-release.mk
include $(PLATFORM_PATH)/hal-server.mk
include $(PLATFORM_PATH)/hal-client.mk
include $(PLATFORM_PATH)/sai.mk
include $(PLATFORM_PATH)/docker-syncd-otn.mk
include $(PLATFORM_PATH)/platform-modules-otn.mk
include $(PLATFORM_PATH)/sonic-eventd-otn-profile.mk
include $(PLATFORM_PATH)/one-image.mk

SONIC_ALL += $(SONIC_ONE_IMAGE)

# Inject sai into syncd
$(SYNCD)_DEPENDS += $(MOLEX_LIBSAI_DEB) $(LIBSAIMETADATA_DEV)

# Inject otn-molex hal dependency library into pmon
# NOTE: Thrift dependency removed - pulled transitively from HALCLIENT
$(DOCKER_PLATFORM_MONITOR)_DEPENDS += $(MOLEX_HALCLIENT_DEB)

# Inject OTN event profile into docker-eventd (overwrites upstream default.json)
$(DOCKER_EVENTD)_DEPENDS += $(SONIC_EVENTD_OTN_PROFILE)

override EXTERNAL_KERNEL_PATCH_LOC := $(BUILD_WORKDIR)/$(PLATFORM_PATH)/non-upstream-patches/
