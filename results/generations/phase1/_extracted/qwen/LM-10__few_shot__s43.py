"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    activities = {
        1: 1.2,
        2: 1.375,
        3: 1.55,
        4: 1.725,
        5: 1.9
    }
    return bmr * activities.get(activity, 1)

def calculate_calories_needed_for_loss(tdee):
    return tdee - 500

def calculate_calories_needed_for_gain(tdee):
    return tdee + 500

def display_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def display_single_result(value, label):
    print(f"{label}: {value}")

def get_user_choice():
    return input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")

def get_user_input(prompt):
    return int(input(prompt))

def calculate_and_display_bmi():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    bmi = calculate_bmi(weight, height)
    display_single_result(bmi, "Your BMI")

def calculate_and_display_bmr():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    bmr = calculate_bmr(weight, height, age)
    display_single_result(bmr, "Your bmr")

def calculate_and_display_tdee():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
    display_single_result(tdee, "Your tdee")

def calculate_and_display_calories_needed_for_loss():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
    lose = calculate_calories_needed_for_loss(tdee)
    display_single_result(lose, "Calories needed to lose weight")

def calculate_and_display_calories_needed_for_gain():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
    gain = calculate_calories_needed_for_gain(tdee)
    display_single_result(gain, "Calories needed to gain weight")

def calculate_and_display_everything():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    lose = calculate_calories_needed_for_loss(tdee)
    gain = calculate_calories_needed_for_gain(tdee)
    display_results(bmi, bmr, tdee, lose, gain)

def get_user_decision():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    return againcalcu

def againcalc():
    decision = get_user_decision()
    if decision == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif decision == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calc():
    cal = get_user_choice()
    if cal == "1":
        calculate_and_display_bmi()
    elif cal == "2":
        calculate_and_display_bmr()
    elif cal == "3":
        calculate_and_display_tdee()
    elif cal == "4":
        calculate_and_display_calories_needed_for_loss()
    elif cal == "5":
        calculate_and_display_calories_needed_for_gain()
    elif cal == "6":
        calculate_and_display_calories_needed_for_gain()
    elif cal == "7":
        calculate_and_display_everything()
    else:
        print("Invalid number, choose a wise one next time")

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()


if __name__ == "__main__":
    run()
