# coding=UTF-8

from __future__ import print_function, absolute_import, division

import logging
import os
import time
import unittest

from coolamqp.clustering import Cluster
from coolamqp.objects import NodeDefinition
from coolamqp.tracing import HoldingFrameTracer

NODE = NodeDefinition(os.environ.get('AMQP_HOST', '127.0.0.1'), 'guest', 'guest', heartbeat=20)
logging.basicConfig(level=logging.DEBUG)


class TestLogFrames(unittest.TestCase):
    def test_log_frames_works(self):
        frame_logger = HoldingFrameTracer()
        self.c = Cluster([NODE], log_frames=frame_logger)
        self.c.start()
        self.assertGreaterEqual(len(frame_logger.frames), 3)

    def tearDown(self):
        self.c.shutdown()

