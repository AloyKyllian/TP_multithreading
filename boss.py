from manager import QueueClient
from task import Task

ADDRESS = ("127.0.0.1", 50000)
AUTHKEY = b"voila"
NB_TASKS = 500


class Boss(QueueClient):
    pass


if __name__ == "__main__":
    Boss.register("task_queue")
    Boss.register("result_queue")
    m = Boss(address=ADDRESS, authkey=AUTHKEY)
    m.connect()
    task_queue = m.task_queue()
    result_queue = m.result_queue()

    for i in range(NB_TASKS):
        task_queue.put(Task(identifier=i))
        print("Task number " + str(i) + " is added")

    while result_queue.qsize() < NB_TASKS:
        pass

    for i in range(NB_TASKS):
        print(result_queue.get().time)

    print("All tasks are done")
