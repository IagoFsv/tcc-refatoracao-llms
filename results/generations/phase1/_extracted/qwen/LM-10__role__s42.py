"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def calculate_bmi(weight, height):
    return weight / height ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(tdee, change):
    return tdee + change

def display_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def againcalc():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calculate_and_display(choice, weight, height, age, activity):
    if choice == "1":
        bmi = calculate_bmi(weight, height)
        display_results(bmi, None, None, None, None)
    elif choice == "2":
        bmr = calculate_bmr(weight, height, age)
        display_results(None, bmr, None, None, None)
    elif choice == "3":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        display_results(None, None, tdee, None, None)
    elif choice == "4":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_needed(tdee, -500)
        display_results(None, None, None, lose, None)
    elif choice == "5":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        gain = calculate_calories_needed(tdee, 500)
        display_results(None, None, None, None, gain)
    elif choice == "6":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        display_results(None, None, None, None, tdee)
    elif choice == "7":
        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_needed(tdee, -500)
        gain = calculate_calories_needed(tdee, 500)
        display_results(bmi, bmr, tdee, lose, gain)
    else:
        print("Invalid number, choose a wise one next time")

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    if cal == "2":
        height = height / 100
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    calculate_and_display(cal, weight, height, age, activity)
    againcalc()

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()


if __name__ == "__main__":
    run()
