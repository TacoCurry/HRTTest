from ga_Output import *
from ga_Solution import Solution
from ga_Input import *
from ga_Task import *
import math
import copy


def get_period(input_file="input/input_rt_gen.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        int(f.readline())
        f.readline()
        return int(f.readline().split()[0])

def get_df(input_file="input/df.txt"):
    with open(input_file, "r", encoding='UTF8') as f:
        return int(f.readline())

def dfga_run():
    # Input from files
    processor, memories, ga_configs = get_configuration()
    Solution.processor, Solution.memories, Solution.ga_configs = processor, memories, ga_configs
    Solution.rt_tasks = rt_tasks = get_rt_tasks()
    period = get_period()
    df = get_df()

    # Initiate out.txt
    with open("input_dfga_result.txt", "w+", encoding='UTF8') as f:
        f.write("")
    with open("input_dfga_fictional_task_result.txt", "w+", encoding='UTF8') as f:
        f.write("")

    # Get total utils
    original_utils = sum([task.wcet / task.period for task in rt_tasks]) * 1.02
    print("Real time tasks util sum: {}".format(original_utils))
    fictional_util = 0
    margin = (Solution.processor.n_core - original_utils) / df

    # mem_req = max([task.mem_req for task in rt_tasks])
    # mem_util = max([task.mem_active_ratio for task in rt_tasks])
    mem_req = mem_util = 0

    for _ in range(df + 1):
        n_task = math.ceil(fictional_util)
        util_per_task = fictional_util / n_task if n_task else 0
        Solution.rt_tasks = copy.deepcopy(rt_tasks)
        with open("input_dfga_fictional_task_result.txt", "a+", encoding='UTF8') as f:
            f.write("{}\n".format(fictional_util))
            for _ in range(n_task):
                f.write("{} {} {} {}\n".format(math.floor(util_per_task * period - 0.05), period, mem_req, mem_util))
                Solution.rt_tasks.append(RTTask(math.floor(util_per_task * period - 0.05), period, mem_req, mem_util))
            f.write("\n")

        # 1. Make initial solution set
        Solution.set_random_seed()
        solutions = [Solution.get_random_solution(Solution.processor.n_core)
                     for _ in range(ga_configs.POPULATIONS)]
        solutions.sort()  # Sort solutions by score

        for g in range(ga_configs.MAX_GEN):
            if g != 0 and g % 100 == 0:
                report_print("fic{}".format(fictional_util), g, solutions)

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
                if new_solution.check_memory() and new_solution.check_utilization(Solution.processor.n_core):
                    get_new_solution = True
                    break

            if get_new_solution:
                # Replace worst solution into new solution
                solutions[-1] = new_solution
                solutions.sort()
                continue
            else:
                raise Exception("{}번째 generation 이후, solution 교배 불가".format(g + 1))

        # 5. Print result
        flag = False
        for solution in solutions:
            if solution.is_schedule():
                print("========================================================")
                print("fictional tasks util: {}".format(fictional_util))
                print("power: {}, utilization: {}".format(solution.power, solution.utilization))
                print("========================================================")
                with open("input_dfga_result.txt", "a", encoding='UTF8') as f:
                    f.write("{}\n".format(fictional_util))
                    for a, b in zip(solution.genes_processor, solution.genes_memory):
                        f.write("{} {}\n".format(a, b))
                    f.write("\n")
                flag = True
                break
        if not flag:
            raise Exception
        fictional_util += margin

# run()
