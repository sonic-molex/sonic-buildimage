# docker image for molex otn syncd

DOCKER_SYNCD_PLATFORM_CODE = otn
include $(PLATFORM_PATH)/../template/docker-syncd-bookworm.mk

$(DOCKER_SYNCD_BASE)_DEPENDS += $(SYNCD) \
                                $(MOLEX_LIBSAI_DEB) \
                                $(MOLEX_HALSERVER_DEB) \
                                $(SONIC_EVENTD)

# Note: libthrift-0.17.0 will be auto-installed as dependency of HALSERVER

$(DOCKER_SYNCD_BASE)_DBG_DEPENDS += $(SYNCD_DBG) \
                                    $(LIBSWSSCOMMON_DBG) \
                                    $(LIBSAIMETADATA_DBG) \
                                    $(LIBSAIREDIS_DBG)

$(DOCKER_SYNCD_BASE)_VERSION = 1.0.0
$(DOCKER_SYNCD_BASE)_PACKAGE_NAME = syncd

$(DOCKER_SYNCD_BASE)_RUN_OPT += -v /host/warmboot:/var/warmboot
$(DOCKER_SYNCD_BASE)_RUN_OPT += -v /var/platform:/var/platform
$(DOCKER_SYNCD_BASE)_RUN_OPT += -v /usr/share/sonic/calibration:/usr/share/sonic/calibration:rw

