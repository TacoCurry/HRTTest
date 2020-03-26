from System import System
import heapq


class SystemIGA(System):
    # 대기중인 non-rt-task가 존재하면 Original과 같은 방식으로 실행.
    # 존재하지 않는다면 유전 알고리즘 결과를 이용하여 실행.

    def __init__(self, sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks):
        super().__init__(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks)
        self.name = "IGA(instant-genetic-algorithm)"

    def run(self):
        # Initialize rt-tasks
        for rt_task in self.rt_tasks:
            rt_task.set_job()
            self.push_rt_queue(rt_task)

        cur_time = 0
        while cur_time < self.sim_time:
            if self.verbose != System.VERBOSE_SIMPLE:
                print("\ncurrent time: {}".format(cur_time))
            if self.verbose == System.VERBOSE_DEBUG_HARD:
                self.print_debug(cur_time)

            # 1. 새로운 RT-task 및 Non-RT-task 확인하기
            self.check_new_non_rt(cur_time)  # 새롭게 들어온 non_rt_job인 이 있는지 확인

            # 새롭게 주기 시작하는 job이 있는지 확인.
            # non_rt_job이 존재한다면 Exec_mode 오리지널, 존재 하지 않는다면 GA로 실행
            for new_start_rt_task in self.check_wait_period_queue(cur_time):
                self.push_rt_queue(new_start_rt_task)

            exec_mode = 'G' if len(self.non_rt_queue) == 0 else 'O'
            for rt_task in self.rt_queue:
                rt_task.set_exec_mode(self.processor, self.memories, exec_mode)
            heapq.heapify(self.rt_queue)

            # 2. 이번 퀀텀에 실행될 Task 고르기
            rt_exec_tasks = []
            non_rt_exec_tasks = []

            for _ in range(min(len(self.rt_queue), self.processor.n_core)):
                rt_exec_tasks.append(heapq.heappop(self.rt_queue))
            for _ in range(min(self.processor.n_core - len(rt_exec_tasks), len(self.non_rt_queue))):
                non_rt_exec_tasks.append(self.non_rt_queue.popleft())

            # 3. Task 실행하기
            # 3.0 util 계산하기
            # (실행 코어 개수) / (전체 코어 개수)로 이번 퀀텀의 cpu util 계산 가능
            util = (len(rt_exec_tasks) + len(non_rt_exec_tasks)) * 100 / self.processor.n_core
            self.add_cpu_utilization(util)

            # 3.1 Idle Processor
            for _ in range(self.processor.n_core - len(rt_exec_tasks) - len(non_rt_exec_tasks)):
                self.processor.exec_idle_without_dvfs()

            # 3.2 RT-task
            # for other non-active rt-tasks (이번 주기에 실행이 안되더라도 메모리는 차지하고 있으므로)
            for non_exec_rt_task in self.rt_queue:
                non_exec_rt_task.exec_idle(self.memories)
            for (_, non_exec_rt_task) in self.rt_wait_queue:
                non_exec_rt_task.exec_idle(self.memories)

            # for active rt-tasks
            if len(rt_exec_tasks) > 0 and self.verbose != System.VERBOSE_SIMPLE:
                print("{}~{} quantum, RT-Task {} 실행함".format(cur_time, cur_time + 1,
                                                             ",".join(map(lambda task: str(task.no), rt_exec_tasks))))

            for rt_task in rt_exec_tasks:
                rt_task.exec_active(self.processor, self.memories)  # 실행
                if rt_task.is_finish():
                    # 이번 주기에 실행을 완료했다면
                    rt_task.init_job()
                    self.push_rt_wait_queue(rt_task)
                else:
                    # 이번 주기 실행할 것 남았다면 다시 대기 큐에 넣기
                    self.push_rt_queue(rt_task)

            # 3.3 Non-RT-task
            # for other non-active non-rt-tasks (이번 주기에 실행이 안되더라도 메모리는 차지하고 있으므로)
            for non_exec_non_rt_task in self.non_rt_queue:
                non_exec_non_rt_task.exec_idle(self.memories)

            # for active non-rt-tasks
            if len(non_rt_exec_tasks) > 0 and self.verbose != System.VERBOSE_SIMPLE:
                print("{}~{} quantum, Non-RT-Task {} 실행함".format(cur_time, cur_time + 1,
                                                                 ",".join(map(lambda task: str(task.no),
                                                                              non_rt_exec_tasks))))
            for non_rt_task in non_rt_exec_tasks:
                non_rt_task.exec_active(self.processor, self.memories, cur_time)
                if non_rt_task.is_end():
                    # 이번 주기에 실행을 완료했다면
                    non_rt_task.end_time = cur_time + 1
                else:
                    # 아직 실행이 남았다면 다시 대기 큐에 넣기
                    self.non_rt_queue.append(non_rt_task)

            # 4. 마무리
            cur_time += 1
            self.check_rt_tasks(cur_time)  # 데드라인 어긴 태스크 없는지 확인

        self.print_final_report()
