from SystemOriginal import SystemOriginal
from SystemGA import SystemGA
from SystemRS import SystemRS
from SystemDG import SystemDG
from Input import *
from Task import RTTask, NonRTTask


def hrt_run():
    # Original
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemOriginal(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # DG(비실시간 담당 코어가 다수일 수 있음)
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 3).run()

    # DG(비실시간 담당 코어가 다수일 수 있음)
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 2).run()

    # DG(비실시간 담당 코어가 다수일 수 있음)
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks, 1).run()
