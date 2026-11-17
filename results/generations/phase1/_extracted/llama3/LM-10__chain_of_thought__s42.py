"""Fitness calculator (BMI, BMR, daily expenditure and calories).

Public entry point: run(). Do not change its name or signature; the rest of
the file may be freely reorganized.
"""


def againcalc():
    againcalcu=input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu== "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif againcalcu== "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calculate_bmi(weight, height):
    bmi = weight / (height ** 2)
    print("Your BMI is", bmi)
    againcalc()

def calculate_bmr(weight, height, age):
    bmr = 10 * weight + 6.25 * height - 5 * age
    print("Your BMR is", bmr)
    againcalc()

def calculate_tdee(weight, height, age, activity):
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    print("Your TDEE is", tdee)
    againcalc()

def calculate_calories_needed_to_lose_weight(weight, height, age, activity):
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    lose = tdee - 500
    print("You need", lose, "calories to lose weight")
    againcalc()

def calculate_calories_needed_to_gain_weight(weight, height, age, activity):
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    gain = tdee + 500
    print("You need", gain, "calories to gain weight")
    againcalc()

def calculate_calories_needed_to_maintain_weight(weight, height, age, activity):
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    print("You need", tdee, "calories to maintain weight")
    againcalc()

def calculate_everything_from_bmi_and_activity_level(weight, height, age, activity):
    cmheight = height / 100
    bmi = weight / (cmheight ** 2)
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    lose = tdee - 500
    gain = tdee + 500
    print("Your BMI is", bmi)
    print("Your BMR is", bmr)
    print("Your TDEE is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")
    againcalc()

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()


def calc():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal== "1":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
        calculate_bmi(weight, height)
        
    elif cal== "2":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        calculate_bmr(weight, height, age)
        
    elif cal== "3":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calculate_tdee(weight, height, age, activity)
        
    elif cal== "4":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calculate_calories_needed_to_lose_weight(weight, height, age, activity)
        
    elif cal== "5":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calculate_calories_needed_to_gain_weight(weight, height, age, activity)
        
    elif cal== "6":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        calculate_calories_needed_to_maintain_weight(weight, height, age)
        
    elif cal== "7":
        weight=int(input("what is your weight in kg?"))
        height=int(input("what is your height in cm?"))
        age=int(input("what is your age in years?"))
        calculate_everything_from_bmi_and_activity_level(weight, height, age)
        
    else:
        print("Invalid number, choose a wise one next time")


if __name__ == "__main__":
    run()
