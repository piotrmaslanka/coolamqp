# coding=UTF-8
from __future__ import print_function, absolute_import
"""
A Python version of the AMQP machine-readable specification.

Generated automatically by CoolAMQP from AMQP machine-readable specification.
See coolamqp.uplink.framing.compilation for the tool

AMQP is copyright (c) 2016 OASIS
CoolAMQP is copyright (c) 2016 DMS Serwis s.c.
"""

import struct, collections, warnings, logging, six

from coolamqp.framing.base import AMQPClass, AMQPMethodPayload, AMQPContentPropertyList
from coolamqp.framing.field_table import enframe_table, deframe_table, frame_table_size
from coolamqp.framing.compilation.content_property import compile_particular_content_property_list_class

logger = logging.getLogger(__name__)

Field = collections.namedtuple('Field', ('name', 'type', 'basic_type', 'reserved'))

# Core constants
FRAME_METHOD = 1
FRAME_HEADER = 2
FRAME_BODY = 3
FRAME_HEARTBEAT = 8
FRAME_MIN_SIZE = 4096
FRAME_END = 206
REPLY_SUCCESS = 200 # Indicates that the method completed successfully. This reply code is
                    # reserved for future use - the current protocol design does not use positive
                    # confirmation and reply codes are sent only in case of an error.
CONTENT_TOO_LARGE = 311 # The client attempted to transfer content larger than the server could accept
                        # at the present time. The client may retry at a later time.
NO_CONSUMERS = 313 # When the exchange cannot deliver to a consumer when the immediate flag is
                   # set. As a result of pending data on the queue or the absence of any
                   # consumers of the queue.
CONNECTION_FORCED = 320 # An operator intervened to close the connection for some reason. The client
                        # may retry at some later date.
INVALID_PATH = 402 # The client tried to work with an unknown virtual host.
ACCESS_REFUSED = 403 # The client attempted to work with a server entity to which it has no
                     # access due to security settings.
NOT_FOUND = 404 # The client attempted to work with a server entity that does not exist.
RESOURCE_LOCKED = 405 # The client attempted to work with a server entity to which it has no
                      # access because another client is working with it.
PRECONDITION_FAILED = 406 # The client requested a method that was not allowed because some precondition
                          # failed.
FRAME_ERROR = 501 # The sender sent a malformed frame that the recipient could not decode.
                  # This strongly implies a programming error in the sending peer.
SYNTAX_ERROR = 502 # The sender sent a frame that contained illegal values for one or more
                   # fields. This strongly implies a programming error in the sending peer.
COMMAND_INVALID = 503 # The client sent an invalid sequence of frames, attempting to perform an
                      # operation that was considered invalid by the server. This usually implies
                      # a programming error in the client.
CHANNEL_ERROR = 504 # The client attempted to work with a channel that had not been correctly
                    # opened. This most likely indicates a fault in the client layer.
UNEXPECTED_FRAME = 505 # The peer sent a frame that was not expected, usually in the context of
                       # a content header and body.  This strongly indicates a fault in the peer's
                       # content processing.
RESOURCE_ERROR = 506 # The server could not complete the method because it lacked sufficient
                     # resources. This may be due to the client creating too many of some type
                     # of entity.
NOT_ALLOWED = 530 # The client tried to work with some entity in a manner that is prohibited
                  # by the server, due to security settings or by some other criteria.
NOT_IMPLEMENTED = 540 # The client tried to use functionality that is not implemented in the
                      # server.
INTERNAL_ERROR = 541 # The server could not complete the method because of an internal error.
                     # The server may require intervention by an operator in order to resume
                     # normal operations.

HARD_ERROR = [CONNECTION_FORCED, INVALID_PATH, FRAME_ERROR, SYNTAX_ERROR, COMMAND_INVALID, CHANNEL_ERROR, UNEXPECTED_FRAME, RESOURCE_ERROR, NOT_ALLOWED, NOT_IMPLEMENTED, INTERNAL_ERROR]
SOFT_ERROR = [CONTENT_TOO_LARGE, NO_CONSUMERS, ACCESS_REFUSED, NOT_FOUND, RESOURCE_LOCKED, PRECONDITION_FAILED]


DOMAIN_TO_BASIC_TYPE = {
    u'class-id': u'short',
    u'consumer-tag': u'shortstr',
    u'delivery-tag': u'longlong',
    u'exchange-name': u'shortstr',
    u'method-id': u'short',
    u'no-ack': u'bit',
    u'no-local': u'bit',
    u'no-wait': u'bit',
    u'path': u'shortstr',
    u'peer-properties': u'table',
    u'queue-name': u'shortstr',
    u'redelivered': u'bit',
    u'message-count': u'long',
    u'reply-code': u'short',
    u'reply-text': u'shortstr',
    u'bit': None,
    u'octet': None,
    u'short': None,
    u'long': None,
    u'longlong': None,
    u'shortstr': None,
    u'longstr': None,
    u'timestamp': None,
    u'table': None,
}

class Connection(AMQPClass):
    """
    The connection class provides methods for a client to establish a network connection to
    
    a server, and for both peers to operate the connection thereafter.
    """
    NAME = u'connection'
    INDEX = 10


class ConnectionClose(AMQPMethodPayload):
    """
    Request a connection close
    
    This method indicates that the sender wants to close the connection. This may be
    due to internal conditions (e.g. a forced shut-down) or due to an error handling
    a specific method, i.e. an exception. When a close is due to an exception, the
    sender provides the class and method id of the method which caused the exception.
    """
    NAME = u'connection.close'

    INDEX = (10, 50)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x32'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reply-code', u'reply-code', u'short', reserved=False),
        Field(u'reply-text', u'reply-text', u'shortstr', reserved=False),
        Field(u'class-id', u'class-id', u'short', reserved=False),
        Field(u'method-id', u'method-id', u'short', reserved=False),
    ]

    def __init__(self, reply_code, reply_text, class_id, method_id):
        """
        Create frame connection.close

        :type reply_code: int, 16 bit unsigned (reply-code in AMQP)
        :type reply_text: binary type (max length 255) (reply-text in AMQP)
        :param class_id: Failing method class
            When the close is provoked by a method exception, this is the class of the
            method.
        :type class_id: int, 16 bit unsigned (class-id in AMQP)
        :param method_id: Failing method id
            When the close is provoked by a method exception, this is the ID of the method.
        :type method_id: int, 16 bit unsigned (method-id in AMQP)
        """
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.class_id = class_id
        self.method_id = method_id

    def write_arguments(self, buf):
        buf.write(struct.pack('!HB', self.reply_code, len(self.reply_text)))
        buf.write(self.reply_text)
        buf.write(struct.pack('!HH', self.class_id, self.method_id))
        
    def get_size(self):
        return 7 + len(self.reply_text)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        reply_code, s_len, = struct.unpack_from('!HB', buf, offset)
        offset += 3
        reply_text = buf[offset:offset+s_len]
        offset += s_len
        class_id, method_id, = struct.unpack_from('!HH', buf, offset)
        offset += 4
        return ConnectionClose(reply_code, reply_text, class_id, method_id)


class ConnectionCloseOk(AMQPMethodPayload):
    """
    Confirm a connection close
    
    This method confirms a Connection.Close method and tells the recipient that it is
    safe to release resources for the connection and close the socket.
    """
    NAME = u'connection.close-ok'

    INDEX = (10, 51)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x33'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x0A\x00\x33\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame connection.close-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return ConnectionCloseOk()


class ConnectionOpen(AMQPMethodPayload):
    """
    Open connection to virtual host
    
    This method opens a connection to a virtual host, which is a collection of
    resources, and acts to separate multiple application domains within a server.
    The server may apply arbitrary limits per virtual host, such as the number
    of each type of entity that may be used, per connection and/or in total.
    """
    NAME = u'connection.open'

    INDEX = (10, 40)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x28'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'virtual-host', u'path', u'shortstr', reserved=False),
        Field(u'reserved-1', u'shortstr', u'shortstr', reserved=True),
        Field(u'reserved-2', u'bit', u'bit', reserved=True),
    ]

    def __init__(self, virtual_host):
        """
        Create frame connection.open

        :param virtual_host: Virtual host name
            The name of the virtual host to work with.
        :type virtual_host: binary type (max length 255) (path in AMQP)
        """
        self.virtual_host = virtual_host

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.virtual_host)))
        buf.write(self.virtual_host)
        buf.write(b'\x00')
        buf.write(struct.pack('!B', 0))
        
    def get_size(self):
        return 3 + len(self.virtual_host)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        virtual_host = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        offset += s_len # reserved field!
        offset += 1
        return ConnectionOpen(virtual_host)


class ConnectionOpenOk(AMQPMethodPayload):
    """
    Signal that connection is ready
    
    This method signals to the client that the connection is ready for use.
    """
    NAME = u'connection.open-ok'

    INDEX = (10, 41)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x29'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x0A\x00\x29\x00\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'shortstr', u'shortstr', reserved=True),
    ]

    def __init__(self):
        """
        Create frame connection.open-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        offset += s_len # reserved field!
        return ConnectionOpenOk()


class ConnectionStart(AMQPMethodPayload):
    """
    Start connection negotiation
    
    This method starts the connection negotiation process by telling the client the
    protocol version that the server proposes, along with a list of security mechanisms
    which the client can use for authentication.
    """
    NAME = u'connection.start'

    INDEX = (10, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'version-major', u'octet', u'octet', reserved=False),
        Field(u'version-minor', u'octet', u'octet', reserved=False),
        Field(u'server-properties', u'peer-properties', u'table', reserved=False),
        Field(u'mechanisms', u'longstr', u'longstr', reserved=False),
        Field(u'locales', u'longstr', u'longstr', reserved=False),
    ]

    def __init__(self, version_major, version_minor, server_properties, mechanisms, locales):
        """
        Create frame connection.start

        :param version_major: Protocol major version
            The major version number can take any value from 0 to 99 as defined in the
            AMQP specification.
        :type version_major: int, 8 bit unsigned (octet in AMQP)
        :param version_minor: Protocol minor version
            The minor version number can take any value from 0 to 99 as defined in the
            AMQP specification.
        :type version_minor: int, 8 bit unsigned (octet in AMQP)
        :param server_properties: Server properties
            The properties SHOULD contain at least these fields: "host", specifying the
            server host name or address, "product", giving the name of the server product,
            "version", giving the name of the server version, "platform", giving the name
            of the operating system, "copyright", if appropriate, and "information", giving
            other general information.
        :type server_properties: table. See coolamqp.uplink.framing.field_table (peer-properties in AMQP)
        :param mechanisms: Available security mechanisms
            A list of the security mechanisms that the server supports, delimited by spaces.
        :type mechanisms: binary type (longstr in AMQP)
        :param locales: Available message locales
            A list of the message locales that the server supports, delimited by spaces. The
            locale defines the language in which the server will send reply texts.
        :type locales: binary type (longstr in AMQP)
        """
        self.version_major = version_major
        self.version_minor = version_minor
        self.server_properties = server_properties
        self.mechanisms = mechanisms
        self.locales = locales

    def write_arguments(self, buf):
        enframe_table(buf, self.server_properties)
        buf.write(struct.pack('!BBI', self.version_major, self.version_minor, len(self.mechanisms)))
        buf.write(self.mechanisms)
        buf.write(struct.pack('!I', len(self.locales)))
        buf.write(self.locales)
        
    def get_size(self):
        return 10 + frame_table_size(self.server_properties) + len(self.mechanisms) + len(self.locales)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        version_major, version_minor, = struct.unpack_from('!BB', buf, offset)
        offset += 2
        server_properties, delta = deframe_table(buf, offset)
        offset += delta
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        mechanisms = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        locales = buf[offset:offset+s_len]
        offset += s_len
        return ConnectionStart(version_major, version_minor, server_properties, mechanisms, locales)


class ConnectionSecure(AMQPMethodPayload):
    """
    Security mechanism challenge
    
    The SASL protocol works by exchanging challenges and responses until both peers have
    received sufficient information to authenticate each other. This method challenges
    the client to provide more information.
    """
    NAME = u'connection.secure'

    INDEX = (10, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'challenge', u'longstr', u'longstr', reserved=False),
    ]

    def __init__(self, challenge):
        """
        Create frame connection.secure

        :param challenge: Security challenge data
            Challenge information, a block of opaque binary data passed to the security
            mechanism.
        :type challenge: binary type (longstr in AMQP)
        """
        self.challenge = challenge

    def write_arguments(self, buf):
        buf.write(struct.pack('!I', len(self.challenge)))
        buf.write(self.challenge)
        
    def get_size(self):
        return 4 + len(self.challenge)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        challenge = buf[offset:offset+s_len]
        offset += s_len
        return ConnectionSecure(challenge)


class ConnectionStartOk(AMQPMethodPayload):
    """
    Select security mechanism and locale
    
    This method selects a SASL security mechanism.
    """
    NAME = u'connection.start-ok'

    INDEX = (10, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'client-properties', u'peer-properties', u'table', reserved=False),
        Field(u'mechanism', u'shortstr', u'shortstr', reserved=False),
        Field(u'response', u'longstr', u'longstr', reserved=False),
        Field(u'locale', u'shortstr', u'shortstr', reserved=False),
    ]

    def __init__(self, client_properties, mechanism, response, locale):
        """
        Create frame connection.start-ok

        :param client_properties: Client properties
            The properties SHOULD contain at least these fields: "product", giving the name
            of the client product, "version", giving the name of the client version, "platform",
            giving the name of the operating system, "copyright", if appropriate, and
            "information", giving other general information.
        :type client_properties: table. See coolamqp.uplink.framing.field_table (peer-properties in AMQP)
        :param mechanism: Selected security mechanism
            A single security mechanisms selected by the client, which must be one of those
            specified by the server.
        :type mechanism: binary type (max length 255) (shortstr in AMQP)
        :param response: Security response data
            A block of opaque data passed to the security mechanism. The contents of this
            data are defined by the SASL security mechanism.
        :type response: binary type (longstr in AMQP)
        :param locale: Selected message locale
            A single message locale selected by the client, which must be one of those
            specified by the server.
        :type locale: binary type (max length 255) (shortstr in AMQP)
        """
        self.client_properties = client_properties
        self.mechanism = mechanism
        self.response = response
        self.locale = locale

    def write_arguments(self, buf):
        enframe_table(buf, self.client_properties)
        buf.write(struct.pack('!B', len(self.mechanism)))
        buf.write(self.mechanism)
        buf.write(struct.pack('!I', len(self.response)))
        buf.write(self.response)
        buf.write(struct.pack('!B', len(self.locale)))
        buf.write(self.locale)
        
    def get_size(self):
        return 6 + frame_table_size(self.client_properties) + len(self.mechanism) + len(self.response) + len(self.locale)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        client_properties, delta = deframe_table(buf, offset)
        offset += delta
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        mechanism = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        response = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        locale = buf[offset:offset+s_len]
        offset += s_len
        return ConnectionStartOk(client_properties, mechanism, response, locale)


class ConnectionSecureOk(AMQPMethodPayload):
    """
    Security mechanism response
    
    This method attempts to authenticate, passing a block of SASL data for the security
    mechanism at the server side.
    """
    NAME = u'connection.secure-ok'

    INDEX = (10, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'response', u'longstr', u'longstr', reserved=False),
    ]

    def __init__(self, response):
        """
        Create frame connection.secure-ok

        :param response: Security response data
            A block of opaque data passed to the security mechanism. The contents of this
            data are defined by the SASL security mechanism.
        :type response: binary type (longstr in AMQP)
        """
        self.response = response

    def write_arguments(self, buf):
        buf.write(struct.pack('!I', len(self.response)))
        buf.write(self.response)
        
    def get_size(self):
        return 4 + len(self.response)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        response = buf[offset:offset+s_len]
        offset += s_len
        return ConnectionSecureOk(response)


class ConnectionTune(AMQPMethodPayload):
    """
    Propose connection tuning parameters
    
    This method proposes a set of connection configuration values to the client. The
    client can accept and/or adjust these.
    """
    NAME = u'connection.tune'

    INDEX = (10, 30)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x1E'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'channel-max', u'short', u'short', reserved=False),
        Field(u'frame-max', u'long', u'long', reserved=False),
        Field(u'heartbeat', u'short', u'short', reserved=False),
    ]

    def __init__(self, channel_max, frame_max, heartbeat):
        """
        Create frame connection.tune

        :param channel_max: Proposed maximum channels
            Specifies highest channel number that the server permits.  Usable channel numbers
            are in the range 1..channel-max.  Zero indicates no specified limit.
        :type channel_max: int, 16 bit unsigned (short in AMQP)
        :param frame_max: Proposed maximum frame size
            The largest frame size that the server proposes for the connection, including
            frame header and end-byte.  The client can negotiate a lower value. Zero means
            that the server does not impose any specific limit but may reject very large
            frames if it cannot allocate resources for them.
        :type frame_max: int, 32 bit unsigned (long in AMQP)
        :param heartbeat: Desired heartbeat delay
            The delay, in seconds, of the connection heartbeat that the server wants.
            Zero means the server does not want a heartbeat.
        :type heartbeat: int, 16 bit unsigned (short in AMQP)
        """
        self.channel_max = channel_max
        self.frame_max = frame_max
        self.heartbeat = heartbeat

    def write_arguments(self, buf):
        buf.write(struct.pack('!HIH', self.channel_max, self.frame_max, self.heartbeat))
        
    def get_size(self):
        return 8

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        channel_max, frame_max, heartbeat, = struct.unpack_from('!HIH', buf, offset)
        offset += 8
        return ConnectionTune(channel_max, frame_max, heartbeat)


class ConnectionTuneOk(AMQPMethodPayload):
    """
    Negotiate connection tuning parameters
    
    This method sends the client's connection tuning parameters to the server.
    Certain fields are negotiated, others provide capability information.
    """
    NAME = u'connection.tune-ok'

    INDEX = (10, 31)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x0A\x00\x1F'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'channel-max', u'short', u'short', reserved=False),
        Field(u'frame-max', u'long', u'long', reserved=False),
        Field(u'heartbeat', u'short', u'short', reserved=False),
    ]

    def __init__(self, channel_max, frame_max, heartbeat):
        """
        Create frame connection.tune-ok

        :param channel_max: Negotiated maximum channels
            The maximum total number of channels that the client will use per connection.
        :type channel_max: int, 16 bit unsigned (short in AMQP)
        :param frame_max: Negotiated maximum frame size
            The largest frame size that the client and server will use for the connection.
            Zero means that the client does not impose any specific limit but may reject
            very large frames if it cannot allocate resources for them. Note that the
            frame-max limit applies principally to content frames, where large contents can
            be broken into frames of arbitrary size.
        :type frame_max: int, 32 bit unsigned (long in AMQP)
        :param heartbeat: Desired heartbeat delay
            The delay, in seconds, of the connection heartbeat that the client wants. Zero
            means the client does not want a heartbeat.
        :type heartbeat: int, 16 bit unsigned (short in AMQP)
        """
        self.channel_max = channel_max
        self.frame_max = frame_max
        self.heartbeat = heartbeat

    def write_arguments(self, buf):
        buf.write(struct.pack('!HIH', self.channel_max, self.frame_max, self.heartbeat))
        
    def get_size(self):
        return 8

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        channel_max, frame_max, heartbeat, = struct.unpack_from('!HIH', buf, offset)
        offset += 8
        return ConnectionTuneOk(channel_max, frame_max, heartbeat)


class Channel(AMQPClass):
    """
    The channel class provides methods for a client to establish a channel to a
    
    server and for both peers to operate the channel thereafter.
    """
    NAME = u'channel'
    INDEX = 20


class ChannelClose(AMQPMethodPayload):
    """
    Request a channel close
    
    This method indicates that the sender wants to close the channel. This may be due to
    internal conditions (e.g. a forced shut-down) or due to an error handling a specific
    method, i.e. an exception. When a close is due to an exception, the sender provides
    the class and method id of the method which caused the exception.
    """
    NAME = u'channel.close'

    INDEX = (20, 40)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x28'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reply-code', u'reply-code', u'short', reserved=False),
        Field(u'reply-text', u'reply-text', u'shortstr', reserved=False),
        Field(u'class-id', u'class-id', u'short', reserved=False),
        Field(u'method-id', u'method-id', u'short', reserved=False),
    ]

    def __init__(self, reply_code, reply_text, class_id, method_id):
        """
        Create frame channel.close

        :type reply_code: int, 16 bit unsigned (reply-code in AMQP)
        :type reply_text: binary type (max length 255) (reply-text in AMQP)
        :param class_id: Failing method class
            When the close is provoked by a method exception, this is the class of the
            method.
        :type class_id: int, 16 bit unsigned (class-id in AMQP)
        :param method_id: Failing method id
            When the close is provoked by a method exception, this is the ID of the method.
        :type method_id: int, 16 bit unsigned (method-id in AMQP)
        """
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.class_id = class_id
        self.method_id = method_id

    def write_arguments(self, buf):
        buf.write(struct.pack('!HB', self.reply_code, len(self.reply_text)))
        buf.write(self.reply_text)
        buf.write(struct.pack('!HH', self.class_id, self.method_id))
        
    def get_size(self):
        return 7 + len(self.reply_text)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        reply_code, s_len, = struct.unpack_from('!HB', buf, offset)
        offset += 3
        reply_text = buf[offset:offset+s_len]
        offset += s_len
        class_id, method_id, = struct.unpack_from('!HH', buf, offset)
        offset += 4
        return ChannelClose(reply_code, reply_text, class_id, method_id)


class ChannelCloseOk(AMQPMethodPayload):
    """
    Confirm a channel close
    
    This method confirms a Channel.Close method and tells the recipient that it is safe
    to release resources for the channel.
    """
    NAME = u'channel.close-ok'

    INDEX = (20, 41)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x29'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x14\x00\x29\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame channel.close-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return ChannelCloseOk()


class ChannelFlow(AMQPMethodPayload):
    """
    Enable/disable flow from peer
    
    This method asks the peer to pause or restart the flow of content data sent by
    a consumer. This is a simple flow-control mechanism that a peer can use to avoid
    overflowing its queues or otherwise finding itself receiving more messages than
    it can process. Note that this method is not intended for window control. It does
    not affect contents returned by Basic.Get-Ok methods.
    """
    NAME = u'channel.flow'

    INDEX = (20, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'active', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, active):
        """
        Create frame channel.flow

        :param active: Start/stop content frames
            If 1, the peer starts sending content frames. If 0, the peer stops sending
            content frames.
        :type active: bool (bit in AMQP)
        """
        self.active = active

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', (self.active << 0)))
        
    def get_size(self):
        return 1

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        active = bool(_bit >> 0)
        offset += 1
        return ChannelFlow(active)


class ChannelFlowOk(AMQPMethodPayload):
    """
    Confirm a flow method
    
    Confirms to the peer that a flow command was received and processed.
    """
    NAME = u'channel.flow-ok'

    INDEX = (20, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'active', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, active):
        """
        Create frame channel.flow-ok

        :param active: Current flow setting
            Confirms the setting of the processed flow method: 1 means the peer will start
            sending or continue to send content frames; 0 means it will not.
        :type active: bool (bit in AMQP)
        """
        self.active = active

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', (self.active << 0)))
        
    def get_size(self):
        return 1

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        active = bool(_bit >> 0)
        offset += 1
        return ChannelFlowOk(active)


class ChannelOpen(AMQPMethodPayload):
    """
    Open a channel for use
    
    This method opens a channel to the server.
    """
    NAME = u'channel.open'

    INDEX = (20, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x05\x00\x14\x00\x0A\x00\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'shortstr', u'shortstr', reserved=True),
    ]

    def __init__(self):
        """
        Create frame channel.open
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        offset += s_len # reserved field!
        return ChannelOpen()


class ChannelOpenOk(AMQPMethodPayload):
    """
    Signal that the channel is ready
    
    This method signals to the client that the channel is ready for use.
    """
    NAME = u'channel.open-ok'

    INDEX = (20, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x14\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x05\x00\x14\x00\x0B\x00\x00\x00\x00\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'longstr', u'longstr', reserved=True),
    ]

    def __init__(self):
        """
        Create frame channel.open-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!L', buf, offset)
        offset += 4
        offset += s_len # reserved field!
        return ChannelOpenOk()


class Exchange(AMQPClass):
    """
    Exchanges match and distribute messages across queues. exchanges can be configured in
    
    the server or declared at runtime.
    """
    NAME = u'exchange'
    INDEX = 40


class ExchangeDeclare(AMQPMethodPayload):
    """
    Verify exchange exists, create if needed
    
    This method creates an exchange if it does not already exist, and if the exchange
    exists, verifies that it is of the correct and expected class.
    """
    NAME = u'exchange.declare'

    INDEX = (40, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x28\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'type', u'shortstr', u'shortstr', reserved=False),
        Field(u'passive', u'bit', u'bit', reserved=False),
        Field(u'durable', u'bit', u'bit', reserved=False),
        Field(u'reserved-2', u'bit', u'bit', reserved=True),
        Field(u'reserved-3', u'bit', u'bit', reserved=True),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
        Field(u'arguments', u'table', u'table', reserved=False),
    ]

    def __init__(self, exchange, type_, passive, durable, no_wait, arguments):
        """
        Create frame exchange.declare

        :param exchange: Exchange names starting with "amq." are reserved for pre-declared and
            standardised exchanges. The client MAY declare an exchange starting with
            "amq." if the passive option is set, or the exchange already exists.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param type_: Exchange type
            Each exchange belongs to one of a set of exchange types implemented by the
            server. The exchange types define the functionality of the exchange - i.e. how
            messages are routed through it. It is not valid or meaningful to attempt to
            change the type of an existing exchange.
        :type type_: binary type (max length 255) (shortstr in AMQP)
        :param passive: Do not create exchange
            If set, the server will reply with Declare-Ok if the exchange already
            exists with the same name, and raise an error if not.  The client can
            use this to check whether an exchange exists without modifying the
            server state. When set, all other method fields except name and no-wait
            are ignored.  A declare with both passive and no-wait has no effect.
            Arguments are compared for semantic equivalence.
        :type passive: bool (bit in AMQP)
        :param durable: Request a durable exchange
            If set when creating a new exchange, the exchange will be marked as durable.
            Durable exchanges remain active when a server restarts. Non-durable exchanges
            (transient exchanges) are purged if/when a server restarts.
        :type durable: bool (bit in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        :param arguments: Arguments for declaration
            A set of arguments for the declaration. The syntax and semantics of these
            arguments depends on the server implementation.
        :type arguments: table. See coolamqp.uplink.framing.field_table (table in AMQP)
        """
        self.exchange = exchange
        self.type_ = type_
        self.passive = passive
        self.durable = durable
        self.no_wait = no_wait
        self.arguments = arguments

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.type_)))
        buf.write(self.type_)
        enframe_table(buf, self.arguments)
        buf.write(struct.pack('!B', (self.passive << 0) | (self.durable << 1) | (self.no_wait << 4)))
        
    def get_size(self):
        return 5 + len(self.exchange) + len(self.type_) + frame_table_size(self.arguments)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        type_ = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        passive = bool(_bit >> 0)
        durable = bool(_bit >> 1)
        no_wait = bool(_bit >> 4)
        offset += 1
        arguments, delta = deframe_table(buf, offset)
        offset += delta
        return ExchangeDeclare(exchange, type_, passive, durable, no_wait, arguments)


class ExchangeDelete(AMQPMethodPayload):
    """
    Delete an exchange
    
    This method deletes an exchange. When an exchange is deleted all queue bindings on
    the exchange are cancelled.
    """
    NAME = u'exchange.delete'

    INDEX = (40, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x28\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'if-unused', u'bit', u'bit', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
    ]

    def __init__(self, exchange, if_unused, no_wait):
        """
        Create frame exchange.delete

        :param exchange: The client must not attempt to delete an exchange that does not exist.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param if_unused: Delete only if unused
            If set, the server will only delete the exchange if it has no queue bindings. If
            the exchange has queue bindings the server does not delete it but raises a
            channel exception instead.
        :type if_unused: bool (bit in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        """
        self.exchange = exchange
        self.if_unused = if_unused
        self.no_wait = no_wait

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', (self.if_unused << 0) | (self.no_wait << 1)))
        
    def get_size(self):
        return 4 + len(self.exchange)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        exchange = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        if_unused = bool(_bit >> 0)
        no_wait = bool(_bit >> 1)
        offset += 1
        return ExchangeDelete(exchange, if_unused, no_wait)


class ExchangeDeclareOk(AMQPMethodPayload):
    """
    Confirm exchange declaration
    
    This method confirms a Declare method and confirms the name of the exchange,
    essential for automatically-named exchanges.
    """
    NAME = u'exchange.declare-ok'

    INDEX = (40, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x28\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x28\x00\x0B\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame exchange.declare-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return ExchangeDeclareOk()


class ExchangeDeleteOk(AMQPMethodPayload):
    """
    Confirm deletion of an exchange
    
    This method confirms the deletion of an exchange.
    """
    NAME = u'exchange.delete-ok'

    INDEX = (40, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x28\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x28\x00\x15\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame exchange.delete-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return ExchangeDeleteOk()


class Queue(AMQPClass):
    """
    Queues store and forward messages. queues can be configured in the server or created at
    
    runtime. Queues must be attached to at least one exchange in order to receive messages
    from publishers.
    """
    NAME = u'queue'
    INDEX = 50


class QueueBind(AMQPMethodPayload):
    """
    Bind queue to an exchange
    
    This method binds a queue to an exchange. Until a queue is bound it will not
    receive any messages. In a classic messaging model, store-and-forward queues
    are bound to a direct exchange and subscription queues are bound to a topic
    exchange.
    """
    NAME = u'queue.bind'

    INDEX = (50, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
        Field(u'arguments', u'table', u'table', reserved=False),
    ]

    def __init__(self, queue, exchange, routing_key, no_wait, arguments):
        """
        Create frame queue.bind

        :param queue: Specifies the name of the queue to bind.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :param exchange: Name of the exchange to bind to
            A client MUST NOT be allowed to bind a queue to a non-existent exchange.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Message routing key
            Specifies the routing key for the binding. The routing key is used for routing
            messages depending on the exchange configuration. Not all exchanges use a
            routing key - refer to the specific exchange documentation.  If the queue name
            is empty, the server uses the last queue declared on the channel.  If the
            routing key is also empty, the server uses this queue name for the routing
            key as well.  If the queue name is provided but the routing key is empty, the
            server does the binding with that empty routing key.  The meaning of empty
            routing keys depends on the exchange implementation.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        :param arguments: Arguments for binding
            A set of arguments for the binding. The syntax and semantics of these arguments
            depends on the exchange class.
        :type arguments: table. See coolamqp.uplink.framing.field_table (table in AMQP)
        """
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key
        self.no_wait = no_wait
        self.arguments = arguments

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        enframe_table(buf, self.arguments)
        buf.write(struct.pack('!B', (self.no_wait << 0)))
        
    def get_size(self):
        return 6 + len(self.queue) + len(self.exchange) + len(self.routing_key) + frame_table_size(self.arguments)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        no_wait = bool(_bit >> 0)
        offset += 1
        arguments, delta = deframe_table(buf, offset)
        offset += delta
        return QueueBind(queue, exchange, routing_key, no_wait, arguments)


class QueueBindOk(AMQPMethodPayload):
    """
    Confirm bind successful
    
    This method confirms that the bind was successful.
    """
    NAME = u'queue.bind-ok'

    INDEX = (50, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x32\x00\x15\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame queue.bind-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return QueueBindOk()


class QueueDeclare(AMQPMethodPayload):
    """
    Declare queue, create if needed
    
    This method creates or checks a queue. When creating a new queue the client can
    specify various properties that control the durability of the queue and its
    contents, and the level of sharing for the queue.
    """
    NAME = u'queue.declare'

    INDEX = (50, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'passive', u'bit', u'bit', reserved=False),
        Field(u'durable', u'bit', u'bit', reserved=False),
        Field(u'exclusive', u'bit', u'bit', reserved=False),
        Field(u'auto-delete', u'bit', u'bit', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
        Field(u'arguments', u'table', u'table', reserved=False),
    ]

    def __init__(self, queue, passive, durable, exclusive, auto_delete, no_wait, arguments):
        """
        Create frame queue.declare

        :param queue: The queue name may be empty, in which case the server must create a new
            queue with a unique generated name and return this to the client in the
            Declare-Ok method.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :param passive: Do not create queue
            If set, the server will reply with Declare-Ok if the queue already
            exists with the same name, and raise an error if not.  The client can
            use this to check whether a queue exists without modifying the
            server state.  When set, all other method fields except name and no-wait
            are ignored.  A declare with both passive and no-wait has no effect.
            Arguments are compared for semantic equivalence.
        :type passive: bool (bit in AMQP)
        :param durable: Request a durable queue
            If set when creating a new queue, the queue will be marked as durable. Durable
            queues remain active when a server restarts. Non-durable queues (transient
            queues) are purged if/when a server restarts. Note that durable queues do not
            necessarily hold persistent messages, although it does not make sense to send
            persistent messages to a transient queue.
        :type durable: bool (bit in AMQP)
        :param exclusive: Request an exclusive queue
            Exclusive queues may only be accessed by the current connection, and are
            deleted when that connection closes.  Passive declaration of an exclusive
            queue by other connections are not allowed.
        :type exclusive: bool (bit in AMQP)
        :param auto_delete: Auto-delete queue when unused
            If set, the queue is deleted when all consumers have finished using it.  The last
            consumer can be cancelled either explicitly or because its channel is closed. If
            there was no consumer ever on the queue, it won't be deleted.  Applications can
            explicitly delete auto-delete queues using the Delete method as normal.
        :type auto_delete: bool (bit in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        :param arguments: Arguments for declaration
            A set of arguments for the declaration. The syntax and semantics of these
            arguments depends on the server implementation.
        :type arguments: table. See coolamqp.uplink.framing.field_table (table in AMQP)
        """
        self.queue = queue
        self.passive = passive
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.no_wait = no_wait
        self.arguments = arguments

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        enframe_table(buf, self.arguments)
        buf.write(struct.pack('!B', (self.passive << 0) | (self.durable << 1) | (self.exclusive << 2) | (self.auto_delete << 3) | (self.no_wait << 4)))
        
    def get_size(self):
        return 4 + len(self.queue) + frame_table_size(self.arguments)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        passive = bool(_bit >> 0)
        durable = bool(_bit >> 1)
        exclusive = bool(_bit >> 2)
        auto_delete = bool(_bit >> 3)
        no_wait = bool(_bit >> 4)
        offset += 1
        arguments, delta = deframe_table(buf, offset)
        offset += delta
        return QueueDeclare(queue, passive, durable, exclusive, auto_delete, no_wait, arguments)


class QueueDelete(AMQPMethodPayload):
    """
    Delete a queue
    
    This method deletes a queue. When a queue is deleted any pending messages are sent
    to a dead-letter queue if this is defined in the server configuration, and all
    consumers on the queue are cancelled.
    """
    NAME = u'queue.delete'

    INDEX = (50, 40)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x28'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'if-unused', u'bit', u'bit', reserved=False),
        Field(u'if-empty', u'bit', u'bit', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
    ]

    def __init__(self, queue, if_unused, if_empty, no_wait):
        """
        Create frame queue.delete

        :param queue: Specifies the name of the queue to delete.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :param if_unused: Delete only if unused
            If set, the server will only delete the queue if it has no consumers. If the
            queue has consumers the server does does not delete it but raises a channel
            exception instead.
        :type if_unused: bool (bit in AMQP)
        :param if_empty: Delete only if empty
            If set, the server will only delete the queue if it has no messages.
        :type if_empty: bool (bit in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        """
        self.queue = queue
        self.if_unused = if_unused
        self.if_empty = if_empty
        self.no_wait = no_wait

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', (self.if_unused << 0) | (self.if_empty << 1) | (self.no_wait << 2)))
        
    def get_size(self):
        return 4 + len(self.queue)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        if_unused = bool(_bit >> 0)
        if_empty = bool(_bit >> 1)
        no_wait = bool(_bit >> 2)
        offset += 1
        return QueueDelete(queue, if_unused, if_empty, no_wait)


class QueueDeclareOk(AMQPMethodPayload):
    """
    Confirms a queue definition
    
    This method confirms a Declare method and confirms the name of the queue, essential
    for automatically-named queues.
    """
    NAME = u'queue.declare-ok'

    INDEX = (50, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'message-count', u'message-count', u'long', reserved=False),
        Field(u'consumer-count', u'long', u'long', reserved=False),
    ]

    def __init__(self, queue, message_count, consumer_count):
        """
        Create frame queue.declare-ok

        :param queue: Reports the name of the queue. if the server generated a queue name, this field
            contains that name.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :type message_count: int, 32 bit unsigned (message-count in AMQP)
        :param consumer_count: Number of consumers
            Reports the number of active consumers for the queue. Note that consumers can
            suspend activity (Channel.Flow) in which case they do not appear in this count.
        :type consumer_count: int, 32 bit unsigned (long in AMQP)
        """
        self.queue = queue
        self.message_count = message_count
        self.consumer_count = consumer_count

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!II', self.message_count, self.consumer_count))
        
    def get_size(self):
        return 9 + len(self.queue)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        queue = buf[offset:offset+s_len]
        offset += s_len
        message_count, consumer_count, = struct.unpack_from('!II', buf, offset)
        offset += 8
        return QueueDeclareOk(queue, message_count, consumer_count)


class QueueDeleteOk(AMQPMethodPayload):
    """
    Confirm deletion of a queue
    
    This method confirms the deletion of a queue.
    """
    NAME = u'queue.delete-ok'

    INDEX = (50, 41)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x29'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'message-count', u'message-count', u'long', reserved=False),
    ]

    def __init__(self, message_count):
        """
        Create frame queue.delete-ok

        :param message_count: Reports the number of messages deleted.
        :type message_count: int, 32 bit unsigned (message-count in AMQP)
        """
        self.message_count = message_count

    def write_arguments(self, buf):
        buf.write(struct.pack('!I', self.message_count))
        
    def get_size(self):
        return 4

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        message_count, = struct.unpack_from('!I', buf, offset)
        offset += 4
        return QueueDeleteOk(message_count)


class QueuePurge(AMQPMethodPayload):
    """
    Purge a queue
    
    This method removes all messages from a queue which are not awaiting
    acknowledgment.
    """
    NAME = u'queue.purge'

    INDEX = (50, 30)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x1E'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
    ]

    def __init__(self, queue, no_wait):
        """
        Create frame queue.purge

        :param queue: Specifies the name of the queue to purge.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        """
        self.queue = queue
        self.no_wait = no_wait

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', (self.no_wait << 0)))
        
    def get_size(self):
        return 4 + len(self.queue)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        no_wait = bool(_bit >> 0)
        offset += 1
        return QueuePurge(queue, no_wait)


class QueuePurgeOk(AMQPMethodPayload):
    """
    Confirms a queue purge
    
    This method confirms the purge of a queue.
    """
    NAME = u'queue.purge-ok'

    INDEX = (50, 31)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x1F'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'message-count', u'message-count', u'long', reserved=False),
    ]

    def __init__(self, message_count):
        """
        Create frame queue.purge-ok

        :param message_count: Reports the number of messages purged.
        :type message_count: int, 32 bit unsigned (message-count in AMQP)
        """
        self.message_count = message_count

    def write_arguments(self, buf):
        buf.write(struct.pack('!I', self.message_count))
        
    def get_size(self):
        return 4

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        message_count, = struct.unpack_from('!I', buf, offset)
        offset += 4
        return QueuePurgeOk(message_count)


class QueueUnbind(AMQPMethodPayload):
    """
    Unbind a queue from an exchange
    
    This method unbinds a queue from an exchange.
    """
    NAME = u'queue.unbind'

    INDEX = (50, 50)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x32'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
        Field(u'arguments', u'table', u'table', reserved=False),
    ]

    def __init__(self, queue, exchange, routing_key, arguments):
        """
        Create frame queue.unbind

        :param queue: Specifies the name of the queue to unbind.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :param exchange: The name of the exchange to unbind from.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Routing key of binding
            Specifies the routing key of the binding to unbind.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        :param arguments: Arguments of binding
            Specifies the arguments of the binding to unbind.
        :type arguments: table. See coolamqp.uplink.framing.field_table (table in AMQP)
        """
        self.queue = queue
        self.exchange = exchange
        self.routing_key = routing_key
        self.arguments = arguments

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        enframe_table(buf, self.arguments)
        
    def get_size(self):
        return 5 + len(self.queue) + len(self.exchange) + len(self.routing_key) + frame_table_size(self.arguments)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        arguments, delta = deframe_table(buf, offset)
        offset += delta
        return QueueUnbind(queue, exchange, routing_key, arguments)


class QueueUnbindOk(AMQPMethodPayload):
    """
    Confirm unbind successful
    
    This method confirms that the unbind was successful.
    """
    NAME = u'queue.unbind-ok'

    INDEX = (50, 51)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x32\x00\x33'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x32\x00\x33\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame queue.unbind-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return QueueUnbindOk()


class Basic(AMQPClass):
    """
    The basic class provides methods that support an industry-standard messaging model.
    """
    NAME = u'basic'
    INDEX = 60


class BasicContentPropertyList(AMQPContentPropertyList):
    """
    The basic class provides methods that support an industry-standard messaging model.
    """
    FIELDS = [
        Field(u'content-type', u'shortstr', u'shortstr', False),
        Field(u'content-encoding', u'shortstr', u'shortstr', False),
        Field(u'headers', u'table', u'table', False),
        Field(u'delivery-mode', u'octet', u'octet', False),
        Field(u'priority', u'octet', u'octet', False),
        Field(u'correlation-id', u'shortstr', u'shortstr', False),
        Field(u'reply-to', u'shortstr', u'shortstr', False),
        Field(u'expiration', u'shortstr', u'shortstr', False),
        Field(u'message-id', u'shortstr', u'shortstr', False),
        Field(u'timestamp', u'timestamp', u'timestamp', False),
        Field(u'type', u'shortstr', u'shortstr', False),
        Field(u'user-id', u'shortstr', u'shortstr', False),
        Field(u'app-id', u'shortstr', u'shortstr', False),
        Field(u'reserved', u'shortstr', u'shortstr', False),
    ]
    # A dictionary from a zero property list to a class typized with
    # some fields
    PARTICULAR_CLASSES = {}

    def __new__(self, **kwargs):
        """
        Return a property list.
        :param content_type: MIME content type
        :type content_type: binary type (max length 255) (AMQP as shortstr)
        :param content_encoding: MIME content encoding
        :type content_encoding: binary type (max length 255) (AMQP as shortstr)
        :param headers: message header field table
        :type headers: table. See coolamqp.uplink.framing.field_table (AMQP as table)
        :param delivery_mode: non-persistent (1) or persistent (2)
        :type delivery_mode: int, 8 bit unsigned (AMQP as octet)
        :param priority: message priority, 0 to 9
        :type priority: int, 8 bit unsigned (AMQP as octet)
        :param correlation_id: application correlation identifier
        :type correlation_id: binary type (max length 255) (AMQP as shortstr)
        :param reply_to: address to reply to
        :type reply_to: binary type (max length 255) (AMQP as shortstr)
        :param expiration: message expiration specification
        :type expiration: binary type (max length 255) (AMQP as shortstr)
        :param message_id: application message identifier
        :type message_id: binary type (max length 255) (AMQP as shortstr)
        :param timestamp: message timestamp
        :type timestamp: 64 bit signed POSIX timestamp (in seconds) (AMQP as timestamp)
        :param type_: message type name
        :type type_: binary type (max length 255) (AMQP as shortstr)
        :param user_id: creating user id
        :type user_id: binary type (max length 255) (AMQP as shortstr)
        :param app_id: creating application id
        :type app_id: binary type (max length 255) (AMQP as shortstr)
        :param reserved: reserved, must be empty
        :type reserved: binary type (max length 255) (AMQP as shortstr)
        """
        zpf = bytearray([
            (('content_type' in kwargs) << 7) | (('content_encoding' in kwargs) << 6) | (('headers' in kwargs) << 5) | (('delivery_mode' in kwargs) << 4) | (('priority' in kwargs) << 3) | (('correlation_id' in kwargs) << 2) | (('reply_to' in kwargs) << 1) | int('expiration' in kwargs),
            (('message_id' in kwargs) << 7) | (('timestamp' in kwargs) << 6) | (('type_' in kwargs) << 5) | (('user_id' in kwargs) << 4) | (('app_id' in kwargs) << 3) | (('reserved' in kwargs) << 2)
        ])
        zpf = six.binary_type(zpf)

        if zpf in BasicContentPropertyList.PARTICULAR_CLASSES:
            warnings.warn(u"""You could go faster.

        If you know in advance what properties you will be using, use typized constructors like

            # runs once
            my_type = BasicContentPropertyList.typize('content_type', 'content_encoding')
            # runs many times
            props = my_type('text/plain', 'utf8')

        instead of

            # runs many times
            props = BasicContentPropertyList(content_type='text/plain', content_encoding='utf8')

        This way you will be faster.

        If you do not know in advance what properties you will be using, it is correct to use
        this constructor.
        """)

            return BasicContentPropertyList.PARTICULAR_CLASSES[zpf](**kwargs)
        else:
            logger.debug('Property field (BasicContentPropertyList:%s) not seen yet, compiling', repr(zpf))
            c = compile_particular_content_property_list_class(zpf, BasicContentPropertyList.FIELDS)
            BasicContentPropertyList.PARTICULAR_CLASSES[zpf] = c
            return c(**kwargs)

    @staticmethod
    def typize(*fields):
        zpf = bytearray([
        (('content_type' in fields) << 7) | (('content_encoding' in fields) << 6) | (('headers' in fields) << 5) | (('delivery_mode' in fields) << 4) | (('priority' in fields) << 3) | (('correlation_id' in fields) << 2) | (('reply_to' in fields) << 1) | int('expiration' in kwargs),
        (('message_id' in fields) << 7) | (('timestamp' in fields) << 6) | (('type_' in fields) << 5) | (('user_id' in fields) << 4) | (('app_id' in fields) << 3) | (('reserved' in fields) << 2)
        ])
        zpf = six.binary_type(zpf)
        if zpf in BasicContentPropertyList.PARTICULAR_CLASSES:
            return BasicContentPropertyList.PARTICULAR_CLASSES[zpf]
        else:
            logger.debug('Property field (BasicContentPropertyList:%s) not seen yet, compiling', repr(zpf))
            c = compile_particular_content_property_list_class(zpf, BasicContentPropertyList.FIELDS)
            BasicContentPropertyList.PARTICULAR_CLASSES[zpf] = c
            return c

    @staticmethod
    def from_buffer(buf, offset):
        """
        Return a content property list instance unserialized from
        buffer, so that buf[offset] marks the start of property flags
        """
        # extract property flags
        pfl = 2
        while ord(buf[offset + pfl]) & 1:
            pfl += 2
        zpf = BasicContentPropertyList.zero_property_flags(buf[offset:offset+pfl])
        if zpf in BasicContentPropertyList.PARTICULAR_CLASSES:
            return BasicContentPropertyList.PARTICULAR_CLASSES[zpf].from_buffer(buf, offset)
        else:
            logger.debug('Property field (BasicContentPropertyList:%s) not seen yet, compiling', repr(zpf))
            c = compile_particular_content_property_list_class(zpf, BasicContentPropertyList.FIELDS)
            BasicContentPropertyList.PARTICULAR_CLASSES[zpf] = c
            return c.from_buffer(buf, offset)


class BasicAck(AMQPMethodPayload):
    """
    Acknowledge one or more messages
    
    This method acknowledges one or more messages delivered via the Deliver or Get-Ok
    methods. The client can ask to confirm a single message or a set of messages up to
    and including a specific message.
    """
    NAME = u'basic.ack'

    INDEX = (60, 80)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x50'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'delivery-tag', u'delivery-tag', u'longlong', reserved=False),
        Field(u'multiple', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, delivery_tag, multiple):
        """
        Create frame basic.ack

        :type delivery_tag: int, 64 bit unsigned (delivery-tag in AMQP)
        :param multiple: Acknowledge multiple messages
            If set to 1, the delivery tag is treated as "up to and including", so that the
            client can acknowledge multiple messages with a single method. If set to zero,
            the delivery tag refers to a single message. If the multiple field is 1, and the
            delivery tag is zero, tells the server to acknowledge all outstanding messages.
        :type multiple: bool (bit in AMQP)
        """
        self.delivery_tag = delivery_tag
        self.multiple = multiple

    def write_arguments(self, buf):
        buf.write(struct.pack('!QB', self.delivery_tag, (self.multiple << 0)))
        
    def get_size(self):
        return 9

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        multiple = bool(_bit >> 0)
        offset += 1
        delivery_tag, = struct.unpack_from('!Q', buf, offset)
        offset += 8
        return BasicAck(delivery_tag, multiple)


class BasicConsume(AMQPMethodPayload):
    """
    Start a queue consumer
    
    This method asks the server to start a "consumer", which is a transient request for
    messages from a specific queue. Consumers last as long as the channel they were
    declared on, or until the client cancels them.
    """
    NAME = u'basic.consume'

    INDEX = (60, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'consumer-tag', u'consumer-tag', u'shortstr', reserved=False),
        Field(u'no-local', u'no-local', u'bit', reserved=False),
        Field(u'no-ack', u'no-ack', u'bit', reserved=False),
        Field(u'exclusive', u'bit', u'bit', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
        Field(u'arguments', u'table', u'table', reserved=False),
    ]

    def __init__(self, queue, consumer_tag, no_local, no_ack, exclusive, no_wait, arguments):
        """
        Create frame basic.consume

        :param queue: Specifies the name of the queue to consume from.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :param consumer_tag: Specifies the identifier for the consumer. the consumer tag is local to a
            channel, so two clients can use the same consumer tags. If this field is
            empty the server will generate a unique tag.
        :type consumer_tag: binary type (max length 255) (consumer-tag in AMQP)
        :type no_local: bool (no-local in AMQP)
        :type no_ack: bool (no-ack in AMQP)
        :param exclusive: Request exclusive access
            Request exclusive consumer access, meaning only this consumer can access the
            queue.
        :type exclusive: bool (bit in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        :param arguments: Arguments for declaration
            A set of arguments for the consume. The syntax and semantics of these
            arguments depends on the server implementation.
        :type arguments: table. See coolamqp.uplink.framing.field_table (table in AMQP)
        """
        self.queue = queue
        self.consumer_tag = consumer_tag
        self.no_local = no_local
        self.no_ack = no_ack
        self.exclusive = exclusive
        self.no_wait = no_wait
        self.arguments = arguments

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', len(self.consumer_tag)))
        buf.write(self.consumer_tag)
        enframe_table(buf, self.arguments)
        buf.write(struct.pack('!B', (self.no_local << 0) | (self.no_ack << 1) | (self.exclusive << 2) | (self.no_wait << 3)))
        
    def get_size(self):
        return 5 + len(self.queue) + len(self.consumer_tag) + frame_table_size(self.arguments)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        consumer_tag = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        no_local = bool(_bit >> 0)
        no_ack = bool(_bit >> 1)
        exclusive = bool(_bit >> 2)
        no_wait = bool(_bit >> 3)
        offset += 1
        arguments, delta = deframe_table(buf, offset)
        offset += delta
        return BasicConsume(queue, consumer_tag, no_local, no_ack, exclusive, no_wait, arguments)


class BasicCancel(AMQPMethodPayload):
    """
    End a queue consumer
    
    This method cancels a consumer. This does not affect already delivered
    messages, but it does mean the server will not send any more messages for
    that consumer. The client may receive an arbitrary number of messages in
    between sending the cancel method and receiving the cancel-ok reply.
    """
    NAME = u'basic.cancel'

    INDEX = (60, 30)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x1E'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'consumer-tag', u'consumer-tag', u'shortstr', reserved=False),
        Field(u'no-wait', u'no-wait', u'bit', reserved=False),
    ]

    def __init__(self, consumer_tag, no_wait):
        """
        Create frame basic.cancel

        :type consumer_tag: binary type (max length 255) (consumer-tag in AMQP)
        :type no_wait: bool (no-wait in AMQP)
        """
        self.consumer_tag = consumer_tag
        self.no_wait = no_wait

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.consumer_tag)))
        buf.write(self.consumer_tag)
        buf.write(struct.pack('!B', (self.no_wait << 0)))
        
    def get_size(self):
        return 2 + len(self.consumer_tag)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        consumer_tag = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        no_wait = bool(_bit >> 0)
        offset += 1
        return BasicCancel(consumer_tag, no_wait)


class BasicConsumeOk(AMQPMethodPayload):
    """
    Confirm a new consumer
    
    The server provides the client with a consumer tag, which is used by the client
    for methods called on the consumer at a later stage.
    """
    NAME = u'basic.consume-ok'

    INDEX = (60, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'consumer-tag', u'consumer-tag', u'shortstr', reserved=False),
    ]

    def __init__(self, consumer_tag):
        """
        Create frame basic.consume-ok

        :param consumer_tag: Holds the consumer tag specified by the client or provided by the server.
        :type consumer_tag: binary type (max length 255) (consumer-tag in AMQP)
        """
        self.consumer_tag = consumer_tag

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.consumer_tag)))
        buf.write(self.consumer_tag)
        
    def get_size(self):
        return 1 + len(self.consumer_tag)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        consumer_tag = buf[offset:offset+s_len]
        offset += s_len
        return BasicConsumeOk(consumer_tag)


class BasicCancelOk(AMQPMethodPayload):
    """
    Confirm a cancelled consumer
    
    This method confirms that the cancellation was completed.
    """
    NAME = u'basic.cancel-ok'

    INDEX = (60, 31)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x1F'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'consumer-tag', u'consumer-tag', u'shortstr', reserved=False),
    ]

    def __init__(self, consumer_tag):
        """
        Create frame basic.cancel-ok

        :type consumer_tag: binary type (max length 255) (consumer-tag in AMQP)
        """
        self.consumer_tag = consumer_tag

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.consumer_tag)))
        buf.write(self.consumer_tag)
        
    def get_size(self):
        return 1 + len(self.consumer_tag)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        consumer_tag = buf[offset:offset+s_len]
        offset += s_len
        return BasicCancelOk(consumer_tag)


class BasicDeliver(AMQPMethodPayload):
    """
    Notify the client of a consumer message
    
    This method delivers a message to the client, via a consumer. In the asynchronous
    message delivery model, the client starts a consumer using the Consume method, then
    the server responds with Deliver methods as and when messages arrive for that
    consumer.
    """
    NAME = u'basic.deliver'

    INDEX = (60, 60)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x3C'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'consumer-tag', u'consumer-tag', u'shortstr', reserved=False),
        Field(u'delivery-tag', u'delivery-tag', u'longlong', reserved=False),
        Field(u'redelivered', u'redelivered', u'bit', reserved=False),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
    ]

    def __init__(self, consumer_tag, delivery_tag, redelivered, exchange, routing_key):
        """
        Create frame basic.deliver

        :type consumer_tag: binary type (max length 255) (consumer-tag in AMQP)
        :type delivery_tag: int, 64 bit unsigned (delivery-tag in AMQP)
        :type redelivered: bool (redelivered in AMQP)
        :param exchange: Specifies the name of the exchange that the message was originally published to.
            May be empty, indicating the default exchange.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Message routing key
            Specifies the routing key name specified when the message was published.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        """
        self.consumer_tag = consumer_tag
        self.delivery_tag = delivery_tag
        self.redelivered = redelivered
        self.exchange = exchange
        self.routing_key = routing_key

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', len(self.consumer_tag)))
        buf.write(self.consumer_tag)
        buf.write(struct.pack('!QBB', self.delivery_tag, (self.redelivered << 0), len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        
    def get_size(self):
        return 12 + len(self.consumer_tag) + len(self.exchange) + len(self.routing_key)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        consumer_tag = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        redelivered = bool(_bit >> 0)
        offset += 1
        delivery_tag, s_len, = struct.unpack_from('!QB', buf, offset)
        offset += 9
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        return BasicDeliver(consumer_tag, delivery_tag, redelivered, exchange, routing_key)


class BasicGet(AMQPMethodPayload):
    """
    Direct access to a queue
    
    This method provides a direct access to the messages in a queue using a synchronous
    dialogue that is designed for specific types of application where synchronous
    functionality is more important than performance.
    """
    NAME = u'basic.get'

    INDEX = (60, 70)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x46'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'queue', u'queue-name', u'shortstr', reserved=False),
        Field(u'no-ack', u'no-ack', u'bit', reserved=False),
    ]

    def __init__(self, queue, no_ack):
        """
        Create frame basic.get

        :param queue: Specifies the name of the queue to get a message from.
        :type queue: binary type (max length 255) (queue-name in AMQP)
        :type no_ack: bool (no-ack in AMQP)
        """
        self.queue = queue
        self.no_ack = no_ack

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.queue)))
        buf.write(self.queue)
        buf.write(struct.pack('!B', (self.no_ack << 0)))
        
    def get_size(self):
        return 4 + len(self.queue)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        queue = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        no_ack = bool(_bit >> 0)
        offset += 1
        return BasicGet(queue, no_ack)


class BasicGetOk(AMQPMethodPayload):
    """
    Provide client with a message
    
    This method delivers a message to the client following a get method. A message
    delivered by 'get-ok' must be acknowledged unless the no-ack option was set in the
    get method.
    """
    NAME = u'basic.get-ok'

    INDEX = (60, 71)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x47'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'delivery-tag', u'delivery-tag', u'longlong', reserved=False),
        Field(u'redelivered', u'redelivered', u'bit', reserved=False),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
        Field(u'message-count', u'message-count', u'long', reserved=False),
    ]

    def __init__(self, delivery_tag, redelivered, exchange, routing_key, message_count):
        """
        Create frame basic.get-ok

        :type delivery_tag: int, 64 bit unsigned (delivery-tag in AMQP)
        :type redelivered: bool (redelivered in AMQP)
        :param exchange: Specifies the name of the exchange that the message was originally published to.
            If empty, the message was published to the default exchange.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Message routing key
            Specifies the routing key name specified when the message was published.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        :type message_count: int, 32 bit unsigned (message-count in AMQP)
        """
        self.delivery_tag = delivery_tag
        self.redelivered = redelivered
        self.exchange = exchange
        self.routing_key = routing_key
        self.message_count = message_count

    def write_arguments(self, buf):
        buf.write(struct.pack('!QBB', self.delivery_tag, (self.redelivered << 0), len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        buf.write(struct.pack('!I', self.message_count))
        
    def get_size(self):
        return 15 + len(self.exchange) + len(self.routing_key)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        redelivered = bool(_bit >> 0)
        offset += 1
        delivery_tag, s_len, = struct.unpack_from('!QB', buf, offset)
        offset += 9
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        message_count, = struct.unpack_from('!I', buf, offset)
        offset += 4
        return BasicGetOk(delivery_tag, redelivered, exchange, routing_key, message_count)


class BasicGetEmpty(AMQPMethodPayload):
    """
    Indicate no messages available
    
    This method tells the client that the queue has no messages available for the
    client.
    """
    NAME = u'basic.get-empty'

    INDEX = (60, 72)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x48'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x0D\x00\x3C\x00\x48\x00\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'shortstr', u'shortstr', reserved=True),
    ]

    def __init__(self):
        """
        Create frame basic.get-empty
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        offset += s_len # reserved field!
        return BasicGetEmpty()


class BasicPublish(AMQPMethodPayload):
    """
    Publish a message
    
    This method publishes a message to a specific exchange. The message will be routed
    to queues as defined by the exchange configuration and distributed to any active
    consumers when the transaction, if any, is committed.
    """
    NAME = u'basic.publish'

    INDEX = (60, 40)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x28'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reserved-1', u'short', u'short', reserved=True),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
        Field(u'mandatory', u'bit', u'bit', reserved=False),
        Field(u'immediate', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, exchange, routing_key, mandatory, immediate):
        """
        Create frame basic.publish

        :param exchange: Specifies the name of the exchange to publish to. the exchange name can be
            empty, meaning the default exchange. If the exchange name is specified, and that
            exchange does not exist, the server will raise a channel exception.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Message routing key
            Specifies the routing key for the message. The routing key is used for routing
            messages depending on the exchange configuration.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        :param mandatory: Indicate mandatory routing
            This flag tells the server how to react if the message cannot be routed to a
            queue. If this flag is set, the server will return an unroutable message with a
            Return method. If this flag is zero, the server silently drops the message.
        :type mandatory: bool (bit in AMQP)
        :param immediate: Request immediate delivery
            This flag tells the server how to react if the message cannot be routed to a
            queue consumer immediately. If this flag is set, the server will return an
            undeliverable message with a Return method. If this flag is zero, the server
            will queue the message, but with no guarantee that it will ever be consumed.
        :type immediate: bool (bit in AMQP)
        """
        self.exchange = exchange
        self.routing_key = routing_key
        self.mandatory = mandatory
        self.immediate = immediate

    def write_arguments(self, buf):
        buf.write(b'\x00\x00')
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        buf.write(struct.pack('!B', (self.mandatory << 0) | (self.immediate << 1)))
        
    def get_size(self):
        return 5 + len(self.exchange) + len(self.routing_key)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        s_len, = struct.unpack_from('!2xB', buf, offset)
        offset += 3
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        _bit, = struct.unpack_from('!B', buf, offset)
        mandatory = bool(_bit >> 0)
        immediate = bool(_bit >> 1)
        offset += 1
        return BasicPublish(exchange, routing_key, mandatory, immediate)


class BasicQos(AMQPMethodPayload):
    """
    Specify quality of service
    
    This method requests a specific quality of service. The QoS can be specified for the
    current channel or for all channels on the connection. The particular properties and
    semantics of a qos method always depend on the content class semantics. Though the
    qos method could in principle apply to both peers, it is currently meaningful only
    for the server.
    """
    NAME = u'basic.qos'

    INDEX = (60, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'prefetch-size', u'long', u'long', reserved=False),
        Field(u'prefetch-count', u'short', u'short', reserved=False),
        Field(u'global', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, prefetch_size, prefetch_count, global_):
        """
        Create frame basic.qos

        :param prefetch_size: Prefetch window in octets
            The client can request that messages be sent in advance so that when the client
            finishes processing a message, the following message is already held locally,
            rather than needing to be sent down the channel. Prefetching gives a performance
            improvement. This field specifies the prefetch window size in octets. The server
            will send a message in advance if it is equal to or smaller in size than the
            available prefetch size (and also falls into other prefetch limits). May be set
            to zero, meaning "no specific limit", although other prefetch limits may still
            apply. The prefetch-size is ignored if the no-ack option is set.
        :type prefetch_size: int, 32 bit unsigned (long in AMQP)
        :param prefetch_count: Prefetch window in messages
            Specifies a prefetch window in terms of whole messages. This field may be used
            in combination with the prefetch-size field; a message will only be sent in
            advance if both prefetch windows (and those at the channel and connection level)
            allow it. The prefetch-count is ignored if the no-ack option is set.
        :type prefetch_count: int, 16 bit unsigned (short in AMQP)
        :param global_: Apply to entire connection
            By default the QoS settings apply to the current channel only. If this field is
            set, they are applied to the entire connection.
        :type global_: bool (bit in AMQP)
        """
        self.prefetch_size = prefetch_size
        self.prefetch_count = prefetch_count
        self.global_ = global_

    def write_arguments(self, buf):
        buf.write(struct.pack('!IHB', self.prefetch_size, self.prefetch_count, (self.global_ << 0)))
        
    def get_size(self):
        return 7

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        global_ = bool(_bit >> 0)
        offset += 1
        prefetch_size, prefetch_count, = struct.unpack_from('!IH', buf, offset)
        offset += 6
        return BasicQos(prefetch_size, prefetch_count, global_)


class BasicQosOk(AMQPMethodPayload):
    """
    Confirm the requested qos
    
    This method tells the client that the requested QoS levels could be handled by the
    server. The requested QoS applies to all active consumers until a new QoS is
    defined.
    """
    NAME = u'basic.qos-ok'

    INDEX = (60, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x3C\x00\x0B\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame basic.qos-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return BasicQosOk()


class BasicReturn(AMQPMethodPayload):
    """
    Return a failed message
    
    This method returns an undeliverable message that was published with the "immediate"
    flag set, or an unroutable message published with the "mandatory" flag set. The
    reply code and text provide information about the reason that the message was
    undeliverable.
    """
    NAME = u'basic.return'

    INDEX = (60, 50)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x32'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = False     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'reply-code', u'reply-code', u'short', reserved=False),
        Field(u'reply-text', u'reply-text', u'shortstr', reserved=False),
        Field(u'exchange', u'exchange-name', u'shortstr', reserved=False),
        Field(u'routing-key', u'shortstr', u'shortstr', reserved=False),
    ]

    def __init__(self, reply_code, reply_text, exchange, routing_key):
        """
        Create frame basic.return

        :type reply_code: int, 16 bit unsigned (reply-code in AMQP)
        :type reply_text: binary type (max length 255) (reply-text in AMQP)
        :param exchange: Specifies the name of the exchange that the message was originally published
            to.  May be empty, meaning the default exchange.
        :type exchange: binary type (max length 255) (exchange-name in AMQP)
        :param routing_key: Message routing key
            Specifies the routing key name specified when the message was published.
        :type routing_key: binary type (max length 255) (shortstr in AMQP)
        """
        self.reply_code = reply_code
        self.reply_text = reply_text
        self.exchange = exchange
        self.routing_key = routing_key

    def write_arguments(self, buf):
        buf.write(struct.pack('!HB', self.reply_code, len(self.reply_text)))
        buf.write(self.reply_text)
        buf.write(struct.pack('!B', len(self.exchange)))
        buf.write(self.exchange)
        buf.write(struct.pack('!B', len(self.routing_key)))
        buf.write(self.routing_key)
        
    def get_size(self):
        return 5 + len(self.reply_text) + len(self.exchange) + len(self.routing_key)

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        reply_code, s_len, = struct.unpack_from('!HB', buf, offset)
        offset += 3
        reply_text = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        exchange = buf[offset:offset+s_len]
        offset += s_len
        s_len, = struct.unpack_from('!B', buf, offset)
        offset += 1
        routing_key = buf[offset:offset+s_len]
        offset += s_len
        return BasicReturn(reply_code, reply_text, exchange, routing_key)


class BasicReject(AMQPMethodPayload):
    """
    Reject an incoming message
    
    This method allows a client to reject a message. It can be used to interrupt and
    cancel large incoming messages, or return untreatable messages to their original
    queue.
    """
    NAME = u'basic.reject'

    INDEX = (60, 90)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x5A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'delivery-tag', u'delivery-tag', u'longlong', reserved=False),
        Field(u'requeue', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, delivery_tag, requeue):
        """
        Create frame basic.reject

        :type delivery_tag: int, 64 bit unsigned (delivery-tag in AMQP)
        :param requeue: Requeue the message
            If requeue is true, the server will attempt to requeue the message.  If requeue
            is false or the requeue  attempt fails the messages are discarded or dead-lettered.
        :type requeue: bool (bit in AMQP)
        """
        self.delivery_tag = delivery_tag
        self.requeue = requeue

    def write_arguments(self, buf):
        buf.write(struct.pack('!QB', self.delivery_tag, (self.requeue << 0)))
        
    def get_size(self):
        return 9

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        requeue = bool(_bit >> 0)
        offset += 1
        delivery_tag, = struct.unpack_from('!Q', buf, offset)
        offset += 8
        return BasicReject(delivery_tag, requeue)


class BasicRecoverAsync(AMQPMethodPayload):
    """
    Redeliver unacknowledged messages
    
    This method asks the server to redeliver all unacknowledged messages on a
    specified channel. Zero or more messages may be redelivered.  This method
    is deprecated in favour of the synchronous Recover/Recover-Ok.
    """
    NAME = u'basic.recover-async'

    INDEX = (60, 100)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x64'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'requeue', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, requeue):
        """
        Create frame basic.recover-async

        :param requeue: Requeue the message
            If this field is zero, the message will be redelivered to the original
            recipient. If this bit is 1, the server will attempt to requeue the message,
            potentially then delivering it to an alternative subscriber.
        :type requeue: bool (bit in AMQP)
        """
        self.requeue = requeue

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', (self.requeue << 0)))
        
    def get_size(self):
        return 1

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        requeue = bool(_bit >> 0)
        offset += 1
        return BasicRecoverAsync(requeue)


class BasicRecover(AMQPMethodPayload):
    """
    Redeliver unacknowledged messages
    
    This method asks the server to redeliver all unacknowledged messages on a
    specified channel. Zero or more messages may be redelivered.  This method
    replaces the asynchronous Recover.
    """
    NAME = u'basic.recover'

    INDEX = (60, 110)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x6E'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = False  # this means that argument part has always the same content

    # See constructor pydoc for details
    FIELDS = [ 
        Field(u'requeue', u'bit', u'bit', reserved=False),
    ]

    def __init__(self, requeue):
        """
        Create frame basic.recover

        :param requeue: Requeue the message
            If this field is zero, the message will be redelivered to the original
            recipient. If this bit is 1, the server will attempt to requeue the message,
            potentially then delivering it to an alternative subscriber.
        :type requeue: bool (bit in AMQP)
        """
        self.requeue = requeue

    def write_arguments(self, buf):
        buf.write(struct.pack('!B', (self.requeue << 0)))
        
    def get_size(self):
        return 1

    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        _bit, = struct.unpack_from('!B', buf, offset)
        requeue = bool(_bit >> 0)
        offset += 1
        return BasicRecover(requeue)


class BasicRecoverOk(AMQPMethodPayload):
    """
    Confirm recovery
    
    This method acknowledges a Basic.Recover method.
    """
    NAME = u'basic.recover-ok'

    INDEX = (60, 111)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x3C\x00\x6F'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x3C\x00\x6F\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame basic.recover-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return BasicRecoverOk()


class Tx(AMQPClass):
    """
    The tx class allows publish and ack operations to be batched into atomic
    
    units of work.  The intention is that all publish and ack requests issued
    within a transaction will complete successfully or none of them will.
    Servers SHOULD implement atomic transactions at least where all publish
    or ack requests affect a single queue.  Transactions that cover multiple
    queues may be non-atomic, given that queues can be created and destroyed
    asynchronously, and such events do not form part of any transaction.
    Further, the behaviour of transactions with respect to the immediate and
    mandatory flags on Basic.Publish methods is not defined.
    """
    NAME = u'tx'
    INDEX = 90


class TxCommit(AMQPMethodPayload):
    """
    Commit the current transaction
    
    This method commits all message publications and acknowledgments performed in
    the current transaction.  A new transaction starts immediately after a commit.
    """
    NAME = u'tx.commit'

    INDEX = (90, 20)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x14'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x14\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.commit
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxCommit()


class TxCommitOk(AMQPMethodPayload):
    """
    Confirm a successful commit
    
    This method confirms to the client that the commit succeeded. Note that if a commit
    fails, the server raises a channel exception.
    """
    NAME = u'tx.commit-ok'

    INDEX = (90, 21)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x15'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x15\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.commit-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxCommitOk()


class TxRollback(AMQPMethodPayload):
    """
    Abandon the current transaction
    
    This method abandons all message publications and acknowledgments performed in
    the current transaction. A new transaction starts immediately after a rollback.
    Note that unacked messages will not be automatically redelivered by rollback;
    if that is required an explicit recover call should be issued.
    """
    NAME = u'tx.rollback'

    INDEX = (90, 30)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x1E'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x1E\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.rollback
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxRollback()


class TxRollbackOk(AMQPMethodPayload):
    """
    Confirm successful rollback
    
    This method confirms to the client that the rollback succeeded. Note that if an
    rollback fails, the server raises a channel exception.
    """
    NAME = u'tx.rollback-ok'

    INDEX = (90, 31)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x1F'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x1F\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.rollback-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxRollbackOk()


class TxSelect(AMQPMethodPayload):
    """
    Select standard transaction mode
    
    This method sets the channel to use standard transactions. The client must use this
    method at least once on a channel before using the Commit or Rollback methods.
    """
    NAME = u'tx.select'

    INDEX = (90, 10)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x0A'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = True, False

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x0A\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.select
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxSelect()


class TxSelectOk(AMQPMethodPayload):
    """
    Confirm transaction mode
    
    This method confirms to the client that the channel was successfully set to use
    standard transactions.
    """
    NAME = u'tx.select-ok'

    INDEX = (90, 11)          # (Class ID, Method ID)
    BINARY_HEADER = b'\x00\x5A\x00\x0B'      # CLASS ID + METHOD ID

    SENT_BY_CLIENT, SENT_BY_SERVER = False, True

    IS_SIZE_STATIC = True     # this means that argument part has always the same length
    IS_CONTENT_STATIC = True  # this means that argument part has always the same content
    STATIC_CONTENT = b'\x00\x00\x00\x04\x00\x5A\x00\x0B\xCE'  # spans LENGTH, CLASS ID, METHOD ID, ....., FRAME_END

    def __init__(self):
        """
        Create frame tx.select-ok
        """


    @staticmethod
    def from_buffer(buf, start_offset):
        offset = start_offset
        return TxSelectOk()


IDENT_TO_METHOD = {
    (90, 21): TxCommitOk,
    (60, 100): BasicRecoverAsync,
    (10, 11): ConnectionStartOk,
    (60, 40): BasicPublish,
    (60, 50): BasicReturn,
    (10, 51): ConnectionCloseOk,
    (20, 20): ChannelFlow,
    (60, 21): BasicConsumeOk,
    (10, 21): ConnectionSecureOk,
    (90, 30): TxRollback,
    (90, 10): TxSelect,
    (50, 11): QueueDeclareOk,
    (60, 70): BasicGet,
    (90, 11): TxSelectOk,
    (10, 30): ConnectionTune,
    (60, 11): BasicQosOk,
    (60, 80): BasicAck,
    (20, 21): ChannelFlowOk,
    (60, 60): BasicDeliver,
    (90, 31): TxRollbackOk,
    (20, 40): ChannelClose,
    (60, 71): BasicGetOk,
    (50, 30): QueuePurge,
    (10, 31): ConnectionTuneOk,
    (10, 40): ConnectionOpen,
    (60, 30): BasicCancel,
    (50, 50): QueueUnbind,
    (40, 10): ExchangeDeclare,
    (10, 50): ConnectionClose,
    (20, 10): ChannelOpen,
    (20, 41): ChannelCloseOk,
    (60, 110): BasicRecover,
    (60, 90): BasicReject,
    (50, 31): QueuePurgeOk,
    (50, 40): QueueDelete,
    (40, 20): ExchangeDelete,
    (50, 20): QueueBind,
    (10, 41): ConnectionOpenOk,
    (60, 31): BasicCancelOk,
    (90, 20): TxCommit,
    (10, 10): ConnectionStart,
    (60, 10): BasicQos,
    (40, 11): ExchangeDeclareOk,
    (40, 21): ExchangeDeleteOk,
    (20, 11): ChannelOpenOk,
    (60, 72): BasicGetEmpty,
    (60, 111): BasicRecoverOk,
    (60, 20): BasicConsume,
    (10, 20): ConnectionSecure,
    (50, 41): QueueDeleteOk,
    (50, 51): QueueUnbindOk,
    (50, 21): QueueBindOk,
    (50, 10): QueueDeclare,
}


BINARY_HEADER_TO_METHOD = {
    b'\x00\x5A\x00\x15': TxCommitOk,
    b'\x00\x3C\x00\x64': BasicRecoverAsync,
    b'\x00\x0A\x00\x0B': ConnectionStartOk,
    b'\x00\x3C\x00\x28': BasicPublish,
    b'\x00\x3C\x00\x32': BasicReturn,
    b'\x00\x0A\x00\x33': ConnectionCloseOk,
    b'\x00\x14\x00\x14': ChannelFlow,
    b'\x00\x3C\x00\x15': BasicConsumeOk,
    b'\x00\x0A\x00\x15': ConnectionSecureOk,
    b'\x00\x5A\x00\x1E': TxRollback,
    b'\x00\x5A\x00\x0A': TxSelect,
    b'\x00\x32\x00\x0B': QueueDeclareOk,
    b'\x00\x3C\x00\x46': BasicGet,
    b'\x00\x5A\x00\x0B': TxSelectOk,
    b'\x00\x0A\x00\x1E': ConnectionTune,
    b'\x00\x3C\x00\x0B': BasicQosOk,
    b'\x00\x3C\x00\x50': BasicAck,
    b'\x00\x14\x00\x15': ChannelFlowOk,
    b'\x00\x3C\x00\x3C': BasicDeliver,
    b'\x00\x5A\x00\x1F': TxRollbackOk,
    b'\x00\x14\x00\x28': ChannelClose,
    b'\x00\x3C\x00\x47': BasicGetOk,
    b'\x00\x32\x00\x1E': QueuePurge,
    b'\x00\x0A\x00\x1F': ConnectionTuneOk,
    b'\x00\x0A\x00\x28': ConnectionOpen,
    b'\x00\x3C\x00\x1E': BasicCancel,
    b'\x00\x32\x00\x32': QueueUnbind,
    b'\x00\x28\x00\x0A': ExchangeDeclare,
    b'\x00\x0A\x00\x32': ConnectionClose,
    b'\x00\x14\x00\x0A': ChannelOpen,
    b'\x00\x14\x00\x29': ChannelCloseOk,
    b'\x00\x3C\x00\x6E': BasicRecover,
    b'\x00\x3C\x00\x5A': BasicReject,
    b'\x00\x32\x00\x1F': QueuePurgeOk,
    b'\x00\x32\x00\x28': QueueDelete,
    b'\x00\x28\x00\x14': ExchangeDelete,
    b'\x00\x32\x00\x14': QueueBind,
    b'\x00\x0A\x00\x29': ConnectionOpenOk,
    b'\x00\x3C\x00\x1F': BasicCancelOk,
    b'\x00\x5A\x00\x14': TxCommit,
    b'\x00\x0A\x00\x0A': ConnectionStart,
    b'\x00\x3C\x00\x0A': BasicQos,
    b'\x00\x28\x00\x0B': ExchangeDeclareOk,
    b'\x00\x28\x00\x15': ExchangeDeleteOk,
    b'\x00\x14\x00\x0B': ChannelOpenOk,
    b'\x00\x3C\x00\x48': BasicGetEmpty,
    b'\x00\x3C\x00\x6F': BasicRecoverOk,
    b'\x00\x3C\x00\x14': BasicConsume,
    b'\x00\x0A\x00\x14': ConnectionSecure,
    b'\x00\x32\x00\x29': QueueDeleteOk,
    b'\x00\x32\x00\x33': QueueUnbindOk,
    b'\x00\x32\x00\x15': QueueBindOk,
    b'\x00\x32\x00\x0A': QueueDeclare,
}


CLASS_ID_TO_CONTENT_PROPERTY_LIST = {
    60: BasicContentPropertyList,
}

# Methods that are sent as replies to other methods, ie. ConnectionOpenOk: ConnectionOpen
# if a method is NOT a reply, it will not be in this dict
# a method may be a reply for AT MOST one method
REPLY_REASONS_FOR = {
    BasicGetEmpty: BasicGet,
    BasicGetOk: BasicGet,
    ExchangeDeleteOk: ExchangeDelete,
    TxSelectOk: TxSelect,
    QueueBindOk: QueueBind,
    BasicConsumeOk: BasicConsume,
    BasicCancelOk: BasicCancel,
    TxRollbackOk: TxRollback,
    ChannelOpenOk: ChannelOpen,
    QueueDeleteOk: QueueDelete,
    ChannelCloseOk: ChannelClose,
    BasicQosOk: BasicQos,
    ConnectionStartOk: ConnectionStart,
    QueueUnbindOk: QueueUnbind,
    TxCommitOk: TxCommit,
    QueuePurgeOk: QueuePurge,
    QueueDeclareOk: QueueDeclare,
    ExchangeDeclareOk: ExchangeDeclare,
    ConnectionTuneOk: ConnectionTune,
    ConnectionSecureOk: ConnectionSecure,
    ConnectionOpenOk: ConnectionOpen,
    ChannelFlowOk: ChannelFlow,
    ConnectionCloseOk: ConnectionClose,
}

# Methods that are replies for other, ie. ConnectionOpenOk: ConnectionOpen
# a method may be a reply for ONE or NONE other methods
# if a method has no replies, it will have an empty list as value here
REPLIES_FOR= {
    BasicGetEmpty: [],
    BasicRecoverOk: [],
    BasicReturn: [],
    QueueDeclare: [QueueDeclareOk],
    BasicGetOk: [],
    ConnectionSecure: [ConnectionSecureOk],
    ExchangeDeleteOk: [],
    TxRollback: [TxRollbackOk],
    TxSelectOk: [],
    QueueBindOk: [],
    ChannelFlow: [ChannelFlowOk],
    BasicConsumeOk: [],
    BasicRecover: [],
    BasicCancelOk: [],
    BasicGet: [BasicGetOk, BasicGetEmpty],
    TxRollbackOk: [],
    BasicAck: [],
    ExchangeDelete: [ExchangeDeleteOk],
    BasicConsume: [BasicConsumeOk],
    ConnectionClose: [ConnectionCloseOk],
    ChannelOpenOk: [],
    QueueDeleteOk: [],
    QueueBind: [QueueBindOk],
    ConnectionStart: [ConnectionStartOk],
    BasicQos: [BasicQosOk],
    QueueUnbind: [QueueUnbindOk],
    BasicQosOk: [],
    BasicReject: [],
    ChannelCloseOk: [],
    ExchangeDeclare: [ExchangeDeclareOk],
    BasicPublish: [],
    ConnectionTune: [ConnectionTuneOk],
    ConnectionStartOk: [],
    QueueUnbindOk: [],
    QueueDelete: [QueueDeleteOk],
    ConnectionCloseOk: [],
    QueuePurge: [QueuePurgeOk],
    ChannelOpen: [ChannelOpenOk],
    ChannelClose: [ChannelCloseOk],
    QueuePurgeOk: [],
    QueueDeclareOk: [],
    BasicCancel: [BasicCancelOk],
    ExchangeDeclareOk: [],
    TxCommitOk: [],
    ConnectionTuneOk: [],
    ConnectionSecureOk: [],
    ConnectionOpenOk: [],
    ChannelFlowOk: [],
    BasicRecoverAsync: [],
    TxSelect: [TxSelectOk],
    BasicDeliver: [],
    TxCommit: [TxCommitOk],
    ConnectionOpen: [ConnectionOpenOk],
}
