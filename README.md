# Documentation

## Problem description

Exact cover problem can be described like: Let we have set $A$ of $n$ elements and set $S$ of subsets of the set $A$. It can satisfy exact cover conditions if we are able to choose elements of $S$ (subsets of $A$) so that they contain every element from set $A$ and every subset has the size of intersection with other chosen subsets equal to 0.

An example of a valid input format is:

```
4
1 2
2 3
3 4
4 1
```

where the first line is the number of elements in set $A$. Next lines are subsets that we are working with. In this case we have subsets of {1st elements; 2nd element}, {2nd; 3rd}, {3rd; 4th} and {4th; 1st}.

The possible solution is to choose 2nd and 4th subset -> they contain every element and size of their intersection is 0.
```
2 4
```

## Encoding

The problem is encoded using variable for every subset that we need to work with. It represents if we need to
include the subset to satisfy exact cover conditions (has value true) or to not include the subset (has value false).

Clauses we need to construct to satisfy the conditions are:

- We need to include every element of $A$: disjunction of every subset that contains the element (at least of 
of the variables must be true -> we need to include at least one subset that includes the element).
- No chosen subset has size of intersection with any other chosen subset grater than 0: From the previous defined 
clause we took every two subsets (variables) and need make sure that just on of them will be chosen (otherwise the 
size of intersection could be grater than 0) -> for every two subsets from clause: -subsetA or -subsetB

It's basically XOR from subsets that contain the element.

## User documentation


Basic usage: 
```
exact_cover.py [-h] [-i INPUT] [-o OUTPUT] [-s SOLVER] [-v {0,1}]
```

Command-line options:

* `-h`, `--help` : Show a help message and exit.
* `-i INPUT`, `--input INPUT` : The instance file. Default: "input.in".
* `-o OUTPUT`, `--output OUTPUT` : Output file for the DIMACS format (i.e. the CNF formula).
* `-s SOLVER`, `--solver SOLVER` : The SAT solver to be used.
*  `-v {0,1}`, `--verb {0,1}` :  Verbosity of the SAT solver used.

## Example instances

* ["satisfiable_human.in"](./instances/satisfiable_human.in): A satisfiable problem, $A$ has 4 elements, there are 4 subsets. Can be solved by human. Very quick.
* ["unsatisfiable_human.in"](./instances/unsatisfiable_human.in): An unsatisfiable problem, $A$ has 4 elements, there are 4 subsets. Can be solved by human. Very quick.
* ["10s_calc_time_satisfiable.in"](./instances/10s_calc_time_satisfiable.in): A satisfiable problem, $A$ has 50 elements, there are 500 subsets. Takes ~10 seconds to calculate.
* ["60s_calc_time_satisfiable.in"](./instances/60s_calc_time_satisfiable.in): A satisfiable problem, $A$ has 50 elements, there is a 1000 subsets. Takes ~60 seconds to calculate.
* ["200_600_unsatisfiable.in"](./instances/200_600_unsatisfiable.in): An unsatisfiable problem, $A$ has 200 elements, there are 600 subsets. Takes ~54 seconds to calculate.
* ["50_200_unsatisfiable.in"](./instances/50_200_unsatisfiable.in): An unsatisfiable problem, $A$ has 50 elements, there are 200 subsets. Takes ~0.8 second to calculate.
* ["20_200_unsatisfiable.in"](./instances/20_200_satisfiable.in): A satisfiable problem, $A$ has 20 elements, there are 200 subsets. Takes ~0.31 second to calculate.

## Experiments

Experiments were run on '11th Gen Intel i7-11370H (8) @ 4.800GHz' and 16 GB RAM on Fedora. Time was measured with python library `time`.

I have created ["generator"](generator.py) for these instances, you can set number of elements in set $A$,
number of subsets and output file (from which ["exact cover"](exact_cover.py) reads). The choosing of contents of
subsets is random.

Times and satisfiability for instances in folder ./instances can be seen in description of these instances above. Time
depends mainly on number of subsets, but also on number of elements. 