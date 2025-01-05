from manager import QueueClient
from task import Task

ADDRESS = ("127.0.0.1", 50000)
AUTHKEY = b"voila"
NB_TASKS = 1


class Boss(QueueClient):
    pass


if __name__ == "__main__":
    m = Boss()
    task_queue = m.task_queue
    result_queue = m.result_queue

    for i in range(NB_TASKS):
        t = Task(identifier=i)
        task_queue.put(t)
        task_queue.put(t)
        print("Task number " + str(i) + " is added")

    while result_queue.qsize() < NB_TASKS:
        pass

    for i in range(NB_TASKS * 2):
        t = result_queue.get()
        print(t.time)
        print(t.x)

    print("All tasks are done")
