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
    set_ga_results(rt_tasks)

    SystemOriginal(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # GA (지연방식)
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    set_ga_results(rt_tasks)

    SystemGA(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # RS
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    set_ga_results(rt_tasks)

    SystemRS(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()

    # DG(비실시간 담당 코어가 다수일 수 있음)
    RTTask.total_power = NonRTTask.total_power = 0
    sim_time, verbose, processor, memories = get_configuration()
    rt_tasks = get_rt_tasks()
    non_rt_tasks = get_non_rt_tasks()
    SystemDG(sim_time, verbose, processor, memories, rt_tasks, non_rt_tasks).run()
