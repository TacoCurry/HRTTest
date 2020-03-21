import random


class Solution:
    processor = None
    memories = None
    rt_tasks = None
    ga_configs = None

    def __init__(self):
        self.genes_processor = []
        self.genes_memory = []

        # For memory balance
        self.n_tasks_for_each_memory = None
        self.used_capacity_for_each_memory = None
        self.memory_with_most_tasks = None

        self.utilization = None
        self.power = None
        self.score = None

    def __lt__(self, other):
        return self.score < other.score

    def is_schedule(self):
        return self.utilization <= Solution.processor.n_core

    def calc_memory_with_most_tasks(self):
        # Find a memory with the most tasks
        res = (0, 0)
        for i, n_tasks in enumerate(self.n_tasks_for_each_memory):
            res = max(res, (n_tasks, i))
        self.memory_with_most_tasks = i

    def calc_memory_used(self):
        # Calculate memory usages for each task
        self.n_tasks_for_each_memory = [0 for _ in range(Solution.memories.n_mem_types)]
        self.used_capacity_for_each_memory = [0 for _ in range(Solution.memories.n_mem_types)]

        for i, rt_task in enumerate(Solution.rt_tasks):
            self.n_tasks_for_each_memory[self.genes_memory[i]] += 1
            self.used_capacity_for_each_memory[self.genes_memory[i]] += rt_task.mem_req

    def check_memory(self):
        # Check memory capacity for each memory
        return all([v <= Solution.memories.list[i].capacity
                    for i, v in enumerate(self.used_capacity_for_each_memory)])

    def adjust_memory(self):
        # Balance memory by moving a task placed in the most frequent memory to another memory.
        replace_index = random.randint(0, self.n_tasks_for_each_memory[self.memory_with_most_tasks] - 1)

        while True:
            new_mem_type = random.randint(0, Solution.memories.n_mem_types - 1)
            if new_mem_type != self.memory_with_most_tasks:
                break

        for i, m in enumerate(self.genes_memory):
            if m == self.memory_with_most_tasks:
                if replace_index == 0:
                    # Replace (replace_index)-th task of most frequent memory into new_mem_type
                    self.genes_memory[i] = new_mem_type

                    self.n_tasks_for_each_memory[self.memory_with_most_tasks] -= 1
                    self.used_capacity_for_each_memory[self.memory_with_most_tasks] -= Solution.rt_tasks[i].mem_req

                    self.n_tasks_for_each_memory[new_mem_type] += 1
                    self.used_capacity_for_each_memory[new_mem_type] += Solution.rt_tasks[i].mem_req

                    self.calc_memory_with_most_tasks()
                    break
                replace_index -= 1

    def check_utilization(self, n_core):
        # Check utilization using UTIL_LIMIT_RATIO
        util_sum = power_sum = 0

        for i, task in enumerate(Solution.rt_tasks):
            processor_mode = Solution.processor.modes[self.genes_processor[i]]
            memory = Solution.memories.list[self.genes_memory[i]]

            # Calc det
            wcet_scaled_processor = 1 / processor_mode.wcet_scale
            wcet_scaled_memory = 1 / memory.wcet_scale
            det = round(task.wcet * max(wcet_scaled_memory, wcet_scaled_processor))
            if det == 0:
                det = 1
            if det > task.period:
                return False  # deadline ncc

            # Calc util
            util_sum += det / task.period

            # Calc active power for processor
            processor_power_unit = (processor_mode.power_active * wcet_scaled_processor +
                                    processor_mode.power_idle * wcet_scaled_memory) / \
                                   (wcet_scaled_memory + wcet_scaled_processor)
            power_sum += processor_power_unit * det / task.period

            # Calc power for memory
            power_sum += task.mem_req * (task.mem_active_ratio * memory.power_active +
                                         (1 - task.mem_active_ratio) * memory.power_idle) * det / task.period \
                         + task.mem_req * memory.power_idle * (1 - det / task.period)

        if util_sum > n_core * (1 + Solution.ga_configs.UTIL_LIMIT_RATIO):
            return False

        # Calc idle power for processor
        if util_sum < n_core:
            power_sum += Solution.processor.modes[-1].power_idle * (Solution.processor.n_core - util_sum)

        self.utilization = util_sum
        self.power = power_sum
        self.score = power_sum
        if util_sum >= n_core:
            # Apply penalty for score
            self.score += power_sum * (util_sum - n_core) * Solution.ga_configs.PENALTY_RATIO
        return True

    def adjust_utilization(self):
        if random.random() * (Solution.processor.n_mode + Solution.memories.n_mem_types) < Solution.processor.n_mode:
            if not self.adjust_utilization_by_processor():
                if not self.adjust_utilization_by_memory():
                    return False
        else:
            if not self.adjust_utilization_by_memory():
                if not self.adjust_utilization_by_processor():
                    return False
        return True

    def adjust_utilization_by_memory(self):
        # Move a random task in LPM to DRAM
        n = len(Solution.rt_tasks)
        index_end = index = random.randint(0, n - 1)

        while True:
            index = (index + 1) % n
            if self.genes_memory[index] > 0:
                # Remove a task from LPM
                self.n_tasks_for_each_memory[self.genes_memory[index]] -= 1
                self.used_capacity_for_each_memory[self.genes_memory[index]] -= Solution.rt_tasks[index].mem_req
                # Add a task to DRAM
                self.genes_memory[index] -= 1
                self.n_tasks_for_each_memory[self.genes_memory[index]] += 1
                self.used_capacity_for_each_memory[self.genes_memory[index]] += Solution.rt_tasks[index].mem_req
                # Update memory with most tasks
                self.calc_memory_with_most_tasks()
                return True

            if index == index_end:
                break
        return False

    def adjust_utilization_by_processor(self):
        # Change a random task to higher processor voltage/frequency mode
        n = len(Solution.rt_tasks)
        index_end = index = random.randint(0, n - 1)

        while True:
            index = (index + 1) % n
            if self.genes_processor[index] > 0:
                self.genes_processor[index] -= 1
                return True
            if index == index_end:
                break
        return False

    @staticmethod
    def set_random_seed():
        random.seed()  # Set seed using current time

    @staticmethod
    def get_random_solution(n_core):
        solution = Solution()

        # Set random attributes
        solution.genes_processor = [random.randint(0, Solution.processor.n_mode - 1)
                                    for _ in range(len(Solution.rt_tasks))]
        solution.genes_memory = [random.randint(0, Solution.memories.n_mem_types - 1)
                                 for _ in range(len(Solution.rt_tasks))]

        # Try making valid solution
        solution.calc_memory_used()
        solution.calc_memory_with_most_tasks()
        for _ in range(Solution.ga_configs.TRY_LIMIT):
            if not solution.check_memory():
                solution.adjust_memory()
                continue
            if solution.check_utilization(n_core):
                return solution
            if not solution.adjust_utilization():
                raise Exception("random solution 생성 불가")

        # 생성을 반복해도 valid한 solution 을 만들지 못할 경우
        raise Exception("random solution 생성 불가")

    @staticmethod
    def select_solution(sum_fitness, fitness_list, solutions):
        point = random.random() * sum_fitness
        temp = 0
        for i, fitness in enumerate(fitness_list):
            temp += fitness
            if point < temp:
                break
        return i, solutions.pop(i)

    @staticmethod
    def select_solution_using_roulette_wheel(solutions):
        # 1. Calculate fitness using formula "fi = (Cw - Ci) + ( Cw - Cb ) / (k - 1)"
        worst_score = solutions[-1].score
        best_score = solutions[0].score
        constant = (worst_score - best_score) / (Solution.ga_configs.K - 1)

        fitness_list = [(worst_score - solution.score + constant) for solution in solutions]
        return Solution.select_solution(sum(fitness_list), fitness_list, solutions)

    @staticmethod
    def select_solution_using_ranking_selection(solutions):
        # Calculate fitness using Ranking Selection
        diff = Solution.ga_configs.MIN_RANKING_SELECTION - Solution.ga_configs.MAX_RANKING_SELECTION
        n = len(solutions)
        fitness_list = [Solution.ga_configs.MAX_RANKING_SELECTION + (i - 1) * diff / (n - 1)
                        for i in range(1, n + 1)]
        # Select
        return Solution.select_solution(sum(fitness_list), fitness_list, solutions)

    @staticmethod
    def crossover(solution1, solution2):
        n_task = len(Solution.rt_tasks)
        crossover_point_processor = random.randint(0, n_task)
        crossover_point_memory = random.randint(0, n_task)

        new_solution = Solution()
        new_solution.genes_processor = solution1.genes_processor[:crossover_point_processor] + \
                                       solution2.genes_processor[crossover_point_processor:]
        new_solution.genes_memory = solution1.genes_memory[:crossover_point_memory] + \
                                    solution2.genes_memory[crossover_point_memory:]
        return new_solution

    def mutation(self):
        if random.random() > Solution.ga_configs.MUTATION_PROB:
            return

        n_task = len(Solution.rt_tasks)

        # processor
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_processor[point1]
        self.genes_processor[point1] = self.genes_processor[point2]
        self.genes_processor[point2] = temp

        # memory
        point1 = random.randint(0, n_task - 1)
        point2 = random.randint(0, n_task - 1)
        temp = self.genes_memory[point1]
        self.genes_memory[point1] = self.genes_memory[point2]
        self.genes_memory[point2] = temp
