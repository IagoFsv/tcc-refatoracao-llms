"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def _get_user_input():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def _get_bmi_data():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in meters?"))
    return weight, height

def _get_bmr_data():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    return weight, height, age

def _get_activity_level():
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return activity

def _calculate_bmi(weight, height):
    return weight / height ** 2

def _calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def _calculate_tdee(bmr, activity):
    return bmr * activity

def _calculate_calories_for_loss(tdee):
    return tdee - 500

def _calculate_calories_for_gain(tdee):
    return tdee + 500

def _print_summary(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def _ask_to_calculate_again():
    againcalcu = input("Do you want to calculate again? y/n: ")
    if againcalcu == "y":
        print("Sure, let's do it again")
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
    else:
        print("Invalid input, choose a wise one next time")

def _run_calculator():
    cal = _get_user_input()
    
    if cal == "1":
        weight, height = _get_bmi_data()
        bmi = _calculate_bmi(weight, height)
        _print_summary(bmi, None, None, None, None)
    elif cal == "2":
        weight, height, age = _get_bmr_data()
        bmr = _calculate_bmr(weight, height, age)
        _print_summary(None, bmr, None, None, None)
    elif cal == "3":
        weight, height, age = _get_bmr_data()
        activity = _get_activity_level()
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        _print_summary(None, None, tdee, None, None)
    elif cal == "4":
        weight, height, age = _get_bmr_data()
        activity = _get_activity_level()
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        lose = _calculate_calories_for_loss(tdee)
        _print_summary(None, None, None, lose, None)
    elif cal == "5":
        weight, height, age = _get_bmr_data()
        activity = _get_activity_level()
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        gain = _calculate_calories_for_gain(tdee)
        _print_summary(None, None, None, None, gain)
    elif cal == "6":
        weight, height, age = _get_bmr_data()
        activity = _get_activity_level()
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        _print_summary(None, None, None, None, tdee)
    elif cal == "7":
        weight, height, age = _get_bmr_data()
        cmheight = height / 100
        bmi = _calculate_bmi(weight, cmheight)
        activity = _get_activity_level()
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        lose = _calculate_calories_for_loss(tdee)
        gain = _calculate_calories_for_gain(tdee)
        _print_summary(bmi, _calculate_bmr(weight, height, age), tdee, lose, gain)
    else:
        print("Invalid number, choose a wise one next time")

def againcalc():
    _run_calculator()
    _ask_to_calculate_again()

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    againcalc()


if __name__ == "__main__":
    run()
