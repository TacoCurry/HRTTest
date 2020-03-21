class ProcessorMode:
    def __init__(self, wcet_scale, power_active, power_idle):
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle


class Processor:
    def __init__(self, n_core):
        self.n_core = n_core
        self.modes = []
        self.n_mode = 0

    def insert_processor_mode(self, wcet_scale, power_active, power_idle):
        self.modes.append(ProcessorMode(wcet_scale, power_active, power_idle))
        self.n_mode += 1
