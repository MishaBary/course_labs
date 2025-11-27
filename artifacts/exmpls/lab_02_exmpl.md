<div align="center">
<h1><a id="intro">Лабораторная работа №2</a><br></h1>
<a href="https://docs.github.com/en"><img src="https://img.shields.io/static/v1?logo=github&logoColor=fff&label=&message=Docs&color=36393f&style=flat" alt="GitHub Docs"></a>
<a href="https://daringfireball.net/projects/markdown"><img src="https://img.shields.io/static/v1?logo=markdown&logoColor=fff&label=&message=Markdown&color=36393f&style=flat" alt="Markdown"></a> 
<a href="https://symbl.cc/en/unicode-table"><img src="https://img.shields.io/static/v1?logo=unicode&logoColor=fff&label=&message=Unicode&color=36393f&style=flat" alt="Unicode"></a> 
<a href="https://shields.io"><img src="https://img.shields.io/static/v1?logo=shieldsdotio&logoColor=fff&label=&message=Shields&color=36393f&style=flat" alt="Shields"></a>
<a href="https://img.shields.io/badge/Risk_Analyze-2448a2"><img src="https://img.shields.io/badge/Course-Risk_Analysis-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/AppSec-2448a2" alt= "RA"></a> <img src="https://img.shields.io/badge/Contributor-Барышев_М._С.-8b9aff" alt="Contributor Badge"></a></div>

***

Данная лабораторная работа посвещена изучению *nix машин и как они работают, позволяет приобрести навыки для работы с терминалом/ консолью и приобрести знания по работе ОС. В лабоработрной работе описываются материалы по командам, скриптам и подключаемым приложениям.

***

## Задание

- ✔ 1. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ who | wc -I
$ id
$ whoami
$ hostnamectl
```

- ✔ 2. Выведите утилитой `tree` список вложенности дерева диреторий для каталога своего пользователя. Далее используйте `ls -a` и укажите отличие от `ls -l`.
- ✔ 3. Используйте утилиту `file` и `df` для определения какая файловая система на разделе `/dev/sda1`.
- ✔ 4. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ which vi
$ locate hello.py
$ sudo updatedb
$ locate hello
$ touch screen
$ find ~ -name screen
$ locate screen
$ sudo updated
$ locate screen
```

- ✔ 5. Используйте конструкцию и вставьте ее в созданный файл ранее. Подключите `pygame` - используем исключительно для стилизации окна.

```py
import pygame
pygame.init()

# Устанавливаем размеры окна
screen_width = 800
screen_height = 600
window_size = (screen_width, screen_height)
pygame.display.set_mode(window_size) # Создаем окно

# Задаем цвет фона
bg_color = (255, 255, 255)
pygame.draw.rect(screen, bg_color, [0, 0, screen_width, screen_height], 1)

# Выводим текст на экран
font = pygame.font.SysFont(None, 75)
text = font.render("Hello appsec world*", True, (0, 255, 0))
text_rect = text.get_rect()
text_rect.center = (400, 300)
screen.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
pygame.display.flip() # Обновляем экран
```

- ✔ 6. Сделайте `commit` и `push` в свой репозиторий с изменениями в `master branch`. На следующих лабораторных работах мы вернемся к этому файлу.
- ✔ 7. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ groups
$ useradd smallman
$ userdel smallman -rf
$ useradd smallman
$ passwd smallman
$ usermod smallman -c 'Hach Hachov Hacherovich,239,45-67,499-239-45-33'
$ passwd smallman
$ id smallman
$ groupadd -g 1500 readgroup
$ usermod -aG readgroup smallman
$ chmod 666 screen 
```


- ✔ 8. Выведите группу прав для `screen` и измените, что бы файл был доступен только для чтения созданному пользователю и выведите права этого польователя для измененного файла только используя `readgroup`.
- ✔ 9. Используйте `POSIX ACL`. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ touch nmapres.txt
$ setfacl -m u:smallman:rw nmapres.txt
$ setfacl -m g:readgroup:r nmapres.txt
$ getfacl nmapres.txt
```

- ✔ 10. Сохраните файл внутри локального репозитория, так как следующая работа будет подразумевать запись в нее данных о nmap.
- ✔ 11. Для закрепления выведите все списки групп пользователей на вашей ОС и права на верхнеуровневые каталоги.
- ✔ 12. Выведите все права для файлов и директорий локального репозитория которые имеют различные пользователи  (без использования длинных путей)
- ✔ 13. Выведите процессы которые у вас запущены в термине и вне его.
- ✔ 14. Оформить `README.md` по аналогии и использовать `shield`, etc.
- ✔ 15. Составить `gist` отчет и отправить ссылку личным сообщением

## Выполнение задания

- ✔ 1. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ who | wc -l # who показывает активные интерактивные сессии, wc -l считает строки → сколько пользователей "в системе" сейчас
# wc — word count, считает строки/слова/байты."-l" — выводит количество строк.

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ who | wc -l
0

$ id # показывает uid/gid текущего пользователя и его группы
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ id
uid=1000(lullaby) gid=1000(lullaby) groups=1000(lullaby) .....

$ whoami # выводит имя текущего пользователя
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ whoami
lullaby

$ hostnamectl # подробная инфа о хосте: имя, ОС, ядро, архитектура, тип машины
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ hostnamectl
 Static hostname: kali
       Icon name: computer-vm
         Chassis: vm 🖴
      Machine ID: 270f451f6d1e48be8be096448bae9068
         Boot ID: a483e51ee8944718be9a7607c4733f12
  Virtualization: oracle
Operating System: Kali GNU/Linux Rolling          
          Kernel: Linux 6.12.13-amd64
    Architecture: x86-64
 Hardware Vendor: innotek GmbH
  Hardware Model: VirtualBox
Firmware Version: VirtualBox
   Firmware Date: Fri 2006-12-01
    Firmware Age: 18y 11month 3w 3d

```

- ✔ 2. Выведите утилитой `tree` список вложенности дерева диреторий для каталога своего пользователя. Далее используйте `ls -a` и укажите отличие от `ls -l`.
```bash
┌──(lullaby㉿kali)-[~]
└─$ tree           
.
├── course_labs
│   ├── artifacts
│   │   ├── cheetsheet
│   │   │   ├── Docker_Image_Security_Best_Practices.pdf
│   │   │   └── gitscm.jpg
│   │   ├── exmpls
│   │   │   ├── Аналитический отчет по уязвимости PrintNightmare.pdf
│   │   │   ├── Пример - Multisignature - Безопасности криптовалютных платежей.pdf
│   │   │   └── Пример_аналитических_отчетов_по_задачам_ИБ.pdf
│   │   ├── owasp

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -a
.  ..  exmpl_hello.py  pygamesteel.py  README.md
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l
total 24
-rw-rw-r-- 1 lullaby lullaby   400 Nov 24 22:06 exmpl_hello.py
-rw-rw-r-- 1 lullaby lullaby   781 Nov 24 22:06 pygamesteel.py
-rw-rw-r-- 1 lullaby lullaby 16240 Nov 24 22:06 README.md

#ls: показывает содержимое каталога. Отличие: ls -a показывает содержимое и скрытые файлы, ls -l: выводит в формате: права, владелец, группа, размер, дата, имя
```
- ✔ 3. Используйте утилиту `file` и `df` для определения какая файловая система на разделе `/dev/sda1`.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo file -s /dev/sda1 # Флаг -s читает содержимое устройств, например /dev/sda1, чтобы определить ФС.
[sudo] password for lullaby: 
/dev/sda1: Linux rev 1.0 ext4 filesystem data, UUID=26eae727-e740-4fc1-bdf7-bcd8261a99e3 (needs journal recovery) (extents) (64bit) (large files) (huge files)
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ df -Th /dev/sda1  #показывает тип фс, размер, занято и точку монтирования раздела. -T — показывает тип ФС (ext4, xfs и др.), -h — human readable (размеры в ГБ/МБ)
Filesystem     Type  Size  Used Avail Use% Mounted on
/dev/sda1      ext4   47G   15G   30G  33% /

```
- ✔ 4. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ which vi # показывает путь к vi
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ which vi
/usr/bin/vi

$ locate hello.py # ищет hello.py в locate
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ locate hello.py
/home/lullaby/course_labs/labs/lab02/exmpl_hello.py
/home/lullaby/course_labs/labs/lab05/source/hello.py
/home/lullaby/risk_lab1/hello.py
/usr/lib/python3/dist-packages/mitmproxy/contrib/kaitaistruct/dtls_client_hello.py
/usr/lib/python3/dist-packages/mitmproxy/contrib/kaitaistruct/tls_client_hello.py

$ sudo updatedb # обновляет базу locate
$ locate hello # ищет все файлы/пути где встречается hello
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ locate hello   
/boot/grub/i386-pc/hello.mod
/home/lullaby/course_labs/labs/lab02/exmpl_hello.py
/home/lullaby/course_labs/labs/lab05/source/hello.py
/home/lullaby/risk_lab1/hello.py
/usr/lib/grub/i386-pc/hello.mod

$ touch screen
$ find ~ -name screen  # поиск по файловой системе в ~
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ find ~ -name screen
/home/lullaby/course_labs/labs/lab02/screen

$ locate screen  # ищет screen в locate
$ sudo updatedb # обновляем базу ещё раз после создания файла
$ locate screen # ищет screen в locate
```

- ✔ 5. Используйте конструкцию и вставьте ее в созданный файл ранее. Подключите `pygame` - используем исключительно для стилизации окна.

```py
import pygame
pygame.init()

# Устанавливаем размеры окна
screen_width = 800
screen_height = 600
window_size = (screen_width, screen_height)
pygame.display.set_mode(window_size) # Создаем окно

# Задаем цвет фона
bg_color = (255, 255, 255)
pygame.draw.rect(screen, bg_color, [0, 0, screen_width, screen_height], 1)

# Выводим текст на экран
font = pygame.font.SysFont(None, 75)
text = font.render("Hello appsec world*", True, (0, 255, 0))
text_rect = text.get_rect()
text_rect.center = (400, 300)
screen.blit(text, text_rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
pygame.display.flip() # Обновляем экран
```

- ✔ 6. Сделайте `commit` и `push` в свой репозиторий с изменениями в `master branch`. На следующих лабораторных работах мы вернемся к этому файлу.
- ✔ 7. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ groups # показывает группы текущего пользователя
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ groups                                    
lullaby adm dialout cdrom floppy sudo audio dip video plugdev users netdev bluetooth lpadmin wireshark scanner vboxsf kaboxer

$ useradd smallman # создаёт пользователя smallman
$ userdel smallman -rf # удаляет пользователя
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo userdel smallman -rf
userdel: smallman mail spool (/var/mail/smallman) not found
userdel: smallman home directory (/home/smallman) not found

$ useradd smallman
$ passwd smallman # задает пароль пользователю
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo passwd smallman 
New password: 
Retype new password: 
passwd: password updated successfully

$ usermod smallman -c 'Hach Hachov Hacherovich,239,45-67,499-239-45-33' # -c записывает GECOS-комментарий
$ passwd smallman
$ id smallman # выводит uid/gid и группы smallman
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo id smallman    
uid=1001(smallman) gid=1001(smallman) groups=1001(smallman)

$ groupadd -g 1500 readgroup # создает группу readgroup с gid=1500. -g — задать GID группы
$ usermod -aG readgroup smallman  # добавляет smallman в readgroup
# -a — append (добавить, а не заменить группы)
# -G — добавить в группы
$ chmod 666 screen # ставит права rw-rw-rw- (читать/писать всем)

Права: 7 = rwx (полный доступ), 
6 = rw- (чтение + запись),
5 = r-x (чтение + исполнение), 
4 = r-- (только чтение), 
3 = -wx (запись + исполнение), 
2 = -w- (только запись), 
1 = --x (только исполнение), 
0 = --- (нет доступа).

666 → rw-rw-rw- (владелец/группа/все)

```

- ✔ 8. Выведите группу прав для `screen` и измените, что бы файл был доступен только для чтения созданному пользователю и выведите права этого польователя для измененного файла только используя `readgroup`.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l screen.py 
-rw-rw-rw- 1 lullaby lullaby 595 Nov 26 13:19 screen.py

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo chgrp readgroup screen.py # меняем группу файла на readgroup
[sudo] password for lullaby:

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ sudo chmod 640 screen.py # права: владелец rw, группа r

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l screen.py
-rw-r----- 1 lullaby readgroup 595 Nov 26 13:19 screen.py

```
- ✔ 9. Используйте `POSIX ACL`. Выведите на терминале и проанализируйте следующие команды консоли

```bash
$ touch nmapres.txt
$ setfacl -m u:smallman:rw nmapres.txt # -m (modify) — изменить/добавить ACL запись. -x удаляет ACL
$ setfacl -m g:readgroup:r nmapres.txt
$ getfacl nmapres.txt
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ getfacl nmapres.txt
# file: nmapres.txt
# owner: lullaby
# group: lullaby
user::rw-
user:smallman:rw-
group::rw-
group:readgroup:r--
mask::rw-
other::r--

```

- ✔ 10. Сохраните файл внутри локального репозитория, так как следующая работа будет подразумевать запись в нее данных о nmap.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ git add nmapres.txt                       
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ git commit -m "for nmap"                           
[lab02-misha 1676067] for nmap
 1 file changed, 0 insertions(+), 0 deletions(-)
 create mode 100644 labs/lab02/nmapres.txt
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ git push                                  
Enumerating objects: 8, done.
Counting objects: 100% (8/8), done.
Delta compression using up to 8 threads
Compressing objects: 100% (4/4), done.
Writing objects: 100% (5/5), 1.02 KiB | 1.02 MiB/s, done.
Total 5 (delta 3), reused 1 (delta 0), pack-reused 0 (from 0)
remote: Resolving deltas: 100% (3/3), completed with 3 local objects.
To https://github.com/MishaBary/course_labs.git
   0a674fb..1676067  lab02-misha -> lab02-misha

```
- ✔ 11. Для закрепления выведите все списки групп пользователей на вашей ОС и права на верхнеуровневые каталоги.
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -ld /* 
lrwxrwxrwx   1 root root     7 Sep 12 18:37 /bin -> usr/bin
drwxr-xr-x   3 root root  4096 Sep 12 18:50 /boot
drwxr-xr-x  18 root root  3300 Nov 26 12:29 /dev
drwxr-xr-x 180 root root 12288 Nov 26 13:33 /etc
drwxr-xr-x   3 root root  4096 Sep 12 18:49 /home
# ls — показать информацию о файлах/каталогах
# -l — длинный формат
# -d выводит информацию о самих каталогах, а не содержимое

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ cat /etc/group
root:x:0:
daemon:x:1:
bin:x:2:
sys:x:3:

```
- ✔ 12. Выведите все права для файлов и директорий локального репозитория которые имеют различные пользователи  (без использования длинных путей)
```bash
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ls -l     
total 28
-rw-rw-r--  1 lullaby lullaby     400 Nov 24 22:06 exmpl_hello.py
-rw-rw-r--+ 1 lullaby lullaby       0 Nov 26 14:02 nmapres.txt
-rw-rw-r--  1 lullaby lullaby     781 Nov 24 22:06 pygamesteel.py
-rw-rw-r--  1 lullaby lullaby   16240 Nov 24 22:06 README.md
-rw-r-----  1 lullaby readgroup   595 Nov 26 14:00 screen.py

```
- ✔ 13. Выведите процессы которые у вас запущены в термине и вне его.
```bash
ps [option] # список процессо в всистеме
    -a # список всех процессов привязанных к терминалу
    -x # ... не привязанных к терминалу
    —е # показывает все процессы системы
    -f # показывает дерево процессов
    -u user # список процессов пользователя

┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ps -a            
    PID TTY          TIME CMD
  48734 pts/0    00:00:00 ps
                                                                                                     
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ ps -x
    PID TTY      STAT   TIME COMMAND
    976 ?        Ss     0:00 /usr/lib/systemd/systemd --user
    978 ?        S      0:00 (sd-pam)
    998 ?        Ss     0:00 /usr/bin/mpris-proxy
   1000 ?        S<sl   0:00 /usr/bin/pipewire

# + pstree 
┌──(lullaby㉿kali)-[~/course_labs/labs/lab02]
└─$ pstree 
```
- ✔ 14. Оформить `README.md` по аналогии и использовать `shield`, etc.
- ✔ 15. Составить `gist` отчет и отправить ссылку личным сообщением


**Вопрос из прошлой лабораторной**: Для чего нужен флаг -u в команде git push -u origin main
Флаг ```-u``` = ```--set-upstream``` устанавливает upstream-связь между локальной веткой и удалённой. После чего можно будет просто прописывать git push без указания конкретной ветки.

```bash
-u, --set-upstream
    For every branch that is up to date or successfully pushed, add upstream (tracking)
    reference, used by argument-less git-pull(1) and other commands. For more information,
    see branch.<name>.merge in git-config(1).
```

***
