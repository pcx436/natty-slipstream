# natty-slipstream

Simplified NAT Slipstream server and client.

* Simple SIP Server
* Just handles SIP `REGISTER` part to punch hole in firewall (no HTTP/browser magic)
* Clients for Windows, Linux and macOS

More info in this post [Abusing Application Layer Gateways](https://embracethered.com/blog/posts/2020/nat-slipstreaming-simplified/)

## What have I changed?
### Features
* Added HTTP server to `sip-server.py` which serves a TCP port that we want to victimize.
* Added `curl` call to `natty.sh` to retrieve victim port.
* Actually connect to victim port and send info to it.

### Usage
Attacker: `python3 sip-server.py VICTIM_PORT`

Victim: `bash ./natty.sh ATTACKER_IP SIP_PORT HTTP_PORT [LOCAL_IP]`


## Requirements for attack
This seems rather obvious, but you may need to do it in your lab environment to make this work.

On the Linux router in your lab environment, you'll need to load the `nf_nat_sip` and `nf_conntrack_sip` conntrack
modules. This enables the SIP Application Layer Gateway. Without it, the SIP connection will not be interpreted
correctly by the NAT. Also, ensure that `net.netfilter.nf_conntrack_helper=1`.

## Reference

Inspired by NAT Slipstream by Samy Kamkar (https://samy.pl/slipstream)

https://github.com/samyk/slipstream
