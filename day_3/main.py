def part_one(rows):
    print("Part 1:")

    count_of_ones = calc_count_of_ones(rows)
    goal = len(rows) / 2

    gamma = ""
    epsilon = ""
    for d in count_of_ones:
        if d > goal:
            gamma += "1"
            epsilon += "0"
        else:
            gamma += "0"
            epsilon += "1"
    
    gamma_10 = int(gamma, 2)
    epsilon_10 = int(epsilon, 2)
    power_consumption = gamma_10 * epsilon_10

    print(gamma, gamma_10)
    print(epsilon, epsilon_10)
    print(power_consumption)


def calc_count_of_ones(rows):
    count_of_ones = [0 for _ in range(len(rows[0]))]

    for row in rows:
        for i, digit in enumerate(row):
            if digit == "1":
                count_of_ones[i] += 1

    return count_of_ones


def filter_rows(rows, half_to_one=True):
    rows = list(rows)

    i = 0
    while (total_rows := len(rows)) > 1:
        goal = total_rows / 2
        count_of_ones = calc_count_of_ones(rows)

        if half_to_one:
            goal_digit = "1" if count_of_ones[i] >= goal else "0"
        else:
            goal_digit = "0" if count_of_ones[i] >= goal else "1"

        rows = [
            row
            for row in rows
            if row[i] == goal_digit
        ]
        i += 1
    return rows[0]


def part_two(rows):
    print("Part 2:")
    oxygen_bin = "".join(filter_rows(rows, half_to_one=True))
    oxygen_dec = int(oxygen_bin, 2)
    print("oxygen", oxygen_bin, oxygen_dec)

    co2_bin = "".join(filter_rows(rows, half_to_one=False))
    co2_dec = int(co2_bin, 2)
    print("co2", co2_bin, co2_dec)
   
    print(oxygen_dec * co2_dec)

if __name__ == "__main__":
    with open("input.txt", "r") as f:
        rows = [r.strip() for r in f.readlines()]

    part_one(rows)
    print()
    part_two(rows)
