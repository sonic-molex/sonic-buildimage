# SONIC ocs-kvm Demo Instructions

This doc contains the procedure to compile, run and test the SONiC-OCS KVM image, the prototype the team currently has.  
For SONiC compilation environment setup, please refer to [sonic-buildimage](https://github.com/sonic-net/sonic-buildimage) and [README.md](https://github.com/sonic-net/sonic-buildimage/blob/master/README.md)

# HOWTO Build ocs-kvm image

``` bash
make init
make configure PLATFORM=ocs-kvm
make BLDENV=bookworm SONIC_BUILD_JOBS=8 target/sonic-ocs-kvm.img.gz
```

# HOWTO setup KVM environment
1. Install Ubuntu KVM tools

```bash
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils -y 
```

2. Check CPU virtualization support

```bash
kvm-ok
INFO: /dev/kvm exists
KVM acceleration can be used
```

3. Copy the SONiC image to host
    - sonic-ocs-kvm.img.gz      --- compressed SONiC image 

4. Decompress the image
```bash
gunzip sonic-ocs-kvm.img.gz
```

## Running SONiC OCS KVM
```bash
sudo qemu-system-x86_64 \
  -hda sonic-ocs-kvm.img \
  -enable-kvm -m 4096 -smp 4 \
  -nographic \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -device e1000,netdev=net0


                             GNU GRUB  version 2.02

 +----------------------------------------------------------------------------+
 |*SONiC-OS-ocs.0-dirty-20250728.102930                                       | 
 | ONIE                                                                       |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            |
 |                                                                            | 
 +----------------------------------------------------------------------------+

      Use the ^ and v keys to select which entry is highlighted.
      Press enter to boot the selected OS, `e' to edit the commands       
      before booting or `c' for a command-line.

                             GNU GRUB  version 2.02
```
If want to quit qemu, please hold Ctrl and press A, then release both keys, and press X.

# HOWTO use ocs-kvm image
## Login directly in CLI
Input user and password to login, which are configured in config file, admin/YourPaSsWoRd for default.
```
sonic login: admin
Password: 
Linux sonic 6.1.0-29-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Wed Jul 23 02:54:51 UTC 2025 on ttyS0
admin@sonic:~$
```

## Login via SSH
Use ssh port 2222 to locally login to SONiC.
```
ssh -p 2222 admin@localhost

The authenticity of host '[localhost]:2222 ([127.0.0.1]:2222)' can't be established.
RSA key fingerprint is SHA256:+pZRW181kQeX5mhEoVaK9VTm1b/nFsyxdkfNYNaQwWY.
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '[localhost]:2222' (RSA) to the list of known hosts.
Debian GNU/Linux 12 \n \l

admin@localhost's password:
Linux sonic 6.1.0-29-2-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.123-1 (2025-01-02) x86_64
You are on
  ____   ___  _   _ _  ____
 / ___| / _ \| \ | (_)/ ___|
 \___ \| | | |  \| | | |
  ___) | |_| | |\  | | |___
 |____/ \___/|_| \_|_|\____|

-- Software for Open Networking in the Cloud --

Unauthorized access and/or use are prohibited.
All access and/or use are subject to monitoring.

Help:    https://sonic-net.github.io/SONiC/

Last login: Mon Aug 25 23:35:30 2025
admin@sonic:~$
```

## Show PMON platform information
### Show summary information
```bash
admin@sonic:~$ show platform summary 
Platform: x86_64-ocs-kvm_x86_64-r0
HwSKU: OCS-V
ASIC: ocs-kvm
ASIC Count: 1
Serial Number: D9401XXX
Model Number: 1835260XXX
Hardware Revision: 1.01
Switch Type: ocs
admin@sonic:~$
```

### Show PSU information
```bash
admin@sonic:~$ show platform psu
PSU    Model    Serial               HW Rev      Voltage (V)    Current (A)    Power (W)  Status    LED
-----  -------  -------------------  --------  -------------  -------------  -----------  --------  -----
PSU 1  VM-PSU   G1251551NJ220600XXX  R00               11.96           1.97        23.62  OK        green
PSU 2  VM-PSU   G1251551NJ220600XXX  R00               11.98           2.01        23.95  OK        green
admin@sonic:~$ 
```

### Show fan information
```bash
admin@sonic:~$ show platform fan
  Drawer    LED            FAN    Speed              Direction    Presence    Status          Timestamp
--------  -----  -------------  -------  ---------------------  ----------  --------  -----------------
FanTray0  green  FanTray0-Fan0      51%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan1      53%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan2      55%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
FanTray0  green  FanTray0-Fan3      57%  FAN_DIRECTION_EXHAUST     Present        OK  20250723 03:31:23
     N/A  green       PSU0-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250723 03:31:23
     N/A  green       PSU1-Fan     100%   FAN_DIRECTION_INTAKE     Present        OK  20250723 03:31:23
admin@sonic:~$
```

### Show thermal information
```bash
admin@sonic:~$ show platform temperature 
        Sensor    Temperature    High TH    Low TH    Crit High TH    Crit Low TH    Warning          Timestamp
--------------  -------------  ---------  --------  --------------  -------------  ---------  -----------------
  System Board              0         75        -5              70              0      False  20250723 03:32:23
System Exhaust              0         75        -5              70              0      False  20250723 03:32:23
admin@sonic:~$
```

### Show firmware information
```bash
admin@sonic:~$ show platform firmware status
Chassis    Module       Component    Version    Description
---------  -----------  -----------  ---------  -------------------------------------------------------------
OCS        LINE-CARD0   OCS0-0       1.02.0003  Optical Circuit Switch of 16x16
           SUPERVISOR0  BIOS         5.6.5      Performs initialization of hardware components during booting
                        FPGA         1.01.0004  Platform managment controller for on-board components
                        CPLD         1.01.0005  Used for managing IO modules
                        ONIE         2022.08    Open network install environment
admin@sonic:~$ 
```

## Redis
We have added the following tables to support data of OCS. 
- For CONFIG_DB (DB 4)
  - OCS_PORT
  - OCS_CROSS_CONNECT
- For STATE_DB (DB 6)
  - OCS_PORT_TABLE
  - OCS_CROSS_CONNECT_TABLE

## CLI Support for OCS
We use SONiC CLI Auto-generation tool to support SONiC OCS CLI by ocs yang model. For more detail please refer to [SONiC CLI Auto-generation tool](https://github.com/sonic-net/SONiC/blob/master/doc/cli_auto_generation/cli_auto_generation.md)

### Generate OCS CLI command
```bash
sudo -i
root@sonic:~# sonic-cli-gen generate show sonic-ocs
INFO:sonic-cli-gen: Auto-generation successful! Location: /usr/local/lib/python3.11/dist-packages/show/plugins/auto/sonic-ocs_yang.py

root@sonic:~# sonic-cli-gen generate config sonic-ocs
INFO:sonic-cli-gen: Auto-generation successful! Location: /usr/local/lib/python3.11/dist-packages/config/plugins/auto/sonic-ocs_yang.py
```

### Features
- show ocs-port
- show ocs-port-table
- show ocs-cross-connect
- show ocs-cross-connect-table
- config ocs-port
- config ocs-cross-connect

### Show OCS port configuration
```bash
root@sonic:~# show ocs-port
SIMPLEX PORT ID    LABEL           CONFIG STATUS
-----------------  --------------  ---------------
1A                 ingress_port1   normal
1B                 egress_port1    normal
2A                 ingress_port2   normal
2B                 egress_port2    normal
3A                 ingress_port3   normal
3B                 egress_port3    normal
4A                 ingress_port4   normal
4B                 egress_port4    normal
5A                 ingress_port5   normal
5B                 egress_port5    normal
6A                 ingress_port6   normal
6B                 egress_port6    normal
7A                 ingress_port7   normal
7B                 egress_port7    normal
8A                 ingress_port8   normal
8B                 egress_port8    normal
9A                 ingress_port9   normal
9B                 egress_port9    normal
10A                ingress_port10  normal
10B                egress_port10   normal
11A                ingress_port11  normal
11B                egress_port11   normal
12A                ingress_port12  normal
12B                egress_port12   normal
13A                ingress_port13  normal
13B                egress_port13   normal
14A                ingress_port14  normal
14B                egress_port14   normal
15A                ingress_port15  normal
15B                egress_port15   normal
16A                ingress_port16  normal
16B                egress_port16   normal
root@sonic:~#
```

### Show OCS port state
```bash
root@sonic:~# show ocs-port-table 
SIMPLEX PORT ID    CONNECTOR TYPE      CONNECTOR PIN  TARGET SIMPLEX PORT ID    OPER STATUS
-----------------  ----------------  ---------------  ------------------------  -------------
1A                 Duplex LC                       0  16B                       connected
1B                 Duplex LC                       0  16A                       connected
2A                 Duplex LC                       0  15B                       connected
2B                 Duplex LC                       0  15A                       connected
3A                 Duplex LC                       0  14B                       connected
3B                 Duplex LC                       0  14A                       connected
4A                 Duplex LC                       0  13B                       connected
4B                 Duplex LC                       0  13A                       connected
5A                 Duplex LC                       0  12B                       connected
5B                 Duplex LC                       0  12A                       connected
6A                 Duplex LC                       0  11B                       connected
6B                 Duplex LC                       0  11A                       connected
7A                 Duplex LC                       0  10B                       connected
7B                 Duplex LC                       0  10A                       connected
8A                 Duplex LC                       0  9B                        connected
8B                 Duplex LC                       0  9A                        connected
9A                 Duplex LC                       0  8B                        connected
9B                 Duplex LC                       0  8A                        connected
10A                Duplex LC                       0  7B                        connected
10B                Duplex LC                       0  7A                        connected
11A                Duplex LC                       0  6B                        connected
11B                Duplex LC                       0  6A                        connected
12A                Duplex LC                       0  5B                        connected
12B                Duplex LC                       0  5A                        connected
13A                Duplex LC                       0  4B                        connected
13B                Duplex LC                       0  4A                        connected
14A                Duplex LC                       0  3B                        connected
14B                Duplex LC                       0  3A                        connected
15A                Duplex LC                       0  2B                        connected
15B                Duplex LC                       0  2A                        connected
16A                Duplex LC                       0  1B                        connected
16B                Duplex LC                       0  1A                        connected
root@sonic:~# 
```

### Show OCS cross connect configuration
```bash
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
1A-16B              1A        16B
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~#
```

### Show OCS cross connect state
```bash
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
1A-16B              enabled   1A, panel IN 1, panel OUT 16, 16
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~# 
```

### Config OCS port
```bash
root@sonic:~# config ocs-port update 1A --config-status force_blocked
root@sonic:~# show ocs-port
SIMPLEX PORT ID    LABEL           CONFIG STATUS
-----------------  --------------  ---------------
1A                 ingress_port1   force_blocked
1B                 egress_port1    normal
2A                 ingress_port2   normal
2B                 egress_port2    normal
3A                 ingress_port3   normal
3B                 egress_port3    normal
4A                 ingress_port4   normal
4B                 egress_port4    normal
5A                 ingress_port5   normal
5B                 egress_port5    normal
6A                 ingress_port6   normal
6B                 egress_port6    normal
7A                 ingress_port7   normal
7B                 egress_port7    normal
8A                 ingress_port8   normal
8B                 egress_port8    normal
9A                 ingress_port9   normal
9B                 egress_port9    normal
10A                ingress_port10  normal
10B                egress_port10   normal
11A                ingress_port11  normal
11B                egress_port11   normal
12A                ingress_port12  normal
12B                egress_port12   normal
13A                ingress_port13  normal
13B                egress_port13   normal
14A                ingress_port14  normal
14B                egress_port14   normal
15A                ingress_port15  normal
15B                egress_port15   normal
16A                ingress_port16  normal
16B                egress_port16   normal
root@sonic:~#
root@sonic:~# show ocs-port-table
SIMPLEX PORT ID    CONNECTOR TYPE      CONNECTOR PIN  TARGET SIMPLEX PORT ID    OPER STATUS
-----------------  ----------------  ---------------  ------------------------  -------------
1A                 Duplex LC                       0  16B                       blocked
1B                 Duplex LC                       0  16A                       connected
2A                 Duplex LC                       0  15B                       connected
2B                 Duplex LC                       0  15A                       connected
3A                 Duplex LC                       0  14B                       connected
3B                 Duplex LC                       0  14A                       connected
4A                 Duplex LC                       0  13B                       connected
4B                 Duplex LC                       0  13A                       connected
5A                 Duplex LC                       0  12B                       connected
5B                 Duplex LC                       0  12A                       connected
6A                 Duplex LC                       0  11B                       connected
6B                 Duplex LC                       0  11A                       connected
7A                 Duplex LC                       0  10B                       connected
7B                 Duplex LC                       0  10A                       connected
8A                 Duplex LC                       0  9B                        connected
8B                 Duplex LC                       0  9A                        connected
9A                 Duplex LC                       0  8B                        connected
9B                 Duplex LC                       0  8A                        connected
10A                Duplex LC                       0  7B                        connected
10B                Duplex LC                       0  7A                        connected
11A                Duplex LC                       0  6B                        connected
11B                Duplex LC                       0  6A                        connected
12A                Duplex LC                       0  5B                        connected
12B                Duplex LC                       0  5A                        connected
13A                Duplex LC                       0  4B                        connected
13B                Duplex LC                       0  4A                        connected
14A                Duplex LC                       0  3B                        connected
14B                Duplex LC                       0  3A                        connected
15A                Duplex LC                       0  2B                        connected
15B                Duplex LC                       0  2A                        connected
16A                Duplex LC                       0  1B                        connected
16B                Duplex LC                       0  1A                        connected
root@sonic:~# 
```

### Config OCS cross connect
```bash
root@sonic:~# config ocs-cross-connect delete 1A-16B
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~#
root@sonic:~# config ocs-cross-connect add 1A-16B --a-side 1A --b-side 16B
root@sonic:~# show ocs-cross-connect
CROSS CONNECT ID    A SIDE    B SIDE
------------------  --------  --------
1A-16B              1A        16B
2A-15B              2A        15B
3A-14B              3A        14B
4A-13B              4A        13B
5A-12B              5A        12B
6A-11B              6A        11B
7A-10B              7A        10B
8A-9B               8A        9B
9A-8B               9A        8B
10A-7B              10A       7B
11A-6B              11A       6B
12A-5B              12A       5B
13A-4B              13A       4B
14A-3B              14A       3B
15A-2B              15A       2B
16A-1B              16A       1B
root@sonic:~# show ocs-cross-connect-table 
CROSS CONNECT ID    STATUS    PHYSICAL PATH
------------------  --------  --------------------------------
1A-16B              enabled   1A, panel IN 1, panel OUT 16, 16
2A-15B              enabled   2A, panel IN 2, panel OUT 15, 15
3A-14B              enabled   3A, panel IN 3, panel OUT 14, 14
4A-13B              enabled   4A, panel IN 4, panel OUT 13, 13
5A-12B              enabled   5A, panel IN 5, panel OUT 12, 12
6A-11B              enabled   6A, panel IN 6, panel OUT 11, 11
7A-10B              enabled   7A, panel IN 7, panel OUT 10, 10
8A-9B               enabled   8A, panel IN 8, panel OUT 9, 9B
9A-8B               enabled   9A, panel IN 9, panel OUT 8, 8B
10A-7B              enabled   10A, panel IN 10, panel OUT 7, 7
11A-6B              enabled   11A, panel IN 11, panel OUT 6, 6
12A-5B              enabled   12A, panel IN 12, panel OUT 5, 5
13A-4B              enabled   13A, panel IN 13, panel OUT 4, 4
14A-3B              enabled   14A, panel IN 14, panel OUT 3, 3
15A-2B              enabled   15A, panel IN 15, panel OUT 2, 2
16A-1B              enabled   16A, panel IN 16, panel OUT 1, 1
root@sonic:~#
```


## REST API Support for OCS
REST API follows RESTCONF protocol

In ```sonic-mgmt-common```, REST APIs are generated from ```sonic-ocs.yang``` yang model.

### Show OCS port configuration
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_PORT" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  2422  100  2422    0     0  89076      0 --:--:-- --:--:-- --:--:-- 89703
{
  "sonic-ocs:OCS_PORT": {
    "OCS_PORT_LIST": [
      {
        "config_status": "normal",
        "label": "ingress_port1",
        "simplex_port_id": "1A"
      },
      {
        "config_status": "normal",
        "label": "egress_port1",
        "simplex_port_id": "1B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port2",
        "simplex_port_id": "2A"
      },
      {
        "config_status": "normal",
        "label": "egress_port2",
        "simplex_port_id": "2B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port3",
        "simplex_port_id": "3A"
      },
      {
        "config_status": "normal",
        "label": "egress_port3",
        "simplex_port_id": "3B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port4",
        "simplex_port_id": "4A"
      },
      {
        "config_status": "normal",
        "label": "egress_port4",
        "simplex_port_id": "4B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port5",
        "simplex_port_id": "5A"
      },
      {
        "config_status": "normal",
        "label": "egress_port5",
        "simplex_port_id": "5B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port6",
        "simplex_port_id": "6A"
      },
      {
        "config_status": "normal",
        "label": "egress_port6",
        "simplex_port_id": "6B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port7",
        "simplex_port_id": "7A"
      },
      {
        "config_status": "normal",
        "label": "egress_port7",
        "simplex_port_id": "7B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port8",
        "simplex_port_id": "8A"
      },
      {
        "config_status": "normal",
        "label": "egress_port8",
        "simplex_port_id": "8B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port9",
        "simplex_port_id": "9A"
      },
      {
        "config_status": "normal",
        "label": "egress_port9",
        "simplex_port_id": "9B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port10",
        "simplex_port_id": "10A"
      },
      {
        "config_status": "normal",
        "label": "egress_port10",
        "simplex_port_id": "10B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port11",
        "simplex_port_id": "11A"
      },
      {
        "config_status": "normal",
        "label": "egress_port11",
        "simplex_port_id": "11B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port12",
        "simplex_port_id": "12A"
      },
      {
        "config_status": "normal",
        "label": "egress_port12",
        "simplex_port_id": "12B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port13",
        "simplex_port_id": "13A"
      },
      {
        "config_status": "normal",
        "label": "egress_port13",
        "simplex_port_id": "13B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port14",
        "simplex_port_id": "14A"
      },
      {
        "config_status": "normal",
        "label": "egress_port14",
        "simplex_port_id": "14B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port15",
        "simplex_port_id": "15A"
      },
      {
        "config_status": "normal",
        "label": "egress_port15",
        "simplex_port_id": "15B"
      },
      {
        "config_status": "normal",
        "label": "ingress_port16",
        "simplex_port_id": "16A"
      },
      {
        "config_status": "normal",
        "label": "egress_port16",
        "simplex_port_id": "16B"
      }
    ]
  }
}
admin@sonic:~$
```

### Show OCS port state
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_PORT_TABLE" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100  4236    0  4236    0     0   173k      0 --:--:-- --:--:-- --:--:--  179k
{
  "sonic-ocs:OCS_PORT_TABLE": {
    "OCS_PORT_LIST": [
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "1A",
        "target_simplex_port_id": "16B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "1B",
        "target_simplex_port_id": "16A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "2A",
        "target_simplex_port_id": "15B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "2B",
        "target_simplex_port_id": "15A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "3A",
        "target_simplex_port_id": "14B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "3B",
        "target_simplex_port_id": "14A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "4A",
        "target_simplex_port_id": "13B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "4B",
        "target_simplex_port_id": "13A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "5A",
        "target_simplex_port_id": "12B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "5B",
        "target_simplex_port_id": "12A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "6A",
        "target_simplex_port_id": "11B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "6B",
        "target_simplex_port_id": "11A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "7A",
        "target_simplex_port_id": "10B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "7B",
        "target_simplex_port_id": "10A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "8A",
        "target_simplex_port_id": "9B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "8B",
        "target_simplex_port_id": "9A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "9A",
        "target_simplex_port_id": "8B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "9B",
        "target_simplex_port_id": "8A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "10A",
        "target_simplex_port_id": "7B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "10B",
        "target_simplex_port_id": "7A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "11A",
        "target_simplex_port_id": "6B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "11B",
        "target_simplex_port_id": "6A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "12A",
        "target_simplex_port_id": "5B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "12B",
        "target_simplex_port_id": "5A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "13A",
        "target_simplex_port_id": "4B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "13B",
        "target_simplex_port_id": "4A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "14A",
        "target_simplex_port_id": "3B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "14B",
        "target_simplex_port_id": "3A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "15A",
        "target_simplex_port_id": "2B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "15B",
        "target_simplex_port_id": "2A"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "16A",
        "target_simplex_port_id": "1B"
      },
      {
        "connector_pin": "0",
        "connector_type": "Duplex LC",
        "oper_status": "connected",
        "simplex_port_id": "16B",
        "target_simplex_port_id": "1A"
      }
    ]
  }
}
admin@sonic:~$
```

### Show OCS cross connect configuration 
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   941  100   941    0     0  45181      0 --:--:-- --:--:-- --:--:-- 47050
{
  "sonic-ocs:OCS_CROSS_CONNECT": {
    "OCS_CROSS_CONNECT_LIST": [
      {
        "a_side": "2A",
        "b_side": "15B",
        "cross_connect_id": "2A-15B"
      },
      {
        "a_side": "3A",
        "b_side": "14B",
        "cross_connect_id": "3A-14B"
      },
      {
        "a_side": "4A",
        "b_side": "13B",
        "cross_connect_id": "4A-13B"
      },
      {
        "a_side": "5A",
        "b_side": "12B",
        "cross_connect_id": "5A-12B"
      },
      {
        "a_side": "6A",
        "b_side": "11B",
        "cross_connect_id": "6A-11B"
      },
      {
        "a_side": "7A",
        "b_side": "10B",
        "cross_connect_id": "7A-10B"
      },
      {
        "a_side": "8A",
        "b_side": "9B",
        "cross_connect_id": "8A-9B"
      },
      {
        "a_side": "9A",
        "b_side": "8B",
        "cross_connect_id": "9A-8B"
      },
      {
        "a_side": "10A",
        "b_side": "7B",
        "cross_connect_id": "10A-7B"
      },
      {
        "a_side": "11A",
        "b_side": "6B",
        "cross_connect_id": "11A-6B"
      },
      {
        "a_side": "12A",
        "b_side": "5B",
        "cross_connect_id": "12A-5B"
      },
      {
        "a_side": "13A",
        "b_side": "4B",
        "cross_connect_id": "13A-4B"
      },
      {
        "a_side": "14A",
        "b_side": "3B",
        "cross_connect_id": "14A-3B"
      },
      {
        "a_side": "15A",
        "b_side": "2B",
        "cross_connect_id": "15A-2B"
      },
      {
        "a_side": "16A",
        "b_side": "1B",
        "cross_connect_id": "16A-1B"
      }
    ]
  }
}
admin@sonic:~$
```


### Show OCS cross connect state 
```bash
admin@sonic:~$ curl -k -X GET "https://localhost/restconf/data/sonic-ocs:sonic-ocs/OCS_CROSS_CONNECT_TABLE" -H "accept: application/yang-data+json" | jq
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   848  100   848    0     0  39535      0 --:--:-- --:--:-- --:--:-- 40380
{
  "sonic-ocs:OCS_CROSS_CONNECT_TABLE": {
    "OCS_CROSS_CONNECT_LIST": [
      {
        "cross_connect_id": "2A-15B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "3A-14B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "4A-13B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "5A-12B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "6A-11B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "7A-10B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "8A-9B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "9A-8B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "10A-7B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "11A-6B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "12A-5B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "13A-4B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "14A-3B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "15A-2B",
        "status": "enabled"
      },
      {
        "cross_connect_id": "16A-1B",
        "status": "enabled"
      }
    ]
  }
}
admin@sonic:~$
```
