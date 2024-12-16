from multiprocessing.managers import BaseManager
from queue import Queue

ADDRESS = ("127.0.0.1", 50000)
AUTHKEY = b"voila"


class QueueManager(BaseManager):
    pass


class QueueClient(BaseManager):
    pass


if __name__ == "__main__":
    task_queue = Queue()
    result_queue = Queue()
    m = QueueManager(address=ADDRESS, authkey=AUTHKEY)
    QueueManager.register("task_queue", callable=lambda: task_queue)
    QueueManager.register("result_queue", callable=lambda: result_queue)
    s = m.get_server()
    s.serve_forever()
