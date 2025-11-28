<div align="center">
<h1><a id="intro">Лабораторная работа №3</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Барышев_М._С.-8b9aff" alt="Contributor Badge"></a></div>

***
Данная лабораторная работа посвещена изучению `nmap` и как с ним работать. Эта лабораторная работа послужит подпоркой для старта в выявлении и определении уязвимостей на уровне сканера портов, что бы освоить базовые методы сканирования. 

***
## Задание

- [x] 1. Опишите используемые методы по их назначению, как они функционируют и какие результаты могут дать для оценки. Используйте сноску из материалов выше по флагам команд.
- [x] 2. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ nmap localhost # проверка 1000 портов

┌──(lullaby㉿kali)-[~]
└─$ nmap localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:09 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000030s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.14 seconds

$ nmap -sC localhost # -sC — запуск стандартных NSE-скриптов (определение сервисов, SSL, HTTP-info, баннеры)

┌──(lullaby㉿kali)-[~]
└─$ nmap -sC localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:09 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000020s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
| ssh-hostkey: 
|   256 48:69:73:5b:c5:a0:cc:91:05:5f:93:e1:a3:6c:a1:7c (ECDSA)
|_  256 a4:14:0e:f8:0d:49:da:19:eb:31:c1:b5:2d:50:fe:72 (ED25519)

Nmap done: 1 IP address (1 host up) scanned in 0.46 seconds

$ nmap -p localhost # флаг -p позволяет выбрать определенный порт 

┌──(lullaby㉿kali)-[~]
└─$ nmap -p localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:09 MSK
Found no matches for the service mask 'localhost' and your specified protocols
QUITTING!

$ nmap -O localhost # -O включает определение ОС устройства

┌──(lullaby㉿kali)-[~]
└─$ nmap -O localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:09 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000072s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
Device type: general purpose
Running: Linux 2.6.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32 cpe:/o:linux:linux_kernel:5 cpe:/o:linux:linux_kernel:6
OS details: Linux 2.6.32, Linux 5.0 - 6.2
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1.70 seconds

$ nmap -p 80 localhost # -p 80 сканирует только порт 80 (HTTP)

┌──(lullaby㉿kali)-[~]
└─$ nmap -p 80 localhost 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:10 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000059s latency).
Other addresses for localhost (not scanned): ::1

PORT   STATE  SERVICE
80/tcp closed http

Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds

$ nmap -p 443 localhost # -p 443 сканирует только порт 443 (HTTPS)

┌──(lullaby㉿kali)-[~]
└─$ nmap -p 443 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:10 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000055s latency).
Other addresses for localhost (not scanned): ::1

PORT    STATE  SERVICE
443/tcp closed https

Nmap done: 1 IP address (1 host up) scanned in 0.13 seconds

$ nmap -p 8443 localhost # -p 8443 сканирует альтернативный HTTPS или админ-панель

┌──(lullaby㉿kali)-[~]
└─$ nmap -p 8443 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:10 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000042s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE  SERVICE
8443/tcp closed https-alt

Nmap done: 1 IP address (1 host up) scanned in 0.11 seconds

$ nmap -p "*" localhost # "*" скан 65535 портов

┌──(lullaby㉿kali)-[~]
└─$ nmap -p "*" localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:10 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000010s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 8376 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.13 seconds

$ nmap -sV -p 22,8080 localhost # -sV - определение версии сервисов (service version detection), -p 22,8080 — список портов

┌──(lullaby㉿kali)-[~]
└─$ nmap -sV -p 22,8080 localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:11 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000096s latency).
Other addresses for localhost (not scanned): ::1

PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 9.9p1 Debian 3 (protocol 2.0)
8080/tcp closed http-proxy
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.29 seconds

$ nmap -sP 192.168.1.0/24 # проверка активных хостов без сканирования портов
# в моем случае другой IP
┌──(lullaby㉿kali)-[~]
└─$ nmap -sP 192.168.31.0/24
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:21 MSK
Nmap scan report for XiaoQiang (192.168.31.1)
Host is up (0.0040s latency).
MAC Address: D4:DA:21:79:96:DF (Beijing Xiaomi Mobile Software)
Nmap scan report for MishaPC (192.168.31.209)
Host is up (0.0013s latency).
MAC Address: C8:4D:44:23:E4:16 (Shenzhen Jiapeng Huaxiang Technology)
Nmap scan report for kali (192.168.31.101)
Host is up.
Nmap done: 256 IP addresses (3 hosts up) scanned in 2.17 seconds

$ nmap --open 192.168.1.1 # фильтрует вывод, скрывая closed / filtered, только открытые порты

┌──(lullaby㉿kali)-[~]
└─$ nmap --open 192.168.31.1
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:22 MSK
Nmap scan report for XiaoQiang (192.168.31.1)
Host is up (0.0016s latency).
Not shown: 996 closed tcp ports (reset)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
443/tcp  open  https
8080/tcp open  http-proxy
MAC Address: D4:DA:21:79:96:DF (Beijing Xiaomi Mobile Software)

Nmap done: 1 IP address (1 host up) scanned in 0.29 seconds

$ nmap --packet-trace 192.168.1.1 # показывает отправленные/полученные пакеты
# еще куча строк 
┌──(lullaby㉿kali)-[~]
└─$ nmap --packet-trace 192.168.31.1
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:23 MSK
SENT (0.0451s) ARP who-has 192.168.31.1 tell 192.168.31.101
RCVD (0.0473s) ARP reply 192.168.31.1 is-at D4:DA:21:79:96:DF
NSOCK INFO [0.1130s] nsock_iod_new2(): nsock_iod_new (IOD 1)

$ nmap --packet-trace scanme.nmap.org 
.
.
.
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.20s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 996 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
9929/tcp  open  nping-echo
31337/tcp open  Elite

$ nmap --iflist # вывод всех интерфейсов и маршрутов

┌──(lullaby㉿kali)-[~]
└─$ nmap --iflist
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:27 MSK
************************INTERFACES************************
DEV  (SHORT) IP/MASK                     TYPE     UP MTU   MAC
lo   (lo)    127.0.0.1/8                 loopback up 65536
lo   (lo)    ::1/128                     loopback up 65536
eth0 (eth0)  192.168.31.101/24           ethernet up 1500  08:00:27:FA:EF:C2
eth0 (eth0)  fe80::a00:27ff:fefa:efc2/64 ethernet up 1500  08:00:27:FA:EF:C2

**************************ROUTES**************************
DST/MASK                     DEV  METRIC GATEWAY
192.168.31.0/24              eth0 100
0.0.0.0/0                    eth0 100    192.168.31.1
::1/128                      lo   0
fe80::a00:27ff:fefa:efc2/128 eth0 0
fe80::/64                    eth0 1024
ff00::/8                     eth0 256

$ nmap -iL scanme.nmap.org # тут надо указывать файл, так как -iL (Input List) загружает адреса из файла
┌──(lullaby㉿kali)-[~]
└─$ nmap -iL scanme.nmap.org 
Failed to open input file scanme.nmap.org for reading: No such file or directory (2)

┌──(lullaby㉿kali)-[~]
└─$ echo "scanme.nmap.org" > targets.txt # указываем в файле и сканируем
                                                                                                     
┌──(lullaby㉿kali)-[~]
└─$ nmap -iL targets.txt
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:30 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.20s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 996 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
9929/tcp  open  nping-echo
31337/tcp open  Elite


$ nmap -A -iL scanme.nmap.org # -A включает ОС + версии сервисов + traceroute + NSE scripts

┌──(lullaby㉿kali)-[~]
└─$ nmap -A -iL targets.txt 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:31 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.19s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 996 closed tcp ports (reset)
PORT      STATE SERVICE    VERSION
22/tcp    open  ssh        OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 ac:00:a0:1a:82:ff:cc:55:99:dc:67:2b:34:97:6b:75 (DSA)
|   2048 20:3d:2d:44:62:2a:b0:5a:9d:b5:b3:05:14:c2:a6:b2 (RSA)
|   256 96:02:bb:5e:57:54:1c:4e:45:2f:56:4c:4a:24:b2:57 (ECDSA)
|_  256 33:fa:91:0f:e0:e1:7b:1f:6d:05:a2:b0:f1:54:41:56 (ED25519)
80/tcp    open  http       Apache httpd 2.4.7 ((Ubuntu))
|_http-favicon: Nmap Project
|_http-title: Go ahead and ScanMe!
|_http-server-header: Apache/2.4.7 (Ubuntu)
9929/tcp  open  nping-echo Nping echo
31337/tcp open  tcpwrapped
Aggressive OS guesses: Linux 5.0 - 5.14 (99%), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3) (99%), OpenWrt 21.02 (Linux 5.4) (96%), Linux 4.15 - 5.19 (96%), Linux 2.6.32 - 3.13 (95%), Linux 5.1 - 5.15 (95%), Linux 6.0 (95%), OpenWrt 22.03 (Linux 5.10) (95%), Linux 4.19 (95%), Linux 5.0 (94%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 27 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using port 80/tcp)
HOP RTT       ADDRESS
1   2.11 ms   XiaoQiang (192.168.31.1)
2   ...
3   4.46 ms   77.37.250.208
4   4.41 ms   212.124.13.32
5   4.62 ms   185.140.151.249
6   ... 7
8   45.03 ms  be7948.ccr42.fra05.atlas.cogentco.com (154.54.72.126)
9   48.24 ms  be2950.ccr42.ams03.atlas.cogentco.com (154.54.72.41)
10  148.05 ms be2183.ccr22.lpl01.atlas.cogentco.com (154.54.58.69)
11  155.08 ms be3042.ccr21.ymq01.atlas.cogentco.com (154.54.44.162)
12  147.96 ms be3501.ccr42.jfk02.atlas.cogentco.com (154.54.95.101)
13  144.38 ms be8030.ccr22.alb02.atlas.cogentco.com (154.54.169.226)
14  149.35 ms be2717.ccr41.ord01.atlas.cogentco.com (154.54.6.221)
15  152.44 ms be5068.ccr32.oma02.atlas.cogentco.com (154.54.166.73)
16  161.55 ms be8568.ccr82.den01.atlas.cogentco.com (154.54.95.109)
17  166.71 ms be3272.ccr21.den01.atlas.cogentco.com (154.54.83.69)
18  166.66 ms be3272.ccr21.den01.atlas.cogentco.com (154.54.83.69)
19  190.08 ms be3905.ccr21.sfo01.atlas.cogentco.com (154.54.1.210)
20  188.35 ms be3905.ccr21.sfo01.atlas.cogentco.com (154.54.1.210)
21  182.44 ms te0-0-0-18.ccr41.sjc03.atlas.cogentco.com (38.104.138.29)
22  182.26 ms 38.104.138.23
23  200.93 ms ae22.gw4.scz1.netarch.akamai.com (23.203.158.53)
24  ... 26
27  200.56 ms scanme.nmap.org (45.33.32.156)

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.64 seconds

$ nmap -sA scanme.nmap.org # -sA - фильтрует ли firewall

┌──(lullaby㉿kali)-[~]
└─$ nmap -sA scanme.nmap.org
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:32 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.20s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
All 1000 scanned ports on scanme.nmap.org (45.33.32.156) are in ignored states.
Not shown: 1000 unfiltered tcp ports (reset)

Nmap done: 1 IP address (1 host up) scanned in 2.91 seconds

$ nmap -PN scanme.nmap.org # не проверять доступность хоста с помощью ping, если блочат icmp

┌──(lullaby㉿kali)-[~]
└─$ nmap -PN scanme.nmap.org 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:32 MSK
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.20s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 996 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
9929/tcp  open  nping-echo
31337/tcp open  Elite

Nmap done: 1 IP address (1 host up) scanned in 2.11 seconds

$ nmap --script=vuln IP_addr -vv # показывает CVE, слабые конфиги, небезопасные сервисы, -vv — подробный вывод

┌──(lullaby㉿kali)-[~]
└─$ nmap --script=vuln IP_addr -vv
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:33 MSK
NSE: Loaded 105 scripts for scanning.
NSE: Script Pre-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 23:33
Completed NSE at 23:33, 10.04s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 23:33
Completed NSE at 23:33, 0.00s elapsed
Failed to resolve "IP_addr".
NSE: Script Post-scanning.
NSE: Starting runlevel 1 (of 2) scan.
Initiating NSE at 23:33
Completed NSE at 23:33, 0.00s elapsed
NSE: Starting runlevel 2 (of 2) scan.
Initiating NSE at 23:33
Completed NSE at 23:33, 0.00s elapsed
Read data files from: /usr/share/nmap
WARNING: No targets were specified, so 0 hosts scanned.
Nmap done: 0 IP addresses (0 hosts up) scanned in 10.20 seconds
           Raw packets sent: 0 (0B) | Rcvd: 0 (0B)

$ nmap -sV --script vuln -oN nmapres_new.txt localhost # -sV — версии сервисов, --script vuln — поиск уязвимостей, -oN file — сохранить обычный текстовый отчёт

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV --script vuln -oN nmapres_new.txt localhost
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:34 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000020s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:9.9p1: 
|       BA3887BD-F579-53B1-A4A4-FF49E953E1C0    8.1     https://vulners.com/githubexploit/BA3887BD-F579-53B1-A4A4-FF49E953E1C0       *EXPLOIT*
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254       *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0       *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       CNVD-2021-25272 5.9     https://vulners.com/cnvd/CNVD-2021-25272
|       6D74A425-60A7-557A-B469-1DD96A2D8FF8    5.9     https://vulners.com/githubexploit/6D74A425-60A7-557A-B469-1DD96A2D8FF8       *EXPLOIT*
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150       *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57       *EXPLOIT*
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.71 seconds

$ cat > ./nmapres_new.txt # сделать подобный пример файлу exmp_targets.txt

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ cat nmapres_new.txt    
scanme.nmap.org
192.168.31.0/24
localhost 

$ grep "VULNERABLE" nmapres_new.txt # данных полей в отчете нет, поэтому выведу другие

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "VULNERABLE" nmapres_new.txt
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "CVE" nmapres_new.txt

|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ grep "EXPLOIT" nmapres_new.txt
|       BA3887BD-F579-53B1-A4A4-FF49E953E1C0    8.1     https://vulners.com/githubexploit/BA3887BD-F579-53B1-A4A4-FF49E953E1C0       *EXPLOIT*
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254       *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0       *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       6D74A425-60A7-557A-B469-1DD96A2D8FF8    5.9     https://vulners.com/githubexploit/6D74A425-60A7-557A-B469-1DD96A2D8FF8       *EXPLOIT*
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150       *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57       *EXPLOIT*

$ mkdir -p ~/project/reports
$ nmap -sV -p 8080 --script vuln -oN ~/project/reports/nmapres_new.txt -oX ~/project/reports/nmapres_new.xml localhost # данный порт закрыт у меня, поэтому отчет будет маленьким и неинформативным, отсканирую все порты

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ sudo nmap -sV --script vuln --open -oN ~/project/reports/nmapres_new.txt -oX ~/project/reports/nmapres_new.xml localhost
# -oN — сохранить текстовый отчёт, -oX — сохранить XML отчёт, -sV — определение версий сервисов, -p 8080 — только порт 8080, --script vuln — запуск vuln-скриптов          
[sudo] password for lullaby: 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:47 MSK
Nmap scan report for localhost (127.0.0.1)
Host is up (0.0000020s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
| vulners: 
|   cpe:/a:openbsd:openssh:9.9p1: 
|       BA3887BD-F579-53B1-A4A4-FF49E953E1C0    8.1     https://vulners.com/githubexploit/BA3887BD-F579-53B1-A4A4-FF49E953E1C0       *EXPLOIT*
|       PACKETSTORM:189283      6.8     https://vulners.com/packetstorm/PACKETSTORM:189283      *EXPLOIT*
|       CVE-2025-26465  6.8     https://vulners.com/cve/CVE-2025-26465
|       9D8432B9-49EC-5F45-BB96-329B1F2B2254    6.8     https://vulners.com/githubexploit/9D8432B9-49EC-5F45-BB96-329B1F2B2254       *EXPLOIT*
|       85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0    6.8     https://vulners.com/githubexploit/85FCDCC6-9A03-597E-AB4F-FA4DAC04F8D0       *EXPLOIT*
|       1337DAY-ID-39918        6.8     https://vulners.com/zdt/1337DAY-ID-39918        *EXPLOIT*
|       CVE-2025-26466  5.9     https://vulners.com/cve/CVE-2025-26466
|       CNVD-2021-25272 5.9     https://vulners.com/cnvd/CNVD-2021-25272
|       6D74A425-60A7-557A-B469-1DD96A2D8FF8    5.9     https://vulners.com/githubexploit/6D74A425-60A7-557A-B469-1DD96A2D8FF8       *EXPLOIT*
|       CVE-2025-32728  4.3     https://vulners.com/cve/CVE-2025-32728
|       CVE-2025-61985  3.6     https://vulners.com/cve/CVE-2025-61985
|       CVE-2025-61984  3.6     https://vulners.com/cve/CVE-2025-61984
|       B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150    3.6     https://vulners.com/githubexploit/B7EACB4F-A5CF-5C5A-809F-E03CCE2AB150       *EXPLOIT*
|_      4C6E2182-0E99-5626-83F6-1646DD648C57    3.6     https://vulners.com/githubexploit/4C6E2182-0E99-5626-83F6-1646DD648C57       *EXPLOIT*
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.84 seconds


$ xsltproc ~/project/reports/nmapres_new.xml -o ~/project/reports/nmapres_new.html # xsltproc — XSLT процессор, делает web-страницу из XML отчёта
```

- [x] 3. Используйте команду `tree` и выведите все вложенные файлы по директориям.
```bash
┌──(lullaby㉿kali)-[~]
└─$ tree . #tree .  # показываем дерево каталогов и файлов текущей директории рекурсивно
.
├── course_labs
│   ├── artifacts
│   │   ├── cheetsheet
│   │   │   ├── Docker_Image_Security_Best_Practices.pdf
│   │   │   └── gitscm.jpg
│   │   ├── exmpls
...
```
- [x] 4.Найдите IP сетевой карты `Ethernet`, которая соответствует вашей виртуальной машине используя `ifconfig` и выполните команду

```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ ifconfig  # показывает список сетевых интерфейсов, их IP, маски, MAC и т.д.               
eth0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.31.101  netmask 255.255.255.0  broadcast 192.168.31.255
        inet6 fe80::a00:27ff:fefa:efc2  prefixlen 64  scopeid 0x20<link>
        ether 08:00:27:fa:ef:c2  txqueuelen 1000  (Ethernet)
        RX packets 8170  bytes 707236 (690.6 KiB)
        RX errors 0  dropped 1  overruns 0  frame 0
        TX packets 10442  bytes 666349 (650.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions                                                                       
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sP 192.168.31.101 
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:51 MSK
Nmap scan report for kali (192.168.31.101)
Host is up.
Nmap done: 1 IP address (1 host up) scanned in 0.00 seconds
```

- [x] 5. Определите ОС, данные ssh, telnet  с помощью `nmap` и выведитео них информацию.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -O 192.168.31.101
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:54 MSK
Nmap scan report for kali (192.168.31.101)
Host is up (0.000054s latency).
Not shown: 999 closed tcp ports (reset)
PORT   STATE SERVICE
22/tcp open  ssh
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.32
OS details: Linux 2.6.32
Network Distance: 0 hops

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 2.03 seconds

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV -p 23 192.168.31.101 # telnet 23 port
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:55 MSK
Nmap scan report for kali (192.168.31.101)
Host is up (0.000086s latency).

PORT   STATE  SERVICE VERSION
23/tcp closed telnet

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.28 seconds
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ nmap -sV -p 22 192.168.31.101 # ssh 22 port
Starting Nmap 7.95 ( https://nmap.org ) at 2025-11-26 23:55 MSK
Nmap scan report for kali (192.168.31.101)
Host is up (0.000083s latency).

PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.9p1 Debian 3 (protocol 2.0)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 0.20 seconds
```
- [x] 6. Результаты из `nmapres_new.txt` надо перенести в `nmapres.txt` и оставить оба файла рядом в локальном репозитории. Желательно использовать `cp` в консоли через редактор.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ cp nmapres_new.txt nmapres.txt
            
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ cp nmapres_new.txt ../lab02/nmapres.txt
                      
┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ ls
exmp_targets.txt  nmapres_new.txt  nmapres.txt  README.md

┌──(lullaby㉿kali)-[~/course_labs/labs/lab03]
└─$ ls ../lab02 
exmpl_hello.py  nmapres.txt  pygamesteel.py  README.md  screen.py

```
- [x] 7. Оформить `README.md` по аналогии и использовать `shield`, etc.
- [x] 8. Составить `gist` отчет и отправить ссылку личным сообщением

***