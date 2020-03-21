class RTTask:
    def __init__(self, wcet, period, mem_req, mem_active_ratio):
        self.wcet = wcet
        self.period = period
        self.mem_req = mem_req
        self.mem_active_ratio = mem_active_ratio
