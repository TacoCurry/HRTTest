import random
import sys


class TaskGen:
    def __init__(self):
        # 입력 정보
        self.n_cores = None
        self.n_tasks = None
        self.wcet_min = self.wcet_max = None
        self.period = None
        self.mem_total = None
        self.util_cpu = None
        self.total_mem_usage = None

        self.n_mems = 2
        self.util_sum_cpu = self.mem_req_total = 0
        self.get_input()

    def gen_task(self):
        with open("input_rt_tasks.txt", "w", encoding='UTF8') as f:
            util = 0
            while True:
                util += self.do_gen_task(f)
                if util >= self.util_cpu:
                    print("util sum: {}".format(util))
                    break

    def do_gen_task(self, input_file):
        class rt_param:
            def __init__(self, name, period, wcet, mem_usage_ratio):
                self.name = name
                self.period = period  # ms
                self.wcet = wcet  # ms
                self.mem_usage_ratio = mem_usage_ratio  # ms

        rt_params = [rt_param("serial", 78, 1, 0.1),
                     rt_param("length", 78, 10, 0.1),
                     rt_param("way point", 234, 25, 0.25),
                     rt_param("encoder", 234, 4, 0.25),
                     rt_param("pid", 234, 10, 0.2),
                     rt_param("motor", 234, 3, 0.1),
                     rt_param("sense temperature", 10000, 1, 0.04),
                     rt_param("send data to server", 60000, 6, 0.12),
                     rt_param("sense vibration", 100, 6, 0.1),
                     rt_param("compress and send", 1000, 8, 0.24),
                     rt_param("get info & calc", 10, 1, 0.12),
                     rt_param("control machine", 10, 1, 0.05),
                     rt_param("update gui", 1000, 20, 0.33)]

        rt = random.choice(rt_params)

        wcet = rt.wcet
        duration = rt.period
        memreq = self.mem_total * rt.mem_usage_ratio
        mem_active_ratio = 0.1 + self.get_rand(1000) / 10000.0 - self.get_rand(1000) / 10000.0

        self.util_sum_cpu += wcet / duration
        self.mem_req_total += memreq

        line = f'{wcet} {format(duration, ".0f")} {format(memreq, ".0f")} {format(mem_active_ratio, ".6f")}\n'
        # print(f'util_total_mem: {format(self.get_util_overhead_by_mem(self.mem_req_total), ".6f")}')
        # print(f'util_total_cpu: {format(self.util_sum_cpu, ".6f")}')
        # print(f'memreq_total: {format(self.mem_req_total, ".0f")}')

        input_file.write(line)
        return wcet / duration

    def get_util_overhead_by_mem(self, mem_used):
        return mem_used / self.mem_total

    def get_input(self, input_file="input/input_rt_gen.txt"):
        # 입력 받기
        try:
            with open(input_file, "r", encoding='UTF8') as f:
                self.n_cores = int(f.readline())
                #self.n_tasks = int(f.readline())
                self.wcet_min, self.wcet_max = tuple(map(int, f.readline().split()))

                line = f.readline().split()
                self.period, self.mem_total = tuple(map(int, line[:2]))
                self.util_cpu = float(line[2])
                self.total_mem_usage = int(line[3])

                # print("=======================================================")
                # print("This is the Task Generation Input")
                #
                # print("n_cores  n_tasks")
                # print(self.n_cores, self.n_tasks)
                #
                # print("period, mem_total, util_cpu, util_target")
                # print(self.period, self.mem_total, self.util_cpu, self.total_mem_usage)

        except FileNotFoundError:
            self.error("task 정보 파일을 찾을 수 없습니다.")

    @staticmethod
    def get_rand(max_value):
        return random.randrange(int(max_value + 1))

    @staticmethod
    def error(message: str):
        print(message)
        sys.exit()
