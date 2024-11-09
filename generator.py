import random

def generate_exact_cover_input(number_of_elements, number_of_subsets, output_file):
    subsets = []
    elements = list(range(1, number_of_elements + 1))

    for _ in range(number_of_subsets):
        subset_size = random.randint(1, max(1, number_of_elements // 2))
        subset = random.sample(elements, subset_size)
        subsets.append(subset)

    with open(output_file, "w") as file:
        file.write(f"{number_of_elements}\n")
        for subset in subsets:
            file.write(" ".join(map(str, subset)) + "\n")

if __name__ == "__main__":
    generate_exact_cover_input(number_of_elements=20, number_of_subsets=200, output_file="instances/name.in")