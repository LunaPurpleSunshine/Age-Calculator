import argparse
from datetime import date


def calculate_age(birthDate): 
    today = date.today()
    age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day)) 
  
    return age

if __name__ == "__main__":

    parser = argparse.ArgumentParser()

    parser .add_argument("birthdate", nargs=3, help="the birth date of the person to be aged. YYYY MM DD")

    args = parser.parse_args()

    birthday = date(int(args.birthdate[0]), int(args.birthdate[1]), int(args.birthdate[2]))

    age = calculate_age(birthDate=birthday)

    if age >= 0:
        print(f"{age} years old")
    else:
        print(f"{abs(age)} years in the future")

