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

def calculate_calories_for_weight_change(tdee, change):
    return tdee + change

def get_user_choice():
    return input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")

def get_user_input(prompt):
    return int(input(prompt))

def print_result(result, message):
    print(message, result)

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

def calculate_bmi_and_activity():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in meters?")
    bmi = calculate_bmi(weight, height)
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    return bmi, activity

def calculate_bmr_and_activity():
    weight = get_user_input("What is your weight in kg?")
    height = get_user_input("What is your height in cm?")
    age = get_user_input("What is your age in years?")
    bmr = calculate_bmr(weight, height, age)
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    return bmr, activity

def handle_bmi():
    bmi, activity = calculate_bmi_and_activity()
    print_result(bmi, "Your BMI is")

def handle_bmr():
    bmr, activity = calculate_bmr_and_activity()
    print_result(bmr, "Your bmr is")

def handle_tdee():
    bmr, activity = calculate_bmr_and_activity()
    tdee = calculate_tdee(bmr, activity)
    print_result(tdee, "Your tdee is")

def handle_calories_for_weight_change():
    bmr, activity = calculate_bmr_and_activity()
    tdee = calculate_tdee(bmr, activity)
    change = -500
    lose = calculate_calories_for_weight_change(tdee, change)
    print_result(lose, "You need")

def handle_calories_for_weight_gain():
    bmr, activity = calculate_bmr_and_activity()
    tdee = calculate_tdee(bmr, activity)
    change = 500
    gain = calculate_calories_for_weight_change(tdee, change)
    print_result(gain, "You need")

def handle_calories_for_weight_maintenance():
    bmr, activity = calculate_bmr_and_activity()
    tdee = calculate_tdee(bmr, activity)
    print_result(tdee, "You need")

def handle_calculate_everything():
    weight = get_user_input("what is your weight in kg?")
    height = get_user_input("what is your height in cm?")
    age = get_user_input("what is your age in years?")
    cmheight = height / 100
    bmi = calculate_bmi(weight, cmheight)
    bmr = calculate_bmr(weight, height, age)
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9")
    tdee = calculate_tdee(bmr, activity)
    lose = calculate_calories_for_weight_change(tdee, -500)
    gain = calculate_calories_for_weight_change(tdee, 500)
    print_result(bmi, "Your BMI is")
    print_result(bmr, "Your bmr is")
    print_result(tdee, "Your tdee is")
    print_result(lose, "You need")
    print_result(gain, "You need")

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()

def calc():
    choice = get_user_choice()
    if choice == "1":
        handle_bmi()
    elif choice == "2":
        handle_bmr()
    elif choice == "3":
        handle_tdee()
    elif choice == "4":
        handle_calories_for_weight_change()
    elif choice == "5":
        handle_calories_for_weight_gain()
    elif choice == "6":
        handle_calories_for_weight_maintenance()
    elif choice == "7":
        handle_calculate_everything()
    else:
        print("Invalid number, choose a wise one next time")

if __name__ == "__main__":
    run()
