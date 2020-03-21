from ga_Output import *
from ga_Solution import Solution
from ga_Input import *
import math


def ga_run():
    # Input from files
    processor, memories, ga_configs = get_configuration()
    Solution.processor, Solution.memories, Solution.ga_configs = processor, memories, ga_configs
    Solution.rt_tasks = get_rt_tasks()

    # Initiate out.txt
    init_out()

    # Get total utils
    original_utils = sum([task.wcet / task.period for task in Solution.rt_tasks])
    print("Original Total util: {}".format(original_utils))

    first_print(Solution.processor.n_core, math.ceil(original_utils))

    for core_max in range(Solution.processor.n_core, math.ceil(original_utils)-1, -1):
        # 1. Make initial solution set
        Solution.set_random_seed()
        solutions = [Solution.get_random_solution(core_max)
                     for _ in range(ga_configs.POPULATIONS)]
        solutions.sort()  # Sort solutions by score

        for g in range(ga_configs.MAX_GEN):
            if g != 0 and g % 100 == 0:
                report_print(core_max, g, solutions)

            get_new_solution = False
            for _ in range(ga_configs.TRY_LIMIT):
                # 2. Select two solution
                solution1_index, solution1 = Solution.select_solution_using_roulette_wheel(solutions)
                solution2_index, solution2 = Solution.select_solution_using_roulette_wheel(solutions)
                solutions.insert(solution2_index, solution2)
                solutions.insert(solution1_index, solution1)

                # 3. Crossover
                new_solution = Solution.crossover(solution1, solution2)
                new_solution.mutation()

                # 4. Check Validity
                new_solution.calc_memory_used()
                new_solution.calc_memory_with_most_tasks()
                if new_solution.check_memory() and new_solution.check_utilization(core_max):
                    get_new_solution = True
                    break

            if get_new_solution:
                # Replace worst solution into new solution
                solutions[-1] = new_solution
                solutions.sort()
                continue
            else:
                raise Exception("{}번째 generation 이후, solution 교배 불가".format(g+1))

        # 5. Print result
        for solution in solutions:
            if solution.is_schedule():
                print("n_core: {}".format(core_max))
                print("power: {}, utilization: {}".format(solution.power, solution.utilization))
                result_print(core_max, solution)
                break


# run()
