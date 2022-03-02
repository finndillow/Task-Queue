class Task:
    def __init__(self, id, time_left, _next=None, _prev=None):
        self.id = id
        self.time_left = time_left
        self._next = _next
        self._prev = _prev

    def reduce_time(self, time):
        self.time_left -= time

        # Negative if the task has "extra time" not used
        return self.time_left

class TaskQueue:
    def __init__(self, time_per_task=1):
        # Tracks set of ids for later
        self.ids = set()
        self.time_per_task = time_per_task
        self._len = 0

    def __len__(self): return self._len

    def is_empty(self): return self._len == 0

    def add_task(self, task):
        # update 
        self.ids.add(task.id)

        # first task added
        if len(self) == 0:
            self.current = task
            task._next = task
            task._prev = task
                
        else:
            self.current._prev._next = task
            task._prev = self.current._prev
            task._next = self.current
            self.current._prev = task

        # change current._next
        if len(self) == 1:
            self.current._next = task
        
        # update length
        self._len += 1

    def remove_task(self, id):
        if id not in self.ids:
            raise RuntimeError(f"id {id} not in TaskQueue")
        
        # loop until id found
        task = self.current
        while task.id != id:
            task = task._next

        # remove task
        if len(self) == 1:
            self.current = None

        else:
            task._next._prev = task._prev
            task._prev._next = task._next

            if task is self.current:
                self.current = task._next

        # update len, ids
        self._len -= 1
        self.ids.remove(task.id)

    def execute_tasks(self):
        time_executing = 0

        # loop until finished
        while not self.is_empty():
            time_left = self.current.reduce_time(self.time_per_task)
            if time_left < 0:
                time_executing -= time_left
            elif time_left == 0:
                time_executing += self.time_per_task
                print(f"Finished task {self.current.id} at t = {time_executing} seconds")
                self.remove_task(self.current.id)   
            else:
                time_executing += self.time_per_task
                self.current = self.current._next     
        return time_executing

