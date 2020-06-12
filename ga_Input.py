from ga_Memory import Memories
from ga_Task import RTTask
import sys
from ga_Processor import Processor


class GAConfig:
    def __init__(self):
        self.MAX_GEN = None
        self.POPULATIONS = None
        self.TRY_LIMIT = None
        self.UTIL_LIMIT_RATIO = None
        self.PENALTY_RATIO = None
        self.MUTATION_PROB = None
        self.K = None
        self.MAX = self.MIN = None


def get_configuration(input_file="input/input_configuration.txt"):
    try:
        processor = None
        memories = None

        with open(input_file, "r", encoding='UTF-8') as f:
            while True:
                line = f.readline()
                if not line:
                    break  # EOF

                line = line.split()
                if len(line) == 0:
                    continue
                if line[0] == '##':
                    if line[1] == 'Memory':
                        memories = get_memory(f)
                    elif line[1] == 'Processor':
                        processor = get_processor(f)
                    elif line[1] == 'GA':
                        ga_config = get_ga_config(f)

        return processor, memories, ga_config

    except FileNotFoundError:
        print("Cannot find {}".format(input_file))
        sys.exit(0)


def get_processor(f):
    processor = Processor(int(f.readline()))
    while True:
        line = f.readline().split()
        if len(line) == 0:
            break
        processor.insert_processor_mode(*map(float, line))
    return processor


def get_memory(f):
    memories = Memories()
    while True:
        line = f.readline().split()
        if len(line) == 0:
            break
        memories.insert_memory(int(line[1]), *map(float, line[2:]))
    return memories


def get_ga_config(f):
    ga_config = GAConfig()

    ga_config.MAX_GEN = int(f.readline())
    ga_config.POPULATIONS = int(f.readline())
    ga_config.TRY_LIMIT = int(f.readline())
    ga_config.UTIL_LIMIT_RATIO = float(f.readline())
    ga_config.PENALTY_RATIO = int(f.readline())
    ga_config.MUTATION_PROB = float(f.readline())
    ga_config.K = int(f.readline())
    ga_config.MAX, ga_config.MIN = tuple(map(int, f.readline().split()))

    return ga_config


def get_rt_tasks(input_file="input_rt_tasks.txt"):
    try:
        rt_tasks = []
        with open(input_file, "r", encoding='UTF-8') as f:
            for i in range(int(f.readline())):
                line = f.readline().split()
                rt_tasks.append(RTTask(*map(int, line[:3]), float(line[3])))

        # for rt_task in rt_tasks:
        #    rt_task.wcet += 1

        return rt_tasks

    except FileNotFoundError:
        print("Cannot find {}".format(input_file))
        sys.exit(0)
