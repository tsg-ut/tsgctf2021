obj-m += lkgit.o
all:
	make -C ~/buildroot-2021.02.1/output/build/linux-5.10.25/ M=$(PWD) modules
	EXTRA_CFLAGS="-g DDEBUG"
clean:
	make -C ~/buildroot-2021.02.1/output/build/linux-5.10.25/ M=$(PWD) clean