#!/usr/bin/env python
import os

KernelVersion = "4.0.3"

def postInstall(fromVersion, fromRelease, toVersion, toRelease):
    # Must run depmod to keep the modules up to date :)
    os.system("/sbin/depmod %s" % KernelVersion)
