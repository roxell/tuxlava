# -*- coding: utf-8 -*-
#
# vim: set ts=4
#
# Copyright 2026-present Linaro Limited
#
# SPDX-License-Identifier: MIT

import re

from tuxlava.exceptions import InvalidArgument
from tuxlava.tests import Test

UT_SUITE = re.compile(r"^[a-z0-9_]+$")


class UBootUT(Test):
    devices = ["qemu-arm64"]
    name = "uboot-ut"
    timeout = 10
    needs_os = False

    def suites(self, parameters):
        return parameters.get("UT_SUITES", "all").split()

    def validate(self, device, parameters, **kwargs):
        super().validate(device=device, parameters=parameters, **kwargs)

        suites = self.suites(parameters)
        if not suites or not all(UT_SUITE.match(s) for s in suites):
            raise InvalidArgument(
                "Invalid value for --parameters UT_SUITES, expected suite names"
            )

    def render(self, parameters, **kwargs):
        return self._render(
            "uboot-ut.yaml.jinja2",
            name=self.name,
            timeout=self.timeout,
            suites=self.suites(parameters),
            **kwargs,
        )


class UBootEFISelftest(Test):
    devices = ["qemu-arm64"]
    name = "uboot-efi-selftest"
    timeout = 10
    needs_os = False
    qemu_options = ["-device virtio-rng-pci"]
    needs_network = True

    def render(self, **kwargs):
        kwargs["name"] = self.name
        kwargs["timeout"] = self.timeout

        return self._render("uboot-efi-selftest.yaml.jinja2", **kwargs)
