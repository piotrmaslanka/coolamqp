# coding=UTF-8
"""
The layer that:
    - manages serialization/deserializtion (framing)
    - manages low-level data sending (streams)
    - sets up connection to AMQP
    - reacts and allows sending low-level AMQP commands

This layer bears no notion of fault tolerance
"""
from __future__ import absolute_import, division, print_function

from coolamqp.uplink.connection import Connection
from coolamqp.uplink.listener import ListenerThread
from coolamqp.uplink.reactor import Reactor
