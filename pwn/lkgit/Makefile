CC			:= gcc
SRC			:= src
CLIENT	:= $(SRC)/client
KERN		:= $(SRC)/kernel
INC			:= $(SRC)/include
EXP			:= solver
DIST		:= dist
BUILD		:= build
DEPLOY	:= deploy

ROOTFS 	= $(CLIENT)/client $(BUILD)/lkgit.ko $(BUILD)/init
DISTOBJ = $(DIST)/rootfs.cpio $(DIST)/rootfs.cpio $(DIST)/run.sh $(DIST)/bzImage $(DIST)/src

CPPFLAGS = -o $@
$(CLIENT)/client: CPPFLAGS += -z execstack -static -Wall -O0 -o $@
$(EXP)/exploit: CPPFLAGS += -static -Os -masm=intel -o $@

# client
$(CLIENT)/client: $(CLIENT)/client.c
	@echo $(CLIENT)
	$(CC) $(CPPFLAGS) $<

# exploit
$(EXP)/exploit.gz.b64: $(EXP)/exploit.c
	docker run -it --rm -v "$$PWD:$$PWD" -w "$$PWD" alpine /bin/sh -c 'apk add gcc musl-dev linux-headers && gcc $(CPPFLAGS) $< -o $(EXP)/exploit --static'
	strip $(EXP)/exploit
	gzip $(EXP)/exploit
	base64 $(EXP)/exploit.gz > $(EXP)/exploit.gz.b64
	rm -f $(EXP)/exploit.gz

# ko
$(BUILD)/lkgit.ko: $(KERN)/Makefile
	cd $(KERN) && $(MAKE)
	cp $(KERN)/lkgit.ko $@
	cd $(KERN) && $(MAKE) clean

# dist
$(DIST)/lkgit.tar.gz: $(DISTOBJ)
	rm -rf $@
	tar -C $(DIST) -czf  $(CURDIR)/$@ $(notdir $(DISTOBJ))
	rm -rf $(DIST)/src
	rm -rf $(DIST)/bzImage
	rm -rf $(DIST)/rootfs.cpio
	rm -rf $(DIST)/run.sh

$(DIST)/src: $(INC) $(CLIENT) $(KERN)
	rm -rf $@
	mkdir $@
	cp -r $(INC) $@
	mkdir $@/client
	mkdir $@/kernel
	cp -r $(CLIENT)/client.c $@/client
	cp -r $(KERN)/lkgit.c $@/kernel

$(DIST)/rootfs.cpio: $(BUILD)/rootfs.cpio
	cp $^ $@

$(DIST)/client: $(CLIENT)/client
	cp $^ $@

$(DIST)/run.sh: $(BUILD)/run.sh
	cp $^ $@

$(DIST)/bzImage: $(BUILD)/bzImage
	cp $^ $@

# filesystem to dist
$(BUILD)/rootfs.cpio: $(ROOTFS)
	rm -rf $(BUILD)/extracted && mkdir $(BUILD)/extracted
	cd $(BUILD)/extracted && cpio -idv --verbose < $(CURDIR)/$(BUILD)/rootfs.cpio || echo "hoge"
	chmod +x $(BUILD)/extracted/bin/*
	rm -f $@
	cp $^ $(BUILD)/extracted/
	echo "TSGCTF{this_is_fake_flag}" > $(BUILD)/extracted/flag
	cp $(BUILD)/setuidgid $(BUILD)/extracted/bin/
	cp $(BUILD)/cttyhack $(BUILD)/extracted/bin/
	cd $(BUILD)/extracted && find . -print0 | cpio --owner root --null -o --format=newc > $(CURDIR)/$@
	rm -rf $(BUILD)/extracted

# filesystem to deploy
$(DEPLOY)/rootfs.cpio: $(ROOTFS)
	rm -rf $(DEPLOY)/extracted && mkdir $(DEPLOY)/extracted
	cd $(DEPLOY)/extracted && cpio -idv < $(CURDIR)/$(BUILD)/rootfs.cpio
	chmod +x $(DEPLOY)/extracted/bin/*
	rm -f $@
	cp $^ $(DEPLOY)/extracted/
	cp $(BUILD)/flag $(DEPLOY)/extracted/flag
	cp $(BUILD)/setuidgid $(DEPLOY)/extracted/bin/
	cp $(BUILD)/cttyhack $(DEPLOY)/extracted/bin/
	cd $(DEPLOY)/extracted && find . -print0 | cpio --owner root --null -o --format=newc > $(CURDIR)/$@
	rm -rf $(DEPLOY)/extracted

# phonies
.PHONY: clean client dist build rootfs kern deploy
kern: $(BUILD)/lkgit.ko
client:	$(CLIENT)/client
exp: $(EXP)/exploit.gz.b64
dist: $(DIST)/lkgit.tar.gz Makefile
	$(MAKE) clean
build: $(BUILDOBJ)
rootfs: $(BUILD)/rootfs.cpio
deploy: $(DEPLOY)/rootfs.cpio
clean:
	rm -f $(CLIENT)/client
	cd $(KERN) && $(MAKE) clean
clean-all:
	$(MAKE) clean
	rm -f $(DIST)/lkgit.tar.gz