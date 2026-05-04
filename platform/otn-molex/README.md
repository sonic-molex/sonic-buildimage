# SONIC otn-molex Demo Instructions

This doc contains the procedure to compile, run and test the SONiC-OTN image, the prototype the team currently has.  
For SONiC compilation environment setup, please refer to [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage) and [README.md](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)

Self-hosted Azure Pipeline PR validation is enabled for this platform branch.

# HOWTO Build otn-molex image

``` bash
make init
make configure PLATFORM=otn-molex
make BLDENV=bookworm SONIC_BUILD_JOBS=8 SONIC_OVERRIDE_BUILD_VARS=' INCLUDE_EXTERNAL_PATCHES=y ' target/sonic-otn-molex.bin
```
