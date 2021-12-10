import fileinput


if __name__ == "__main__":

    signals_and_outputs = [
        [scrambled.split(" "), outputs.split(" ")]
        for line in fileinput.input()
        for scrambled, outputs in (line.strip().split(" | "),)
    ]

    total = 0
    for signals, outputs in signals_and_outputs:
        length_to_segments = {len(signal): set(signal) for signal in signals}

        number = ""
        for output in map(set, outputs):
            if len(output) == 2:
                number += "1"
            elif len(output) == 3:
                number += "7"
            elif len(output) == 4:
                number += "4"
            elif len(output) == 7:
                number += "8"
            elif len(output) == 5:  # Could be 2, 3, 5
                # Only the digit 2 shares 3 segments with the digit 4
                # Of 3 and 5, only 3 shares 2 segments with the digit 1
                if len(output & length_to_segments[4]) == 2:
                    number += "2"
                elif len(output & length_to_segments[2]) == 2:
                    number += "3"
                else:
                    number += "5"
            elif len(output) == 6:  # Could be 0, 6, 9
                # Only the digit 9 shares 4 segments with the digit 4
                # Of 0 and 6, only 0 shares 2 segments with the digit 1
                if len(output & length_to_segments[4]) == 4:
                    number += "9"
                elif len(output & length_to_segments[2]) == 2:
                    number += "0"
                else:
                    number += "6"
        total += int(number)

    print("Part 2:", total)

