from utility import *
import random
from Task import RTTask


def get_period(input_file="input/input_rt_gen.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        int(f.readline())
        int(f.readline())
        return int(f.readline().split()[0])


def get_rt_tasks(input_file="input_rt_tasks.txt"):
    rt_tasks = []
    with open(input_file, "r", encoding='UTF-8') as f:
        for i in range(int(f.readline())):
            line = f.readline().split()
            rt_tasks.append(RTTask(i, *map(int, line[:3]), float(line[3])))

    return rt_tasks


def non_rt_gen():
    sim_time, arr_rate, bt_min, bt_max, mem_total, total_memory_usage = get_input()
    mem_req_total = 0
    period = get_period()
    task_per_period = round(period * arr_rate)
    rt_tasks = get_rt_tasks()
    wcet_mean = round(sum([task.wcet for task in rt_tasks]) / len(rt_tasks) * 25)

    with open('input_nonrt_tasks.txt', 'w', encoding='utf-8') as f:
        time = period
        tasks = []
        while time < sim_time:
            if task_per_period <= 0:
                n_task = 1 if random.random() <= period * arr_rate else 0
            else:
                n_task = task_per_period + int(random.randrange(task_per_period)) \
                         - int(random.randrange(task_per_period))

            for _ in range(n_task):
                tasks.append((time, wcet_mean + int(random.randrange(wcet_mean // 2)
                                                    - int(random.randrange(wcet_mean // 2)))))
            time += period

        mem_req_1task = mem_total / len(tasks)

        f.write("{}\n".format(len(tasks)))
        for task in tasks:
            mem_req = mem_req_1task + random.randrange(int(mem_req_1task / 2)) - random.randrange(
                int(mem_req_1task / 2))
            mem_active_ratio = 0.1 + random.randrange(1000) / 10000.0 - random.randrange(1000) / 10000.0
            mem_req_total += mem_req

            f.write("{} {} {} {}\n".format(*task, format(mem_req, ".0f"), format(mem_active_ratio, ".6f")))

    # print("\n=======================================================")
    # print(f'mem_req_total: {format(mem_req_total, ".0f")}')
    # print("This is the Task Generation Output")
    # print("Generate {} tasks.".format(len(tasks)))

# non_rt_gen
