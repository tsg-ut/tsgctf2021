# lkgit

## How to reproduce server environment 

Just run `bash ./deploy.sh`.

## How to run exploit

`make exp && cd solver && python2 ./exploit.py <host> <port>` or just use `solver/Dockerfile`.

## debug kernel

config files for buildroot(`build/.config`) and Linux kernel(`.config.linux`) is attached. You can use them to build your kernel with debug info to study it.

## Makefile

- `make exp`: compile exploit.
- `make dist`: compile `lkgit.tar.gz`.
- `make deploy`: compile images to deploy.

Refer to `Makefile` for other phonies.

## description

### En

The man made two wonderful software.  
I make them worse and worse.

The flag is `/home/user/flag`.

### Jp

もしも羊がウィスキーであったなら。

flagは`/home/user/flag`です。



## estimated difficulty 
medium
