def error(msg):
    print(msg)
    exit(0)


def get_input(input_file="input/input_non_rt_gen.txt"):
    try:
        with open(input_file, "r", encoding='UTF8') as f:
            sim_time = int(f.readline())
            arr_rate = float(f.readline())

            bt_min, bt_max = tuple(map(int, f.readline().split()))
            mem_total, total_memory_usage = tuple(map(int, f.readline().split()))

            # print("=======================================================")
            #             # print("This is the Task Generation Input")
            #             #
            #             # print("sim_time: {}".format(sim_time))
            #             # print("arr_rate: {}".format(arr_rate))
            #             # print("bt_min: {}".format(bt_min))
            #             # print("bt_max: {}".format(bt_max))
            #             # print("mem_total: {}".format(mem_total))
            #             # print("total_memory_usage: {}".format(total_memory_usage))

            return sim_time, arr_rate, bt_min, bt_max, mem_total, total_memory_usage

    except FileNotFoundError:
        error("task 정보 파일을 찾을 수 없습니다.")
