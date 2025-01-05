import time
import json
import numpy as np


class Task:
    def __init__(self, identifier=0, size=None):
        self.identifier = identifier
        # choosee the size of the problem
        self.size = 100
        # Generate the input of the problem
        self.a = np.random.rand(self.size, self.size)
        self.b = np.random.rand(self.size)
        # prepare room for the results
        self.x = np.zeros((self.size))
        self.time = 0

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        if (
            self.identifier != other.identifier
            and self.size != other.size
            and self.a != other.a
            and self.b != other.b
            and self.x != other.x
            and self.time != other.time
        ):
            return False
        return True

    def to_json(self):
        txt = json.dumps(
            {
                "identifier": self.identifier,
                "size": self.size,
                "a": self.a.tolist(),
                "b": self.b.tolist(),
                "x": self.x.tolist(),
                "time": self.time,
            },
            sort_keys=True,
        )

        return txt

    @staticmethod
    def from_json(data):
        task = Task()
        data = json.loads(data)
        task.identifier = data["identifier"]
        task.size = data["size"]
        task.a = np.array(data["a"])
        task.b = np.array(data["b"])
        task.x = np.array(data["x"])
        task.time = data["time"]
        return task

    def work(self):
        start = time.perf_counter()
        self.x = np.linalg.solve(self.a, self.b)
        self.time = time.perf_counter() - start
