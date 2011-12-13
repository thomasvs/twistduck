#!/usr/bin/python

import sys

from twistduck import base, widgets
from twisted.internet import reactor

if __name__ == '__main__':
    # FIXME: implement basic auth
    API_KEY = None
    AUTH = open('auth').readline().strip()

    db = base.DucksBoard(key=API_KEY, auth=AUTH)

    dtl = widgets.TimeLine(db, 21278)
    d = dtl.send(
        title="hi",
        content="Some details about my error message",
        image="https://dashboard.ducksboard.com/static/img/timeline/red.gif")

    print d
    def cb(res):
        print res
        reactor.stop()
    d.addCallback(cb)
    d.addErrback(lambda _: sys.stdout.write("error: %r\n", _))

    reactor.run()
