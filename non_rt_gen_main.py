from utility import *
import random


def non_rt_gen():
    sim_time, arr_rate, bt_min, bt_max, mem_total, total_memory_usage = get_input()
    mem_req_total = 0

    with open('input_nonrt_tasks.txt', 'w', encoding='utf-8') as f:
        tasks = [(cur_time, random.randint(bt_min, bt_max))
                 for cur_time in range(sim_time) if random.random() <= arr_rate]

        mem_req_1task = mem_total / len(tasks)

        f.write("{}\n".format(len(tasks)))
        for task in tasks:
            mem_req = mem_req_1task + random.randrange(int(mem_req_1task / 2)) - random.randrange(
                int(mem_req_1task / 2))
            mem_active_ratio = 0.1 + random.randrange(1000) / 10000.0 - random.randrange(1000) / 10000.0
            mem_req_total += mem_req

            f.write("{} {} {} {}\n".format(*task, format(mem_req, ".0f"), format(mem_active_ratio, ".6f")))

    print("\n=======================================================")
    print(f'mem_req_total: {format(mem_req_total, ".0f")}')
    print("This is the Task Generation Output")
    print("Generate {} tasks.".format(len(tasks)))


# non_rt_gen
