# Locate the commit that introduced this regression

A regression was reported against `systemd/systemd`.  The report, with any bisect result
and culprit diagnosis removed, is quoted verbatim below.

## Report

```
resolved: regression in answers on the local stub

The internet is broken!!!!
```console
$ ping www.youtube.com
ping: www.youtube.com: No address associated with hostname
$ build/test-nss dns www.youtube.com
======== dns ========
_nss_dns_gethostbyname4_r("www.youtube.com") → status=NSS_STATUS_NOTFOUND
                   pat=0x(nil) errno=999/--- h_errno=4/No address associated with name

_nss_dns_gethostbyname3_r("www.youtube.com", AF_INET) → status=NSS_STATUS_NOTFOUND
                   errno=999/--- h_errno=4/No address associated with name ttl=2147483647

_nss_dns_gethostbyname3_r("www.youtube.com", AF_INET6) → status=NSS_STATUS_NOTFOUND
                   errno=999/--- h_errno=4/No address associated with name ttl=2147483647

_nss_dns_gethostbyname3_r("www.youtube.com", *) → status=NSS_STATUS_UNAVAIL
                   errno=97/EAFNOSUPPORT h_errno=4/No address associated with name ttl=2147483647

_nss_dns_gethostbyname3_r("www.youtube.com", AF_UNIX) → status=NSS_STATUS_UNAVAIL
                   errno=97/EAFNOSUPPORT h_errno=4/No address associated with name ttl=2147483647

_nss_dns_gethostbyname2_r("www.youtube.com", AF_INET) → status=NSS_STATUS_NOTFOUND
                   errno=999/--- h_errno=4/No address associated with name

_nss_dns_gethostbyname2_r("www.youtube.com", AF_INET6) → status=NSS_STATUS_NOTFOUND
                   errno=999/--- h_errno=4/No address associated with name

_nss_dns_gethostbyname2_r("www.youtube.com", *) → status=NSS_STATUS_UNAVAIL
                   errno=97/EAFNOSUPPORT h_errno=4/No address associated with name

_nss_dns_gethostbyname2_r("www.youtube.com", AF_UNIX) → status=NSS_STATUS_UNAVAIL
                   errno=97/EAFNOSUPPORT h_errno=4/No address associated with name

_nss_dns_gethostbyname_r("www.youtube.com") → status=NSS_STATUS_NOTFOUND
                   errno=999/--- h_errno=4/No address associated with name

$ resolvectl query www.youtube.com
www.youtube.com: 2a00:1450:4001:811::200e      -- link: wlp4s0
                 2a00:1450:4001:812::200e      -- link: wlp4s0
                 2a00:1450:4001:80f::200e      -- link: wlp4s0
                 2a00:1450:4001:810::200e      -- link: wlp4s0
                 216.58.212.174                -- link: wlp4s0
                 142.250.74.206                -- link: wlp4s0
                 142.250.186.46                -- link: wlp4s0
                 142.250.186.110               -- link: wlp4s0
                 142.250.186.142               -- link: wlp4s0
                 142.250.186.174               -- link: wlp4s0
                 172.217.23.110                -- link: wlp4s0
                 216.58.212.142                -- link: wlp4s0
                 142.250.185.78                -- link: wlp4s0
                 172.217.16.142                -- link: wlp4s0
                 142.250.185.142               -- link: wlp4s0
                 142.250.185.174               -- link: wlp4s0
                 142.250.185.238               -- link: wlp4s0
                 (youtube-ui.l.google.com)

-- Information acquired via protocol DNS in 2.7ms.
-- Data is authenticated: no
```

I only noticed because I had `dns` in hosts from some earlier testing. 

<details>

```console
sudo tcpdump -vvv -i lo port domain
dropped privs to tcpdump
tcpdump: listening on lo, link-type EN10MB (Ethernet), snapshot length 262144 bytes
22:38:27.187126 IP (tos 0x0, ttl 64, id 1453, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.38262 > localhost.domain: [bad udp cksum 0xfe7b -> 0x11b6!] 5739+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.187170 IP (tos 0x0, ttl 64, id 1454, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.38262 > localhost.domain: [bad udp cksum 0xfe7b -> 0x4ead!] 48755+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.211921 IP (tos 0x0, ttl 1, id 64008, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.38262: [bad udp cksum 0xff7f -> 0x73ab!] 5739 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [54s] A 142.250.185.206, youtube-ui.l.google.com. [54s] A 142.250.185.238, youtube-ui.l.google.com. [54s] A 216.58.212.174, youtube-ui.l.google.com. [54s] A 142.250.74.206, youtube-ui.l.google.com. [54s] A 142.250.186.46, youtube-ui.l.google.com. [54s] A 142.250.186.78, youtube-ui.l.google.com. [54s] A 142.250.186.110, youtube-ui.l.google.com. [54s] A 142.250.186.174, youtube-ui.l.google.com. [54s] A 172.217.18.110, youtube-ui.l.google.com. [54s] A 172.217.23.110, youtube-ui.l.google.com. [54s] A 216.58.212.142, youtube-ui.l.google.com. [54s] A 142.250.185.78, youtube-ui.l.google.com. [54s] A 142.250.185.110, youtube-ui.l.google.com. [54s] A 142.250.185.142, youtube-ui.l.google.com. [54s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.213430 IP (tos 0x0, ttl 1, id 64010, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.38262: [bad udp cksum 0xfeff -> 0x60e5!] 48755 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m20s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m20s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m20s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m20s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.213518 IP (tos 0x0, ttl 64, id 1474, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.57421 > localhost.domain: [bad udp cksum 0xfe7b -> 0x17e5!] 50532+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.213531 IP (tos 0x0, ttl 64, id 1475, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.57421 > localhost.domain: [bad udp cksum 0xfe7b -> 0x9ce2!] 9575+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.214294 IP (tos 0x0, ttl 1, id 64011, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.57421: [bad udp cksum 0xff7f -> 0x88da!] 50532 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.214685 IP (tos 0x0, ttl 1, id 64012, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.57421: [bad udp cksum 0xfeff -> 0xb31a!] 9575 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.214802 IP (tos 0x0, ttl 64, id 1476, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.43609 > localhost.domain: [bad udp cksum 0xfe7b -> 0xd5d8!] 15717+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.215739 IP (tos 0x0, ttl 1, id 64013, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.43609: [bad udp cksum 0xff7f -> 0x46ce!] 15717 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.215874 IP (tos 0x0, ttl 64, id 1477, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.48026 > localhost.domain: [bad udp cksum 0xfe7b -> 0x7b4d!] 34479+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.216862 IP (tos 0x0, ttl 1, id 64014, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.48026: [bad udp cksum 0xff7f -> 0xec42!] 34479 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.217035 IP (tos 0x0, ttl 64, id 1478, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.53985 > localhost.domain: [bad udp cksum 0xfe7b -> 0xef7b!] 57401+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.217593 IP (tos 0x0, ttl 1, id 64015, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.53985: [bad udp cksum 0xfeff -> 0x05b4!] 57401 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.217732 IP (tos 0x0, ttl 64, id 1479, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.35377 > localhost.domain: [bad udp cksum 0xfe7b -> 0xf0a4!] 10177+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.218225 IP (tos 0x0, ttl 1, id 64016, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.35377: [bad udp cksum 0xfeff -> 0x06dd!] 10177 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.218366 IP (tos 0x0, ttl 64, id 1480, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.54925 > localhost.domain: [bad udp cksum 0xfe7b -> 0xcb5b!] 7086+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.219117 IP (tos 0x0, ttl 1, id 64017, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.54925: [bad udp cksum 0xff7f -> 0x3c51!] 7086 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.219171 IP (tos 0x0, ttl 64, id 1481, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.44395 > localhost.domain: [bad udp cksum 0xfe7b -> 0x81e8!] 36419+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.219917 IP (tos 0x0, ttl 1, id 64018, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.44395: [bad udp cksum 0xff7f -> 0xf2dd!] 36419 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.219998 IP (tos 0x0, ttl 64, id 1482, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.41473 > localhost.domain: [bad udp cksum 0xfe7b -> 0x6ae9!] 38316+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.220692 IP (tos 0x0, ttl 1, id 64019, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.41473: [bad udp cksum 0xfeff -> 0x8121!] 38316 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.220793 IP (tos 0x0, ttl 64, id 1483, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.54709 > localhost.domain: [bad udp cksum 0xfe7b -> 0x7aa3!] 21054+ [1au] AAAA? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.221118 IP (tos 0x0, ttl 1, id 64020, offset 0, flags [DF], proto UDP (17), length 204)
    localhost.domain > localhost.54709: [bad udp cksum 0xfeff -> 0x90db!] 21054 q: AAAA? www.youtube.com. 0/4/1 ns: youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:800::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:801::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80e::200e, youtube-ui.l.google.com. [3m19s] AAAA 2a00:1450:4001:80f::200e ar: . OPT UDPsize=65494 (176)
22:38:27.221293 IP (tos 0x0, ttl 64, id 1484, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.51347 > localhost.domain: [bad udp cksum 0xfe7b -> 0x8c0e!] 26869+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.222529 IP (tos 0x0, ttl 1, id 64021, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.51347: [bad udp cksum 0xff7f -> 0xfd03!] 26869 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
22:38:27.222610 IP (tos 0x0, ttl 64, id 1486, offset 0, flags [DF], proto UDP (17), length 72)
    localhost.44067 > localhost.domain: [bad udp cksum 0xfe7b -> 0x1449!] 64810+ [1au] A? www.youtube.com. ar: . OPT UDPsize=1200 (44)
22:38:27.223573 IP (tos 0x0, ttl 1, id 64022, offset 0, flags [DF], proto UDP (17), length 332)
    localhost.domain > localhost.44067: [bad udp cksum 0xff7f -> 0x853e!] 64810 q: A? www.youtube.com. 0/15/1 ns: youtube-ui.l.google.com. [53s] A 142.250.185.206, youtube-ui.l.google.com. [53s] A 142.250.185.238, youtube-ui.l.google.com. [53s] A 216.58.212.174, youtube-ui.l.google.com. [53s] A 142.250.74.206, youtube-ui.l.google.com. [53s] A 142.250.186.46, youtube-ui.l.google.com. [53s] A 142.250.186.78, youtube-ui.l.google.com. [53s] A 142.250.186.110, youtube-ui.l.google.com. [53s] A 142.250.186.174, youtube-ui.l.google.com. [53s] A 172.217.18.110, youtube-ui.l.google.com. [53s] A 172.217.23.110, youtube-ui.l.google.com. [53s] A 216.58.212.142, youtube-ui.l.google.com. [53s] A 142.250.185.78, youtube-ui.l.google.com. [53s] A 142.250.185.110, youtube-ui.l.google.com. [53s] A 142.250.185.142, youtube-ui.l.google.com. [53s] A 142.250.185.174 ar: . OPT UDPsize=65494 (304)
```
</details>
```

## What you have

- `/testbed/repo` is a git clone of `systemd/systemd` truncated just after the regression was
  reported.  `HEAD` is `66e52d22210eeec86fd87bc4ff2cc0b107546750` and the full history behind it is present.
- The commit that introduced the regression is an ancestor of `HEAD`.  The commit that
  *fixes* it is not in this repository -- it was written after the cutoff.
- You do not need to build or test the project.  Reading history, `git log`, `git diff`,
  `git show` and writing your own probe scripts is the intended way to work.
- Some release-note and changelog files have been removed from the working tree on purpose.

## What to produce

Write the full 40-character hexadecimal SHA of the **first bad commit** -- the single
commit that introduced this regression -- into `/testbed/answer.txt`, and nothing else:

```
echo <40-char-sha> > /testbed/answer.txt
```

Requirements:

- Exactly one line, exactly 40 lowercase hex characters.  Abbreviated SHAs are rejected.
- No explanation, no extra lines, no surrounding punctuation.
- The commit must exist in this repository.

## Rules

- Do **not** use the network.  This task is derived from a public issue report and the
  answer is published on the internet; fetching it is cheating and is detected and
  scored zero.  Solve it from the repository.
- Do not rewrite history, add remotes, or fetch objects.
