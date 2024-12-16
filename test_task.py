import unittest
import numpy as np
from task import Task


class TestTask(unittest.TestCase):
    def test_work(self):
        task = Task()
        task.work()
        np.testing.assert_allclose(np.dot(task.a, task.x), task.b)
    def test_json(self):
        task = Task()
        task_json = task.to_json()
        task2 = Task.from_json(task_json)
        print(task == task2)


if __name__ == "__main__":
    unittest.main()
