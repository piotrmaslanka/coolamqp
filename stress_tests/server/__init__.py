import logging

from coolamqp.clustering.events import ReceivedMessage
from coolamqp.objects import Queue, Message

logger = logging.getLogger(__name__)
from satella.coding.concurrent import TerminableThread
from ..settings import queue_names, connect, LogFramesToFile


class Server(TerminableThread):
    def __init__(self, amqp):
        self.amqp = amqp
        super().__init__()
        self.consumers = []
        for queue_name in queue_names:
            cons, fut = self.amqp.consume(Queue(queue_name + '-repl'))
            self.consumers.append(cons)

    def loop(self):
        evt = self.amqp.drain(timeout=1.0)
        if isinstance(evt, ReceivedMessage):
            routing_key = evt.routing_key.tobytes().decode('utf8')
            routing_key = routing_key.replace('-repl', '')
            self.amqp.publish(Message(evt.body), routing_key=routing_key)


def run(notify_client, result_client, notify_server, server_result):
    logging.basicConfig(level=logging.DEBUG)

    lftf = LogFramesToFile('server.txt')

    amqp = connect(on_fail=server_result, log_frames=lftf)
    server = Server(amqp)

    notify_client.put(None)
    notify_server.get()

    server.start()

    try:
        notify_server.get()
    except KeyboardInterrupt:
        pass

    server.terminate().join()

    lftf.close()