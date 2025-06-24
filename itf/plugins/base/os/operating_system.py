# *******************************************************************************
# Copyright (c) 2025 Contributors to the Eclipse Foundation
#
# See the NOTICE file(s) distributed with this work for additional
# information regarding copyright ownership.
#
# This program and the accompanying materials are made available under the
# terms of the Apache License Version 2.0 which is available at
# https://www.apache.org/licenses/LICENSE-2.0
#
# SPDX-License-Identifier: Apache-2.0
# *******************************************************************************
from enum import Enum
from itf.plugins.base.os.config import global_os_config as os_config

class OperatingSystem(Enum):
    LINUX = os_config.os.linux
    QNX = os_config.os.qnx
    UNSPECIFIED = {}

    @staticmethod
    def argparse(s):
        try:
            return OperatingSystem[s.upper()]
        except KeyError:
            return s
