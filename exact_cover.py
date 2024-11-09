import subprocess
import time
from argparse import ArgumentParser


def load_instance(input_file_name):
    # read the input instance
    # the instance is the makespan to be used, the size of the grid, and the placement of tiles in the grid
    # tile 0 is the empty space

    subsets = []
    with open(input_file_name, "r") as file:
        number_of_elements = int(next(file))  # first line is the number of elements
        for line in file:
            if line:
                line = line.split()
                line = [int(i) for i in line]
                subsets.append(line)

    # print(number_of_elements, subsets) # uncomment if you want to see loaded input
    return (subsets, number_of_elements)


def encode(instance):
    # given the instance, create a cnf formula, i.e. a list of lists of integers
    # also return the total number of variables used

    subsets = instance[0]
    number_of_elements = instance[1]
    number_of_vars = len(subsets)

    cnf = []

    # every element is covered in subsets
    for element in range(1, number_of_elements + 1):
        clause = []
        for var, subset in enumerate(subsets):
            if element in subset:
                clause.append(var + 1)  # variable numbers start at 1
        if clause:
            cnf.append(clause)

    # no elements is in several chosen subsets
    for element in range(1, number_of_elements + 1):
        relevant_vars = [var + 1 for var, subset in enumerate(subsets) if element in subset]
        for i in range(len(relevant_vars)):
            for j in range(i + 1, len(relevant_vars)):
                cnf.append([-relevant_vars[i], -relevant_vars[j]])

    # print(cnf) # uncomment if you want to see clauses
    return (cnf, number_of_vars)


def call_solver(cnf, nr_vars, output_name, solver_name, verbosity):
    # print CNF into formula.cnf in DIMACS format
    with open(output_name, "w") as file:
        file.write("p cnf " + str(nr_vars) + " " + str(len(cnf)) + '\n')
        for clause in cnf:
            file.write(' '.join(str(lit) for lit in clause) + ' 0\n')

    # call the solver and return the output
    return subprocess.run(['./' + solver_name, '-model', '-verb=' + str(verbosity), output_name],
                          stdout=subprocess.PIPE)


def print_result(result):
    for line in result.stdout.decode('utf-8').split('\n'):
        print(line)  # print the whole output of the SAT solver to stdout, so you can see the raw output for yourself

    # check the returned result
    if (result.returncode == 20):  # returncode for SAT is 10, for UNSAT is 20
        return

    # parse the model from the output of the solver
    # the model starts with 'v'
    model = []
    for line in result.stdout.decode('utf-8').split('\n'):
        if line.startswith("v"):  # there might be more lines of the model, each starting with 'v'
            vars = line.split(" ")
            vars.remove("v")
            model.extend(int(v) for v in vars)
    model.remove(0)  # 0 is the end of the model, just ignore it

    print()
    print("##########################################################################")
    print("###########[ Human readable result of the exact cover problem ]###########")
    print("##########################################################################")
    print()

    # decode the meaning of the assignment
    print("To satisfy exact cover problem conditions choose this subsets:")
    print("|", end="")
    for var in model:
        if var > 0:
            print(f" {var} |", end="")
    print()


if __name__ == "__main__":
    start_time = time.time()

    parser = ArgumentParser()

    parser.add_argument(
        "-i",
        "--input",
        default="input.in",
        type=str,
        help=(
            "The instance file."
        ),
    )
    parser.add_argument(
        "-o",
        "--output",
        default="formula.cnf",
        type=str,
        help=(
            "Output file for the DIMACS format (i.e. the CNF formula)."
        ),
    )
    parser.add_argument(
        "-s",
        "--solver",
        default="glucose-syrup",
        type=str,
        help=(
            "The SAT solver to be used."
        ),
    )
    parser.add_argument(
        "-v",
        "--verb",
        default=1,
        type=int,
        choices=range(0, 2),
        help=(
            "Verbosity of the SAT solver used."
        ),
    )
    args = parser.parse_args()

    # get the input instance
    instance = load_instance(args.input)

    # encode the problem to create CNF formula
    cnf, nr_vars = encode(instance)

    # call the SAT solver and get the result
    result = call_solver(cnf, nr_vars, args.output, args.solver, args.verb)

    # interpret the result and print it in a human-readable format
    print_result(result)

    end_time = time.time()
    print (f"\nAnd it took {end_time-start_time:.2f} seconds to calculate!")
