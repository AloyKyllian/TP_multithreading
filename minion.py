from manager import QueueClient
from task import Task

ADDRESS = ('127.0.0.1',50000)
AUTHKEY = b'voila'

class Minion(QueueClient):
    pass

if __name__ == '__main__':
    Minion.register('task_queue')
    Minion.register('result_queue')
    m = Minion(address=ADDRESS, authkey=AUTHKEY)
    m.connect()
    task_queue = m.task_queue()
    result_queue = m.result_queue()
    while True:
        cpt = 0
        while (task_queue.qsize() > 0):
            task = task_queue.get()
            task.work()
            result_queue.put(task)
            cpt += 1
            print('the task number '+str(task.identifier)+' is done')
            