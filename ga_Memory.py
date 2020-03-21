class Memory:
    def __init__(self, capacity, wcet_scale, power_active, power_idle):
        self.capacity = capacity
        self.wcet_scale = wcet_scale
        self.power_active = power_active
        self.power_idle = power_idle
        self.used_capacity = 0


class Memories:
    def __init__(self):
        self.list = []
        self.n_mem_types = 0
        self.total_capacity = 0

    def insert_memory(self, capacity, wcet_scale, power_active, power_idle):
        self.list.append(Memory(capacity, wcet_scale, power_active, power_idle))
        self.n_mem_types += 1
        self.total_capacity += capacity

    def init_memories(self):
        self.total_capacity = 0
        for memory in self.list:
            memory.used_capacity = memory.power_consumed_active = memory.power_consumed_idle = 0
            self.total_capacity += memory.capacity

    def check_memory(self):
        for memory in self.list:
            if memory.used_capacity > memory.capacity:
                return False
        return True
