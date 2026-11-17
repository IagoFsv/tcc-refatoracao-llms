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

def _get_user_input(cal_choice):
    if cal_choice == "1":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
        return weight, height
    elif cal_choice == "2":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal_choice == "3":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        return weight, height, age, activity
    elif cal_choice == "4":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        return weight, height, age, activity
    elif cal_choice == "5":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        return weight, height, age, activity
    elif cal_choice == "6":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal_choice == "7":
        weight=int(input("what is your weight in kg?"))
        height=int(input("what is your height in cm?"))
        age=int(input("what is your age in years?"))
        return weight, height, age
    else:
        print("Invalid number, choose a wise one next time")

def _calculate_bmi(weight, height):
    cmheight=height/100
    bmi=weight/cmheight**2
    return bmi

def _calculate_bmr(weight, height, age):
    bmr=10*weight+6.25*height-5*age
    return bmr

def _calculate_tdee(bmr, activity):
    tdee=bmr*activity
    return tdee

def _calculate_calories(weight, height, age, activity):
    tdee=_calculate_tdee(_calculate_bmr(weight, height, age), activity)
    lose=tdee-500
    gain=tdee+500
    return lose, gain, tdee

def calc():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal== "1":
        weight, height = _get_user_input(cal)
        bmi = _calculate_bmi(weight, height)
        print("Your BMI is", bmi)
        againcalc()
        
    elif cal== "2":
        weight, height, age = _get_user_input(cal)
        bmr = _calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
        againcalc()
        
    elif cal== "3":
        weight, height, age, activity = _get_user_input(cal)
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
        againcalc()
        
    elif cal== "4":
        weight, height, age, activity = _get_user_input(cal)
        lose, gain, tdee = _calculate_calories(weight, height, age, activity)
        print("You need", lose, "calories to lose weight")
        againcalc()
        
    elif cal== "5":
        weight, height, age, activity = _get_user_input(cal)
        lose, gain, tdee = _calculate_calories(weight, height, age, activity)
        print("You need", gain, "calories to gain weight")
        againcalc()
        
    elif cal== "6":
        weight, height, age = _get_user_input(cal)
        tdee = _calculate_tdee(_calculate_bmr(weight, height, age), 1.55)
        print("You need", tdee, "calories to maintain weight")
        againcalc()
        
    elif cal== "7":
        weight, height, age = _get_user_input(cal)
        bmi = _calculate_bmi(weight, height)
        bmr = _calculate_bmr(weight, height, age)
        tdee = _calculate_tdee(bmr, 1.55)
        lose = tdee-500
        gain = tdee+500
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
