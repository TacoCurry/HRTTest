from System import System
import heapq


class SystemEDF(System):
    # 경성 태스크를 항상 오리지널 방식으로 수행하며, 비실시간이 들어오면 남는시간에 실행시켜주는 방식
    # 대조군. 유전알고리즘 쓰지 않음.

    def __init__(self, sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks):
        super().__init__(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks)
        self.name = "O"

    def run(self):
        task_queue = []

        for rt_task in self.rt_tasks:
            heapq.heappush(task_queue, (rt_task.period, rt_task.wcet, rt_task.period, rt_task.no))

        new_start = [0, 0, 0, 0]
        heapq.heapify(new_start)

        while True:
            start = heapq.heappop(new_start)
            if self.sim_time < start:
                break

            task = heapq.heappop(task_queue)
            if task[0] < start + task[1]:
                print("deadline failed {}".format(task[3]))
                break

            print("{}부터 {}까지 태스크{} 싫행".format(start, start + task[1], task[3]))
            heapq.heappush(task_queue, (task[0] + task[2], task[1], task[2], task[3]))
            heapq.heappush(new_start, start + task[1])
