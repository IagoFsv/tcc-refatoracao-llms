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

def get_choice():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def get_user_input(cal):
    if cal== "1":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
        return weight, height
    elif cal== "2":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal== "3":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal== "4":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal== "5":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal== "6":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        return weight, height, age
    elif cal== "7":
        weight=int(input("what is your weight in kg?"))
        height=int(input("what is your height in cm?"))
        age=int(input("what is your age in years?"))
        cmheight=height/100
        return weight, height, age
    else:
        print("Invalid number, choose a wise one next time")

def calc():
    cal=get_choice()
    if cal== "1":
        weight, height = get_user_input(cal)
        bmi=weight/height**2
        print("Your BMI is", bmi)
        againcalc()
        
    elif cal== "2":
        weight, height, age = get_user_input(cal)
        bmr=10*weight+6.25*height-5*age
        print("Your bmr is", bmr)
        againcalc()
        
    elif cal== "3":
        weight, height, age = get_user_input(cal)
        bmr=10*weight+6.25*height-5*age
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee=bmr*activity
        print("Your tdee is", tdee)
        againcalc()
        
    elif cal== "4":
        weight, height, age = get_user_input(cal)
        bmr=10*weight+6.25*height-5*age
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee=bmr*activity
        lose=tdee-500
        print("You need", lose, "calories to lose weight")
        againcalc()
        
    elif cal== "5":
        weight, height, age = get_user_input(cal)
        bmr=10*weight+6.25*height-5*age
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee=bmr*activity
        gain=tdee+500
        print("You need", gain, "calories to gain weight")
        againcalc()
        
    elif cal== "6":
        weight, height, age = get_user_input(cal)
        bmr=10*weight+6.25*height-5*age
        tdee=bmr
        print("You need", tdee, "calories to maintain weight")
        againcalc()
        
    elif cal== "7":
        weight, height, age = get_user_input(cal)
        cmheight=height/100
        bmi=weight/cmheight**2
        bmr=10*weight+6.25*height-5*age
        activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee=bmr*activity
        lose=tdee-500
        gain=tdee+500
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
