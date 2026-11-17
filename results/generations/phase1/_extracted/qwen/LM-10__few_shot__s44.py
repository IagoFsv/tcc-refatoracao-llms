"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def _get_user_input(prompt):
    return input(prompt)

def _calculate_bmi(weight, height):
    return weight / height ** 2

def _calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def _calculate_tdee(bmr, activity):
    return bmr * activity

def _calculate_calories_to_lose_weight(tdee):
    return tdee - 500

def _calculate_calories_to_gain_weight(tdee):
    return tdee + 500

def _display_result(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def _ask_to_calculate_again():
    againcalcu = _get_user_input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        return True
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
        return False
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")
        return False

def _get_activity_level():
    return int(_get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))

def _get_weight_and_height():
    weight = int(_get_user_input("What is your weight in kg?"))
    height = int(_get_user_input("What is your height in cm?"))
    return weight, height

def _get_age():
    return int(_get_user_input("What is your age in years?"))

def _get_calculation_choice():
    return _get_user_input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")

def _perform_calculation(choice, weight, height, age, activity=None):
    if choice == "1":
        bmi = _calculate_bmi(weight, height)
        print("Your BMI is", bmi)
    elif choice == "2":
        bmr = _calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
    elif choice == "3":
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
    elif choice == "4":
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, activity)
        lose = _calculate_calories_to_lose_weight(tdee)
        print("You need", lose, "calories to lose weight")
    elif choice == "5":
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, activity)
        gain = _calculate_calories_to_gain_weight(tdee)
        print("You need", gain, "calories to gain weight")
    elif choice == "6":
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, activity)
        print("You need", tdee, "calories to maintain weight")
    elif choice == "7":
        bmi = _calculate_bmi(weight, height)
        bmr = _calculate_bmr(weight, height, age)
        activity = _get_activity_level()
        tdee = _calculate_tdee(bmr, activity)
        lose = _calculate_calories_to_lose_weight(tdee)
        gain = _calculate_calories_to_gain_weight(tdee)
        _display_result(bmi, bmr, tdee, lose, gain)
    else:
        print("Invalid number, choose a wise one next time")

def calc():
    choice = _get_calculation_choice()
    weight, height = _get_weight_and_height()
    age = _get_age()
    if choice in ["1", "2", "3", "6"]:
        activity = _get_activity_level()
    _perform_calculation(choice, weight, height, age, activity)

def againcalc():
    if _ask_to_calculate_again():
        calc()

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    calc()


if __name__ == "__main__":
    run()
