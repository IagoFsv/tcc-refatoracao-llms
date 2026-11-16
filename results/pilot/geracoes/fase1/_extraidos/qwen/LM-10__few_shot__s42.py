def _get_user_input():
    return input("Do you want to calculate again? y/n: ")

def _print_separator():
    print("----------------------------------------")

def _get_choice():
    return input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")

def _get_weight():
    return int(input("What is your weight in kg?"))

def _get_height():
    return int(input("What is your height in cm?"))

def _get_age():
    return int(input("What is your age in years?"))

def _get_activity_level():
    return int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))

def _calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def _calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def _calculate_tdee(bmr, activity):
    return bmr * activity

def _calculate_calories_to_lose_weight(tdee):
    return tdee - 500

def _calculate_calories_to_gain_weight(tdee):
    return tdee + 500

def _print_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def _calculate_and_print_all(weight, height, age, activity):
    bmi = _calculate_bmi(weight, height)
    bmr = _calculate_bmr(weight, height, age)
    tdee = _calculate_tdee(bmr, activity)
    lose = _calculate_calories_to_lose_weight(tdee)
    gain = _calculate_calories_to_gain_weight(tdee)
    _print_results(bmi, bmr, tdee, lose, gain)

def _handle_choice(choice, weight, height, age, activity):
    if choice == "1":
        bmi = _calculate_bmi(weight, height)
        print("Your BMI is", bmi)
    elif choice == "2":
        bmr = _calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
    elif choice == "3":
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), activity)
        print("Your tdee is", tdee)
    elif choice == "4":
        lose = _calculate_calories_to_lose_weight(_calculate_tdee(_calculate_bmr(weight, height, age), activity))
        print("You need", lose, "calories to lose weight")
    elif choice == "5":
        gain = _calculate_calories_to_gain_weight(_calculate_tdee(_calculate_bmr(weight, height, age), activity))
        print("You need", gain, "calories to gain weight")
    elif choice == "6":
        print("You need", _calculate_tdee(_calculate_bmr(weight, height, age), activity), "calories to maintain weight")
    elif choice == "7":
        _calculate_and_print_all(weight, height, age, activity)
    else:
        print("Invalid number, choose a wise one next time")

def againcalc():
    againcalcu = _get_user_input()
    _print_separator()
    if againcalcu == "y":
        print("Sure, let's do it again")
        _print_separator()
        calc()
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        _print_separator()
    else:
        print("Invalid input, choose a wise one next time")
        _print_separator()

def calc():
    choice = _get_choice()
    weight = _get_weight()
    height = _get_height()
    age = _get_age()
    activity = _get_activity_level()
    _handle_choice(choice, weight, height, age, activity)
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
