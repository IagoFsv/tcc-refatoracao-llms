"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""

def get_user_input():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def calculate_bmi(weight, height):
    return weight / (height / 100) ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(tdee, change):
    return tdee + change

def display_results(bmi=None, bmr=None, tdee=None, lose=None, gain=None):
    if bmi is not None:
        print("Your BMI is", bmi)
    if bmr is not None:
        print("Your bmr is", bmr)
    if tdee is not None:
        print("Your tdee is", tdee)
    if lose is not None:
        print("You need", lose, "calories to lose weight")
    if gain is not None:
        print("You need", gain, "calories to gain weight")

def ask_to_calculate_again():
    againcalcu = input("Do you want to calculate again? y/n: ")
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

def calculate_bmi_and_activity():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return weight, height, age, activity

def calculate_all():
    weight, height, age, activity = calculate_bmi_and_activity()
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    lose = calculate_calories_needed(tdee, -500)
    gain = calculate_calories_needed(tdee, 500)
    display_results(bmi, bmr, tdee, lose, gain)

def calculate_single_metric(metric):
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    if metric == "bmr":
        bmr = calculate_bmr(weight, height, age)
        display_results(bmr=bmr)
    elif metric == "tdee":
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
        display_results(tdee=tdee)
    elif metric == "lose":
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
        lose = calculate_calories_needed(tdee, -500)
        display_results(lose=lose)
    elif metric == "gain":
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
        gain = calculate_calories_needed(tdee, 500)
        display_results(gain=gain)
    elif metric == "maintain":
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
        display_results(tdee=tdee)

def main():
    while True:
        cal = get_user_input()
        if cal == "1":
            calculate_single_metric("bmi")
        elif cal == "2":
            calculate_single_metric("bmr")
        elif cal == "3":
            calculate_single_metric("tdee")
        elif cal == "4":
            calculate_single_metric("lose")
        elif cal == "5":
            calculate_single_metric("gain")
        elif cal == "6":
            calculate_single_metric("maintain")
        elif cal == "7":
            calculate_all()
        else:
            print("Invalid number, choose a wise one next time")
        
        if not ask_to_calculate_again():
            break

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return main()

if __name__ == "__main__":
    run()
