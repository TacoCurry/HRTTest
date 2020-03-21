def first_print(max_core, min_core, file="input_ga_result.txt"):
    with open(file, "a", encoding='UTF8') as f:
        f.write("{} {}\n".format(max_core, min_core))
    return True


def result_print(n_core, solution, file="input_ga_result.txt"):
    with open(file, "a", encoding='UTF8') as f:
        f.write("{}\n".format(n_core))
        for a, b in zip(solution.genes_processor, solution.genes_memory):
            f.write("{} {}\n".format(a, b))
        f.write("\n")
    return True


def init_out(file="input_ga_result.txt"):
    with open(file, "w+", encoding='UTF8') as f:
        f.write("\n")


def report_print(core_max, n_generation, solutions):
    file = "report{}.txt".format(core_max)

    power_min = power_max = power_sum = solutions[0].power
    util_min = util_max = util_sum = solutions[0].utilization

    for solution in solutions[1:]:
        power_sum += solution.power
        util_sum += solution.utilization

        if solution.power > power_max:
            power_max = solution.power
        elif solution.power < power_min:
            power_min = solution.power

        if solution.utilization > util_max:
            util_max = solution.utilization
        elif solution.utilization < util_min:
            util_min = solution.utilization

    power_avg = power_sum / len(solutions)
    util_avg = util_sum / len(solutions)

    with open(file, "a", encoding='UTF8') as f:
        f.write("generation: {}, power_min: {}, power_avg: {}, power_max: {}, "
                "util_min: {}, util_avg: {}, util_max: {}\n".format(n_generation, round(power_min, 5),
                                                                    round(power_avg, 5), round(power_max, 5),
                                                                    round(util_min, 5), round(util_avg, 5),
                                                                    round(util_max, 5)))