#!/usr/bin/python

import sys

from twistduck import base, widgets

from twisted.internet import reactor
from twisted.internet import defer

if __name__ == '__main__':
    # FIXME: implement basic auth
    API_KEY = None
    AUTH = open('auth').readline().strip()

    db = base.DucksBoard(key=API_KEY, auth=AUTH)

    dtl = widgets.TimeLine(db, 21278)
    dtt = widgets.CustomCounterTrend(db, 27499)

    d = defer.Deferred()

    def timeline(_):
        return dtl.send(
            title="hi",
            content="Some details about my error message",
            image="https://dashboard.ducksboard.com/static/img/timeline/red.gif")

    def trend(_):
        return dtt.send(150)

    def cb(res):
        print res

    def stop(_):
        reactor.stop()

    d.addCallback(timeline)
    d.addCallback(cb)
    d.addCallback(trend)
    d.addCallback(cb)
    d.addCallback(stop)
    d.addErrback(lambda _: sys.stdout.write("error: %r\n", _))

    d.callback(None)

    reactor.run()
