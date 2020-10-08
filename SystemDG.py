from System import System
from Task import RTTask
import heapq


def get_period(input_file="input/input_rt_gen.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        int(f.readline())
        f.readline()
        return int(f.readline().split()[0])


def get_df(input_file="input/df.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        return int(f.readline())


def get_fic_tasks(rt_tasks, df, input_file="input_dfga_fictional_task_result.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        fic_tasks = [[] for _ in range(df + 1)]
        fic_util = []
        for i in range(df + 1):
            fic_util.append(float(f.readline()))
            task_no = len(rt_tasks) - 1
            while True:
                line = f.readline().split()
                if not line:
                    break
                task_no += 1
                fic_tasks[i].append(
                    RTTask(task_no, int(line[0]), int(line[1]), float(line[2]), float(line[3])))
        return fic_tasks, fic_util


def set_ga_results(rt_tasks, fic_tasks, df, input_file="input_dfga_result.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        for task in rt_tasks:
            task.ga_processor_modes = [0 for _ in range(df + 1)]
            task.ga_memory_modes = [0 for _ in range(df + 1)]

        for i in range(df + 1):
            f.readline()
            task_no = -1
            while True:
                line = f.readline().split()
                if not line:
                    break
                task_no += 1
                if task_no < len(rt_tasks):
                    rt_tasks[task_no].ga_processor_modes[i] = int(line[0])
                    rt_tasks[task_no].ga_memory_modes[i] = int(line[1])
                else:
                    fic_tasks[i][task_no - len(rt_tasks)].ga_processor_modes = int(line[0])
                    fic_tasks[i][task_no - len(rt_tasks)].ga_memory_modes = int(line[1])


class SystemDG(System):
    def __init__(self, sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, mode):
        super().__init__(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks)
        self.name = "D"
        self.mode = 1

    def run(self):
        self.init_remain_burst_time_track()

        util_original = self.calc_original_util()
        df = get_df()
        margin = (self.processor.n_core - util_original) / df
        period = get_period()
        fic_tasks, fic_util = get_fic_tasks(self.rt_tasks, df)
        set_ga_results(self.rt_tasks, fic_tasks, df)

        # Initialize rt-tasks
        for rt_task in self.rt_tasks:
            rt_task.set_job()
            rt_task.next_period_start = 0
            self.push_rt_wait_queue(rt_task)

        cur_time = 0
        past_bt_sum = 1000000
        while cur_time < self.sim_time:
            # 1 tick 마다 실행 할
            if self.verbose != System.VERBOSE_SIMPLE:
                print("\ncurrent time: {}".format(cur_time))
            if self.verbose == System.VERBOSE_DEBUG_HARD:
                self.print_debug(cur_time)

            # 1. 새로운 RT-task 및 Non-RT-task 확인하기
            past_bt_sum += self.check_new_non_rt(cur_time)  # 새롭게 들어온 non_rt_job이 있는지 확인

            if cur_time % period == 0:
                remain_burst_time_sum = 0
                for non_rt_task in self.non_rt_queue:
                    remain_burst_time_sum += non_rt_task.bt - non_rt_task.exec_time

                mode = 2
                # mode = round((past_bt_sum + remain_burst_time_sum) * df / (
                #             period * (self.processor.n_core - util_original))) + self.mode
                # if mode < 0:
                #     mode = 0
                # elif mode > df:
                #     mode = df
                past_bt_sum = 0

                for new_start_rt_task in self.check_wait_period_queue(cur_time):
                    new_start_rt_task.set_exec_mode(self.processor, self.memories, 'G', mode)
                    self.push_rt_queue(new_start_rt_task)
                for fic_task in fic_tasks[mode]:
                    fic_task.i_job = 1
                    fic_task.deadline = cur_time + period
                    fic_task.ga_mode = None
                    fic_task.det = fic_task.wcet
                    fic_task.fic_set_exec_mode(self.processor, self.memories)
                    self.push_rt_queue(fic_task)

            self.print_remain_burst_time_track(cur_time)  # burst_time_tracking 결과 출력

            # 2. 이번 퀀텀에 실행될 Task 고르기
            rt_exec_tasks = []
            for _ in range(min(len(self.rt_queue), self.processor.n_core)):
                rt_exec_tasks.append(heapq.heappop(self.rt_queue))

            # 3. Task 실행하기
            # 3.0 util 계산하기

            # 3.1 Idle Processor
            for _ in range(self.processor.n_core - len(rt_exec_tasks)):
                self.processor.exec_idle_with_dvfs()

            # 3.2 RT-task
            # for other non-active rt-tasks (이번 주기에 실행이 안되더라도 메모리는 차지하고 있으므로)
            for non_exec_rt_task in self.rt_queue:
                if non_exec_rt_task.no < len(self.rt_tasks):
                    non_exec_rt_task.exec_idle(self.memories)
            for (_, non_exec_rt_task) in self.rt_wait_queue:
                non_exec_rt_task.exec_idle(self.memories)

            # for active rt-tasks
            if len(rt_exec_tasks) > 0 and self.verbose != System.VERBOSE_SIMPLE:
                print("{}~{} quantum, RT-Task {} 실행함".format(cur_time, cur_time + 1,
                                                             ",".join(
                                                                 map(lambda task: str(task.no), rt_exec_tasks))))
            non_rt_count = util_temp = 0
            for rt_task in rt_exec_tasks:
                if rt_task.no < len(self.rt_tasks):
                    rt_task.exec_active(self.processor, self.memories)  # 실행
                    util_temp += 1
                else:
                    if len(self.non_rt_queue) > 0:
                        non_rt_count += 1
                    rt_task.i_job += 1
                    rt_task.calc_d_for_pd2()
                    rt_task.calc_b_for_pd2()
                    rt_task.calc_D_for_pd2()

                if rt_task.is_finish():
                    # 이번 주기에 실행을 완료했다면
                    if rt_task.no < len(self.rt_tasks):
                        rt_task.init_job()
                        self.push_rt_wait_queue(rt_task)
                else:
                    # 이번 주기 실행할 것 남았다면 다시 대기 큐에 넣기
                    self.push_rt_queue(rt_task)

            non_rt_tasks = [self.non_rt_queue.popleft() for _ in range(min(len(self.non_rt_queue), non_rt_count))]
            for non_rt_task in non_rt_tasks:
                util_temp += 1
                non_rt_task.exec_active(self.processor, self.memories, cur_time)  # 실행
                if self.verbose != System.VERBOSE_SIMPLE:
                    print("{}~{} quantum, Non-RT-Task {} 실행함".format(cur_time, cur_time + 1, non_rt_task.no))
                if non_rt_task.is_end():
                    # 이번 주기에 실행을 완료했다면
                    non_rt_task.end_time = cur_time + 1
                else:
                    # 아직 실행이 남았다면 다시 대기 큐에 넣기
                    self.non_rt_queue.append(non_rt_task)

            # (실행 코어 개수) / (전체 코어 개수)로 이번 퀀텀의 cpu util 계산 가능
            util = util_temp * 100 / self.processor.n_core
            self.add_cpu_utilization(util)

            # 4. 마무리
            cur_time += 1
            self.check_rt_tasks(cur_time)  # 데드라인 어긴 태스크 없는지 확인

        self.print_final_report()
