import requests
import random
import string
import threading



class MyThread(threading.Thread):

    def __init__(self, func):

        super(MyThread, self).__init__()
        self.func = func
        self._stop_event = threading.Event()
        self.threadLock = threading.Lock()

    def run(self):

        self.threadLock.acquire()
        self.func()
        self.threadLock.release()

    def stop(self):

        self._stop_event.set()


class Parameter(object):

    __digits = string.digits
    __chars = string.ascii_lowercase
    __ip_format = '192.168.'

    @classmethod
    def randomIP(cls):

        IP = cls.__ip_format + '.'.join('%s' % random.randint(0, 255) for i in range(2))

        return IP

    @classmethod
    def randomMAC(cls, length=12):

        MAC = ''.join(random.choice(cls.__chars + cls.__digits) for _ in range(length))

        return MAC

    @classmethod
    def randomSerial(cls, length=6):

        serial = ''.join(random.choice(cls.__digits) for _ in range(length))

        return serial


def lockRegister():

    url = "http://127.0.0.1:5160/lockapi/"
    url_parameter = url + Parameter.randomMAC() + '/re?lock_ip=' + Parameter.randomIP() + '&ps=@&serial=' + Parameter.randomSerial() + '&uid='

    requests.get(url_parameter)

threads = list()
for i in range(10):
    thread = MyThread(lockRegister)
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()



