def part_1(readings):
    depth = 0
    horizontal = 0
    for direction, amount in readings:
        if direction == "forward":
            horizontal += amount
        elif direction == "up":
            depth -= amount
        elif direction == "down":
            depth += amount

    product = depth * horizontal
    return (depth, horizontal, product)


def part_2(readings):
    aim = 0
    depth = 0
    horizontal = 0
    for direction, amount in readings:
        if direction == "forward":
            horizontal += amount
            depth += amount * aim
        elif direction == "up":
            aim -= amount
        elif direction == "down":
            aim += amount

    product = depth * horizontal
    return (depth, horizontal, product)



if __name__ == "__main__":

    with open("input.txt", "r") as f:
        readings = [
            (direction, int(amount))
            for l in f.readlines()
            for direction, amount in [l.split()]
        ]

    print(part_1(readings))
    print(part_2(readings))
    
