import json

from zope.interface import implements
from twisted.internet import reactor, protocol

from twisted.web import iweb, client, http_headers
from twisted.internet import defer


class _StringProducer(object):
    implements(iweb.IBodyProducer)

    def __init__(self, body):
        self.body = body
        self.length = len(body)

    def startProducing(self, consumer):
        consumer.write(self.body)
        return defer.succeed(None)

    def pauseProducing(self):
        pass

    def stopProducing(self):
        pass


def _request(url, values={}, headers={}, method='POST'):
    agent = client.Agent(reactor)
    data = json.dumps(values)

    d = agent.request(method,
                      url,
                      http_headers.Headers(headers),
                      _StringProducer(data) if data else None)

    def handle_response(response):
        if response.code == 204:
            d = defer.succeed('')
        else:
            d = defer.Deferred()
            response.deliverBody(SimpleReceiver(d))
        return d

    d.addCallback(handle_response)
    return d


class SimpleReceiver(protocol.Protocol):

    def __init__(s, d):
        s.buf = ''
        s.d = d

    def dataReceived(s, data):
        s.buf += data

    def connectionLost(s, reason):
        # TODO: test if reason is twisted.web.client.ResponseDone,
        # if not, do an errback
        s.d.callback(s.buf)


class DucksBoard(object):
    """
    I manage the connection details to Ducksboard.
    """

    URL = 'https://push.ducksboard.com/values'

    def __init__(self, key, auth):
        self._key = key
        self._auth = str(auth)

    def post(self, wid, data):
        d = _request(
            "%s/%d" % (self.URL, wid),
            data,
            headers={
                'Content-Type': ['application/json'],
                'Authorization': [self._auth]})
        return d
