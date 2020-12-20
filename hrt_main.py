from SystemOriginal import SystemOriginal
from SystemGIA1 import SystemGIA1
from SystemGIA2 import SystemGIA2
from SystemGRA import SystemGRA
from SystemDG import SystemDG
from Input import *
from Task import RTTask, NonRTTask

def get_df(input_file="input/df.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        return int(f.readline())

def hrt_run():
    # Original
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemOriginal(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # DG(비실시간 담당 코어가 다수일 수 있음)
    df = get_df()
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    print("\n{}".format(1))
    SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 1).run()

    # GRA
    # df = get_df()
    # RTTask.total_power = NonRTTask.total_power = 0
    # sim_time, verbose, processor, memories = get_configuration()
    # rt_tasks = get_rt_tasks()
    # non_rt_tasks = get_non_rt_tasks()
    # print("\n{}".format(1))
    # SystemGRA(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # GIA-1
    # df = get_df()
    # RTTask.total_power = NonRTTask.total_power = 0
    # sim_time, verbose, processor, memories = get_configuration()
    # rt_tasks = get_rt_tasks()
    # non_rt_tasks = get_non_rt_tasks()
    # print("\n{}".format(1))
    # SystemGIA1(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 1).run()
    #
    # # GIA-2
    # df = get_df()
    # RTTask.total_power = NonRTTask.total_power = 0
    # sim_time, verbose, processor, memories = get_configuration()
    # rt_tasks = get_rt_tasks()
    # non_rt_tasks = get_non_rt_tasks()
    # print("\n{}".format(1))
    # SystemGIA2(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 1).run()

