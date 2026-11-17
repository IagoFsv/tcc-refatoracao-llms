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

def ask_user_for_choice():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def ask_user_for_weight_and_height(cal):
    if cal == "1" or cal == "7":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
    else:
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
    return weight, height

def ask_user_for_age_and_activity(cal):
    if cal == "2" or cal == "3" or cal == "4" or cal == "5" or cal == "6":
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    else:
        activity=0
        age=0
    return age, activity

def calculate_bmi(weight, height):
    bmi=weight/height**2
    return bmi

def calculate_bmr(weight, height, age):
    bmr=10*weight+6.25*height-5*age
    return bmr

def calculate_tdee(bmr, activity):
    tdee=bmr*activity
    return tdee

def calculate_calories_needed_to_lose_weight(tdee):
    lose=tdee-500
    return lose

def calculate_calories_needed_to_gain_weight(tdee):
    gain=tdee+500
    return gain

def calculate_calories_needed_to_maintain_weight(tdee):
    return tdee

def print_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def print_bmi_only(bmi):
    print("Your BMI is", bmi)

def calc():
    cal=ask_user_for_choice()
    if cal== "1":
        weight, height=ask_user_for_weight_and_height(cal)
        bmi=calculate_bmi(weight, height)
        print_results(bmi, 0, 0, 0, 0)
        againcalc()
        
    elif cal== "2":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        bmr=calculate_bmr(weight, height, age)
        print_results(0, bmr, 0, 0, 0)
        againcalc()
        
    elif cal== "3":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        print_results(0, 0, tdee, 0, 0)
        againcalc()
        
    elif cal== "4":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        lose=calculate_calories_needed_to_lose_weight(tdee)
        print_results(0, 0, tdee, lose, 0)
        againcalc()
        
    elif cal== "5":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        gain=calculate_calories_needed_to_gain_weight(tdee)
        print_results(0, 0, tdee, 0, gain)
        againcalc()
        
    elif cal== "6":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        print_results(0, 0, tdee, 0, 0)
        againcalc()
        
    elif cal== "7":
        weight, height=ask_user_for_weight_and_height(cal)
        age=int(input("What is your age in years?"))
        bmi=calculate_bmi(weight, height)
        bmr=calculate_bmr(weight, height, age)
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee=calculate_tdee(bmr, activity)
        lose=calculate_calories_needed_to_lose_weight(tdee)
        gain=calculate_calories_needed_to_gain_weight(tdee)
        print_results(bmi, bmr, tdee, lose, gain)
        againcalc()
        
    else:
        print("Invalid number, choose a wise one next time")


def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()


if __name__ == "__main__":
    run()
