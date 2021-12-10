import fileinput
import re

REQUIRED_FIELDS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL_FIELDS = {"cid"}

RE = re.compile("()")

if __name__ == "__main__":

    passports = []
    full_input = "".join(fileinput.input())
    match = RE.findall(full_input)
    print(match)
    print(full_input)

    valid_passports = [
        passport
        for passport in passports
        if not REQUIRED_FIELDS.difference(passport)
    ]
    print("Part 1:", len(valid_passports))

