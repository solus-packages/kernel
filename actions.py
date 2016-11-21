#!/usr/bin/python
# -*- coding: utf-8 -*-
#
KVERSION = "4.8.10"

from pisi.actionsapi import kerneltools, shelltools, autotools, pisitools, get
import os

NoStrip = ["/boot"]

shelltools.export("KBUILD_BUILD_USER", "solus")
shelltools.export("KBUILD_BUILD_HOST", "toadstool")
shelltools.export("PYTHONDONTWRITEBYTECODE", "1")
shelltools.export("HOME", get.workDIR())
cached_jobs = get.makeJOBS()

def drop_jobs():
    if "JOBS" in os.environ:
        del os.environ["JOBS"]

def set_jobs():
    global cached_jobs
    os.environ["JOBS"] = cached_jobs

def setup():
    kerneltools.configure()

def build():
    kerneltools.build(debugSymbols=False)
    drop_jobs()
    shelltools.system("make -C tools/perf WERROR=0")
    set_jobs()

def install():
    # pisi needs patching to check if the links exist, before it removes them
    pisitools.dodir("/lib/modules/%s" % KVERSION)
    shelltools.echo("%s/lib/modules/%s/source" % (get.installDIR(), KVERSION), "mustFix")
    shelltools.echo("%s/lib/modules/%s/build" % (get.installDIR(), KVERSION), "mustFix")

    kerneltools.install()

    # Install kernel headers needed for out-of-tree module compilation
    kerneltools.installHeaders()
    kerneltools.installLibcHeaders()

    # Generate some module lists to use within mkinitramfs
    shelltools.system("./generate-module-list %s/lib/modules/%s" % (get.installDIR(), kerneltools.__getSuffix()))

    shelltools.system("ln -sv boot/kernel-%s %s/vmlinuz" % (KVERSION, get.installDIR()))

    # kernel-tools
    drop_jobs()
    shelltools.system("make -C tools/perf WERROR=0  install DESTDIR=%s prefix=/usr" % get.installDIR())
    set_jobs()
