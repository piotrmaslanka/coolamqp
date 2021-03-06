# coding=UTF-8
from __future__ import absolute_import, division, print_function

import logging
import os

from coolamqp.clustering import Cluster
from coolamqp.objects import NodeDefinition, Queue

NODE = NodeDefinition(os.environ.get('AMQP_HOST', '127.0.0.1'), 'guest', 'guest', heartbeat=20)
logging.basicConfig(level=logging.DEBUG)

amqp = Cluster([NODE])
amqp.start(wait=True)

q = Queue(u'lolwut', auto_delete=True, exclusive=True)
c, f = amqp.consume(q, no_ack=True, body_receive_mode=1)

# time.sleep(30)

# amqp.shutdown(True)
