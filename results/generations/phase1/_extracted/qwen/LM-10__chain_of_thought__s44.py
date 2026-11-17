"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def get_user_input():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
    return bmi

def calculate_bmr(weight, height, age):
    bmr = 10 * weight + 6.25 * height - 5 * age
    return bmr

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_for_weight_change(bmr, activity, change):
    tdee = calculate_tdee(bmr, activity)
    return tdee + change

def display_results(cal, bmi=None, bmr=None, tdee=None, lose=None, gain=None):
    if cal == "1":
        print("Your BMI is", bmi)
    elif cal == "2":
        print("Your bmr is", bmr)
    elif cal == "3":
        print("Your tdee is", tdee)
    elif cal == "4":
        print("You need", lose, "calories to lose weight")
    elif cal == "5":
        print("You need", gain, "calories to gain weight")
    elif cal == "6":
        print("You need", tdee, "calories to maintain weight")
    elif cal == "7":
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
        run()
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calc():
    cal = get_user_input()
    if cal == "1":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        bmi = calculate_bmi(weight, height)
        display_results(cal, bmi=bmi)
    elif cal == "2":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        display_results(cal, bmr=bmr)
    elif cal == "3":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        display_results(cal, tdee=tdee)
    elif cal == "4":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_for_weight_change(bmr, activity, -500)
        display_results(cal, lose=lose)
    elif cal == "5":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        gain = calculate_calories_for_weight_change(bmr, activity, 500)
        display_results(cal, gain=gain)
    elif cal == "6":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        display_results(cal, tdee=tdee)
    elif cal == "7":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_for_weight_change(bmr, activity, -500)
        gain = calculate_calories_for_weight_change(bmr, activity, 500)
        display_results(cal, bmi=calculate_bmi(weight, height), bmr=bmr, tdee=tdee, lose=lose, gain=gain)
    else:
        print("Invalid number, choose a wise one next time")

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()

if __name__ == "__main__":
    run()
