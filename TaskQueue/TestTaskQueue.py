from TaskQueue import Task, TaskQueue
import unittest

class TestTask(unittest.TestCase):
    def testInit(self):
        t = Task(id=1, time_left=3)
        self.assertEqual(t.id, 1)
        self.assertEqual(t.time_left, 3)

    def testReduceTime(self):
        t = Task(id=1, time_left=3)
        self.assertEqual(t.time_left, 3)
        t.reduce_time(2)
        self.assertEqual(t.time_left, 1)
        t.reduce_time(1)
        self.assertEqual(t.time_left, 0)

class TestTaskQueue(unittest.TestCase):
    def testInit(self):

        TQ = TaskQueue()
        self.assertEqual(len(TQ), 0)
        self.assertEqual(TQ.time_per_task, 1)


        TQ = TaskQueue(time_per_task = 3)
        self.assertEqual(TQ.time_per_task, 3)
        

    def testAddRemoveTasks(self):
        t1 = Task(id=1, time_left=3)
        t2 = Task(id=2, time_left=1)
        t3 = Task(id=3, time_left=5)
        tasks = [t1, t2, t3]

        TQ = TaskQueue()
        for task in tasks:
            TQ.add_task(task)

        with self.assertRaises(RuntimeError):
                TQ.remove_task(7)


        self.assertEqual(len(TQ), 3)
        self.assertEqual(TQ.current.id, 1)

        TQ.remove_task(1)
        self.assertEqual(len(TQ), 2)
        self.assertEqual(TQ.current.id, 2)

        TQ.remove_task(2)
        self.assertEqual(len(TQ), 1)
        self.assertEqual(TQ.current.id, 3)

        TQ.remove_task(3)
        self.assertEqual(len(TQ), 0)
        self.assertEqual(TQ.current, None)

    def testIsEmpty(self):
        # note that we test an expected True *and* an expected False
        t1 = Task(id=1, time_left=3)
    
        TQ = TaskQueue()
        self.assertTrue(TQ.is_empty())

        TQ.add_task(t1)
        self.assertFalse(TQ.is_empty())

    def testExecuteTasks(self):
        t1 = Task(id=1, time_left=3)
        t2 = Task(id=2, time_left=1)
        t3 = Task(id=3, time_left=5)
        tasks = [t1, t2, t3]

        TQ = TaskQueue(time_per_task=1)

        for task in tasks:
            TQ.add_task(task)

        self.assertEqual(TQ.execute_tasks(), 9)


unittest.main()