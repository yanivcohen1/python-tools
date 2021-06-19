import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='(%(threadName)-9s) %(message)s',)

class massage:
    msg = None
    # Initializing
    def __init__(self, msg = None):
        self.msg = msg

    def setMsg(self, msg):
        self.msg = msg

    def getMsg(self) -> any:
        return self.msg

def consumer(cv: threading.Condition ,msg: massage, timeout = None):
    logging.debug('Consumer thread started ...')
    for x in range(1, 5, 2): # 1, 3 Loop twice in total
        with cv:
            logging.debug('Consumer waiting ...')
            if timeout == None: cv.wait()
            else: cv.wait(timeout)
            logging.debug('Consumer consumed the resource, timeout: %s, msg %s', timeout, msg.getMsg())

def producer(cv: threading.Condition, msg: massage):
    logging.debug('Producer thread started ...')
    with cv:
        logging.debug('Making resource available')
        msg.setMsg("from producer thread")
        logging.debug('Notifying to all consumers, msg %s', msg.getMsg())
        cv.notifyAll()

if __name__ == '__main__':
    condition = threading.Condition()
    msg = massage()
    cs1 = threading.Thread(name='consumer1', target=consumer, args=(condition, msg))
    cs2 = threading.Thread(name='consumer2', target=consumer, args=(condition, msg, 3)) # timeout 3 sec
    pd = threading.Thread(name='producer', target=producer, args=(condition, msg))

    cs1.start()
    time.sleep(2)
    cs2.start()
    time.sleep(2)
    msg.setMsg("from main thread")
    with condition:
        condition.notify_all()
    time.sleep(2)
    pd.start()