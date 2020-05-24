from SystemOriginal import SystemOriginal
from SystemGA import SystemGA
from SystemRS import SystemRS
from SystemEDF import SystemEDF
from SystemDG import SystemDG
from Input import *
from Task import RTTask, NonRTTask

def get_df(input_file="input/df.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        return int(f.readline())

def hrt_run():
    # # Original
    # RTTask.total_power = NonRTTask.total_power = 0
    # sim_time, verbose, processor, memories = get_configuration()
    # rt_tasks = get_rt_tasks()
    # non_rt_tasks = get_non_rt_tasks()
    # SystemOriginal(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()
    #
    # # DG(비실시간 담당 코어가 다수일 수 있음)
    # df = get_df()
    # for c in range(-df, df+1):
    #     RTTask.total_power = NonRTTask.total_power = 0
    #     sim_time, verbose, processor, memories = get_configuration()
    #     rt_tasks = get_rt_tasks()
    #     non_rt_tasks = get_non_rt_tasks()
    #     print("\n{}".format(c))
    #     SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, c).run()

    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    SystemEDF(sim_time, verbose, processor, memories, rt_tasks, None).run()

