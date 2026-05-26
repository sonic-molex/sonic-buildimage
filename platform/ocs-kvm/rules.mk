include $(PLATFORM_PATH)/hal-server.mk
include $(PLATFORM_PATH)/hal-client.mk
include $(PLATFORM_PATH)/allied-vision.mk
include $(PLATFORM_PATH)/sai.mk
include $(PLATFORM_PATH)/docker-syncd-ocs-kvm.mk
include $(PLATFORM_PATH)/platform-modules-ocs-kvm.mk
include $(PLATFORM_PATH)/sonic-version.mk
include $(PLATFORM_PATH)/one-image.mk
include $(PLATFORM_PATH)/onie.mk
include $(PLATFORM_PATH)/kvm-image.mk
include $(PLATFORM_PATH)/raw-image.mk

SONIC_ALL += $(SONIC_ONE_IMAGE) $(SONIC_KVM_IMAGE) $(SONIC_RAW_IMAGE)

# Inject ocs-kvm otai into syncd
$(SYNCD)_DEPENDS += $(OCSKVM_LIBOTAI_DEB) $(LIBSAIMETADATA_DEV)

# Inject ocs-kvm hal dependency library into pmon
$(DOCKER_PLATFORM_MONITOR)_DEPENDS += $(OCSKVM_HALCLIENT_DEB)
