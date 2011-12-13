import time

class Widget(object):
    wid = None

    def __init__(self, ducksboard, wid):
        self._ducksboard = ducksboard
        self.wid = wid


    def post(self, data):
        d = self._ducksboard.post(self.wid, data)
        return d



class TimeLine(Widget):

    def send(self, title, content=None, image=None):
        data = {
            "timestamp": time.time(),
            "value": {
                "title": title,
                "content": content,
                "image": image
            }
        }


        d = self.post(data)

        return d
