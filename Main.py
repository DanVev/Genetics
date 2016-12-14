import random as rn
import itertools as it

NUMBER_OF_ITEMS = 15
NUMBER_OF_ITERATIONS = 10
WEIGHT = rn.randint(40, 60)
MUTATION_PROBABILITY = 0.01
weight_list = [rn.randint(1, 10) for i in range(NUMBER_OF_ITEMS)]
cost_list = [rn.randint(1, 10) for i in range(NUMBER_OF_ITEMS)]
POP_SIZE = 75
EXP_NUMBER = 5
RECREATION_NUMBER = 30


def decode(code):
    while WEIGHT < weight(code):
        code[(min([(i, cost_list[i]) for i in range(NUMBER_OF_ITEMS) if code[i] != 0], key=lambda x: x[1])[0])] = 0


def p(ver):
    return ver >= rn.random()


def weight(code):
    return sum(map(lambda x, y: x * y, code, weight_list))


def criteria(code):
    return sum(map(lambda x, y: x * y, code, cost_list))


def choice(seq, p_list):
    while True:
        for index in range(len(seq)):
            if p(p_list[index]):
                return seq[index]


def initialize_1(_pop_size):
    """Случайный метод генерации популяции"""
    pop = []
    for i in range(_pop_size):
        code = [0] * NUMBER_OF_ITEMS
        for pos in range(NUMBER_OF_ITEMS):
            if weight(code) < WEIGHT + weight_list[pos]:
                code[pos] = rn.randint(0, 1)
        pop.append(code)
    return pop


def initialize_2(_pop_size):
    pop = []
    cost_sum = sum(cost_list)
    while len(pop) < _pop_size:
        code = [0] * NUMBER_OF_ITEMS
        for i in range(5):
            for pos in range(NUMBER_OF_ITEMS):
                if weight(code) < WEIGHT + weight_list[pos] and p(
                                cost_list[pos] / cost_sum):
                    code[pos] = 1
            pop.append(code)
    return pop


def select_pairs1(_population, limit=POP_SIZE):
    return [(rn.choice(_population), rn.choice(_population)) for i in range(limit)]


def select_pairs2(_population, limit=POP_SIZE):
    crit_list = [criteria(code) for code in _population]
    crit_sum = sum(crit_list)
    crit_list = list(map(lambda x: x / crit_sum, crit_list))
    return [(choice(_population, crit_list), choice(_population, crit_list)) for i in range(limit)]


def crossover1(pair):
    cr1, cr2 = pair
    middle = round(NUMBER_OF_ITEMS / 2)
    return cr1[:middle] + cr2[middle:]


def crossover2(pair):
    cr1, cr2 = pair
    return [rn.choice(x) for x in zip(cr1, cr2)]


def mutate1(population):
    index = rn.randint(0, len(population) - 1)
    code = population[index]
    while True:
        position = rn.randint(0, len(code) - 1)
        code[position] = 1 - code[position]
        if weight(code) > WEIGHT:
            code[position] = 1 - code[position]
        else:
            break
    population[index] = code


def mutate2(population):
    index = rn.randint(0, len(population) - 1)
    code = population[index]
    pos1, pos2 = rn.randint(0, NUMBER_OF_ITEMS - 1), rn.randint(0, NUMBER_OF_ITEMS - 1)
    code[pos1], code[pos2] = code[pos2], code[pos1]


def selection1(_population):
    crit_list = [criteria(code) for code in _population]
    crit_sum = sum(crit_list)
    crit_list = list(map(lambda x: x / crit_sum, crit_list))
    i = 0
    while len(_population) != POP_SIZE:
        if p(1 - crit_list[i]):
            _population.pop(i)
        i = (i + 1) // len(_population)


def selection2(_population):
    while len(_population) != POP_SIZE:
        index1, index2 = rn.randint(0, len(_population) - 1), rn.randint(0, len(_population) - 1)
        crit1, crit2 = criteria(_population[index1]), criteria(_population[index2])
        crit_sum = crit1 + crit2
        if not crit_sum:
            crit1 = 1
            crit2 = 1
            crit_sum = 2
        if p(1 - crit1 / crit_sum):
            _population.pop(index1)
        elif p(1 - crit2 / crit_sum):
            _population.pop(index2)


def selection3(_population):
    while len(_population) != POP_SIZE:
        index1, index2 = rn.randint(0, len(_population) - 1), rn.randint(0, len(_population) - 1)
        if criteria(_population[index1]) > criteria((_population[index2])):
            _population.pop(index2)
        else:
            _population.pop(index1)


for initialize in initialize_1, initialize_2:
    for select_pairs in select_pairs1, select_pairs2:
        for mutate in mutate1, mutate2:
            for crossover in crossover1, crossover2:
                for selection in selection1, selection2, selection3:
                    exp_results = []
                    print("Начальная популяция " + str(initialize.__name__),
                          "Выбор пары: " + str(select_pairs.__name__),
                          "Кроссовер: " + str(crossover.__name__), "Селекция: " + str(selection.__name__), sep="\n")
                    for exp_number in range(EXP_NUMBER):
                        stage_results = []
                        population = initialize(POP_SIZE)
                        for step_number in range(1, NUMBER_OF_ITERATIONS + 1):
                            for code in population:
                                assert len(code) == 15

                            # recreation stage
                            for pair in select_pairs(population,
                                                     rn.randint(RECREATION_NUMBER - 5, RECREATION_NUMBER + 5)):
                                population.append(crossover(pair))
                            # mutation stage
                            if p(MUTATION_PROBABILITY):
                                mutate(population)
                            # decoding stage
                            for code in population:
                                decode(code)
                            # selection stage
                            selection(population)
                            # output stage
                            stage_results.append(criteria(max(population, key=criteria)))
                            # print("Локальный максимум на этапе {} равен {}".format(step_number, criteria(
                            #    max(population, key=criteria))))
                        exp_results.append((stage_results[-1] - stage_results[0]) / stage_results[0])
                    print(" ".join([str(int(100 * x)) + "%" for x in exp_results]))
