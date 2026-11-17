def bmi_calculator(weight, height):
    return weight / height ** 2

def bmr_calculator(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def tdee_calculator(bmr, activity):
    return bmr * activity

def calorie_calculator(bmr, activity, goal):
    if goal == "lose":
        return bmr * activity - 500
    elif goal == "gain":
        return bmr * activity + 500
    else:
        return bmr * activity

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal == "1":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in meters?"))
        print("Your BMI is", bmi_calculator(weight, height))
        againcalc()

    elif cal == "2":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        print("Your bmr is", bmr_calculator(weight, height, age))
        againcalc()

    elif cal == "3":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        print("Your tdee is", tdee_calculator(bmr_calculator(weight, height, age), activity))
        againcalc()

    elif cal == "4":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        print("You need", calorie_calculator(bmr_calculator(weight, height, age), activity, "lose"), "calories to lose weight")
        againcalc()

    elif cal == "5":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        print("You need", calorie_calculator(bmr_calculator(weight, height, age), activity, "gain"), "calories to gain weight")
        againcalc()

    elif cal == "6":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        print("You need", tdee_calculator(bmr_calculator(weight, height, age), activity), "calories to maintain weight")
        againcalc()

    elif cal == "7":
        weight = int(input("what is your weight in kg?"))
        height = int(input("what is your height in cm?"))
        age = int(input("what is your age in years?"))
        cmheight = height / 100
        bmi = bmi_calculator(weight, cmheight)
        bmr = bmr_calculator(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = tdee_calculator(bmr, activity)
        lose = calorie_calculator(bmr, activity, "lose")
        gain = calorie_calculator(bmr, activity, "gain")
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
    return calc()


if __name__ == "__main__":
    run()
