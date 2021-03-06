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
        self.n_tasks = round(self.util_cpu * self.n_cores / (((self.wcet_max + self.wcet_min) / 2) / self.period))

        util_cpu_1_task = self.util_cpu / self.n_tasks * self.n_cores
        mem_req_1_task = self.total_mem_usage / self.n_tasks

        # print("=======================================================")
        # print(f'util_cpu_1task:{format(util_cpu_1_task, ".6f")}')
        # print(f'memreq_1task: {format(mem_req_1_task, ".0f")}')
        # print("=======================================================")
        #
        with open("input_rt_tasks.txt", "w", encoding='UTF8') as f:
            f.write("{}\n".format(self.n_tasks))
            util = 0
            for _ in range(self.n_tasks):
                util += self.do_gen_task(f, util_cpu_1_task, mem_req_1_task)
            print("util sum: {}".format(util))

        # print(f'util_total_mem: {format(self.get_util_overhead_by_mem(self.mem_req_total), ".6f")}')
        # print(f'util_total_cpu: {format(self.util_sum_cpu, ".6f")}')
        # print(f'mem_req_total: {format(self.mem_req_total, ".0f")}')

    def do_gen_task(self, input_file, util_cpu_1_task, mem_req_1_task):
        wcet = self.wcet_min + self.get_rand(self.wcet_max - self.wcet_min)
        # duration = wcet / util_cpu_1_task + int(self.get_rand(wcet / util_cpu_1_task / 2)) - int(self.get_rand(wcet / util_cpu_1_task / 2))
        duration = self.period
        # wcet = int(duration * util_cpu_1_task) + int(self.get_rand(duration * util_cpu_1_task)) - int(self.get_rand(duration * util_cpu_1_task))
        if wcet == 0:
            wcet = 1
        memreq = mem_req_1_task + int(self.get_rand(mem_req_1_task / 2)) - int(self.get_rand(mem_req_1_task / 2))
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
