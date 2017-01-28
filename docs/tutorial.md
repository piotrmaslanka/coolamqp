# Tutorial

If you want to connect to an AMQP broker, you need:
* its address (and port)
* login and password
* name of the virtual host

An idea of a heartbeat interval would be good, but you can do without. Since CoolAMQP will support clusters
in the future, you should define the nodes first. You can do it using _NodeDefinition_.
See NodeDefinition's documentation for alternative ways to do this, but here we will use
the AMQP connection string.

```python
from coolamqp.objects import NodeDefinition

node = NodeDefinition('amqp://user@password:host/vhost')
```

_Cluster_ instances are used to interface with the cluster (or a single broker). It
accepts a list of nodes:

```python
from coolamqp.clustering import Cluster
cluster = Cluster([node])
cluster.start(wait=True)
```

_wait=True_ will block until connection is completed. After this, you can use other methods.

## Publishing and consuming

Connecting is boring. After we do, we want to do something! Let's try sending a message, and receiving it. To do that,
you must first define a queue, and register a consumer.

```python
from coolamqp.objects import Queue

queue = Queue(u'my_queue', auto_delete=True, exclusive=True)

consumer, consume_confirm = cluster.consume(queue, no_ack=False)
consume_confirm.result()    # wait for consuming to start
```

This will create an auto-delete and exclusive queue. After than, a consumer will be registered for this queue.
_no_ack=False_ will mean that we have to manually confirm messages. 

You can specify a callback, that will be called with a message if one's received by this consumer. Since
we did not do that, this will go to a generic queue belonging to _Cluster_. 

_consumer_ is a _Consumer_ object. This allows us to do some things with the consumer (such as setting QoS),
but most importantly it allows us to cancel it later. _consume_confirm_ is a _Future_, that will succeed
when AMQP _basic.consume-ok_ is received.

To send a message we need to construct it first, and later publish:

```python
from coolamqp.objects import Message

msg = Message(b'hello world', properties=Message.Properties())
cluster.publish(msg, routing_key=u'my_queue')
```

This creates a message with no properties, and sends it through default (direct) exchange to our queue.
Note that CoolAMQP simply considers your messages to be bags of bytes + properties. It will not modify them,
nor decode, and will always expect and return bytes.

To actually get our message ...