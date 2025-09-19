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
import logging
from contextlib import contextmanager, nullcontext

from itf.plugins.base.os.operating_system import OperatingSystem
from itf.plugins.base.target.base_target import Target
from itf.plugins.base.target.config.ecu import Ecu
from itf.plugins.base.target.processors.qvp_processor import TargetProcessorQVP
from itf.plugins.dlt.dlt_receive import DltReceive, Protocol


logger = logging.getLogger(__name__)


class TargetQvp(Target):
    """Target for the QVP (QNX Virtual Platform)."""

    def __init__(self, target_ecu: Ecu, target_sut_os: OperatingSystem = OperatingSystem.QNX):
        super().__init__(target_ecu, target_sut_os)

    # pylint: disable=unused-argument
    def register_processors(self, process=None, initialize_serial_device=True, initialize_serial_logs=True):
        self.sut = TargetProcessorQVP(self.target_ecu.sut, self.target_sut_os, process)
        self.processors.append(self.sut)


@contextmanager
def qvp_target(target_config, test_config):
    """Context manager for QVP target setup.

    Currently, only ITF tests against an already running QQVP instance is supported.
    """
    with nullcontext() as qvp_process:
        with DltReceive(
            target_ip=target_config.ip_address,
            protocol=Protocol.UDP,
            data_router_config=target_config.data_router_config,
            binary_path=test_config.dlt_receive_path,
        ):
            target = TargetQvp(test_config.ecu, test_config.os)
            target.register_processors(qvp_process)
            yield target
            target.teardown()
