def againcalc():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def get_choice():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def get_weight_height_age():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    return weight, height, age

def get_activity_level():
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return activity

def calculate_bmi(weight, height):
    cmheight = height / 100
    bmi = weight / cmheight ** 2
    return bmi

def calculate_bmr(weight, height, age):
    bmr = 10 * weight + 6.25 * height - 5 * age
    return bmr

def calculate_tdee(bmr, activity):
    tdee = bmr * activity
    return tdee

def calculate_calories_needed_to_lose_gain_maintain(tdee):
    lose = tdee - 500
    gain = tdee + 500
    return lose, gain

def calculate_and_display_results(cal, weight, height, age, activity):
    if cal == "1":
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
        againcalc()
    elif cal == "2":
        bmr = calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
        againcalc()
    elif cal == "3":
        bmr = calculate_bmr(weight, height, age)
        activity = get_activity_level()
        tdee = calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
        againcalc()
    elif cal == "4":
        bmr = calculate_bmr(weight, height, age)
        activity = get_activity_level()
        tdee = calculate_tdee(bmr, activity)
        lose, gain = calculate_calories_needed_to_lose_gain_maintain(tdee)
        print("You need", lose, "calories to lose weight")
        againcalc()
    elif cal == "5":
        bmr = calculate_bmr(weight, height, age)
        activity = get_activity_level()
        tdee = calculate_tdee(bmr, activity)
        gain, lose = calculate_calories_needed_to_lose_gain_maintain(tdee)
        print("You need", gain, "calories to gain weight")
        againcalc()
    elif cal == "6":
        bmr = calculate_bmr(weight, height, age)
        activity = get_activity_level()
        tdee = calculate_tdee(bmr, activity)
        print("You need", tdee, "calories to maintain weight")
        againcalc()
    elif cal == "7":
        weight, height, age = get_weight_height_age()
        cmheight = height / 100
        bmi = weight / cmheight ** 2
        bmr = calculate_bmr(weight, height, age)
        activity = get_activity_level()
        tdee = calculate_tdee(bmr, activity)
        lose, gain = calculate_calories_needed_to_lose_gain_maintain(tdee)
        print("Your BMI is", bmi)
        print("Your bmr is", bmr)
        print("Your tdee is", tdee)
        print("You need", lose, "calories to lose weight")
        print("You need", gain, "calories to gain weight")
        print("You need", tdee, "calories to maintain weight")
        againcalc()
    else:
        print("Invalid number, choose a wise one next time")


def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    calc()
    return


if __name__ == "__main__":
    run()
