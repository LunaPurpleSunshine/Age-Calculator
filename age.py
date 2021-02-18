import argparse
from datetime import date


def calculate_age(birthDate):
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))

    return age


if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser.add_argument("year",
                        nargs=1,
                        help="Required. The birth year of the person to be aged. YYYY or YY (assumes 19XX)")
    parser.add_argument("month",
                        nargs="?",
                        default="01",
                        const="01",
                        help="Optional (Default 01). The birth month of the person to be aged. MM")
    parser.add_argument("day",
                        nargs="?",
                        default="01",
                        const="01",
                        help="Optional (Default 01). The birth day of the person to be aged. DD")

    args = parser.parse_args()

    year = args.year[0]

    if len(year) == 2:
        year = int("19" + year)
    elif len(year) == 4:
        year = int(year)
    else:
        raise ValueError

    month = int(args.month)
    day = int(args.day)

    birthday = date(int(year), month, day)

    age = calculate_age(birthDate=birthday)

    if age >= 0:
        print(f"{age} years old today {date.today()}")
        print(f"Will turn {age + 1} on next birthday")
    else:
        print(f"{abs(age)} years in the future")
