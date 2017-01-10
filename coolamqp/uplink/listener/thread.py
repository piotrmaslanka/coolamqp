# coding=UTF-8
from __future__ import absolute_import, division, print_function

import threading

from coolamqp.uplink.listener.epoll_listener import EpollListener


class ListenerThread(threading.Thread):
    """
    A thread that does the listening.

    It automatically picks the best listener for given platform.
    """

    def __init__(self):
        threading.Thread.__init__(self)
        self.daemon = True
        self.terminating = False
        self.listener = EpollListener()

    def terminate(self):
       self.terminating = True

    def run(self):
        while not self.terminating:
            self.listener.wait(timeout=1)
        self.listener.shutdown()

    def register(self, sock, on_read=lambda data: None, on_fail=lambda: None):
        """
        Add a socket to be listened for by the loop.

        :param sock: a socket instance (as returned by socket module)
        :param on_read: callable(data) to be called with received data
        :param on_fail: callable() to be called when socket fails

        :return: a BaseSocket instance to use instead of this socket
        """
        return self.listener.register(sock, on_read, on_fail)