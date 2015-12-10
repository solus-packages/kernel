#!/usr/bin/env python
import os
import shutil

KernelVersion = "4.1.14"

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    # Must run depmod to keep the modules up to date :)
    os.system("/sbin/depmod %s" % KernelVersion)

    kernel = "/boot/kernel-%s" % KernelVersion
    if os.path.exists("/boot/efi/solus"):
        try:
            shutil.copy(kernel, "/boot/efi/solus/kernel")
        except Exception, e:
            print("Failed to copy efi kernel")
