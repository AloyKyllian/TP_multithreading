from manager import QueueClient

ADDRESS = ("127.0.0.1", 50000)
AUTHKEY = b"voila"


class Minion(QueueClient):
    pass


if __name__ == "__main__":
    m = Minion()
    task_queue = m.task_queue
    result_queue = m.result_queue
    while True:
        cpt = 0
        while task_queue.qsize() > 0:
            task = task_queue.get()
            task.work()
            result_queue.put(task)
            cpt += 1
            print("the task number " + str(task.identifier) + " is done")
