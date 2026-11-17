def ask_for_choice():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def ask_for_weight():
    weight=int(input("What is your weight in kg?"))
    return weight

def ask_for_height():
    height=int(input("What is your height in cm?"))
    return height

def ask_for_age():
    age=int(input("What is your age in years?"))
    return age

def ask_for_activity_level():
    activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return activity

def calculate_bmi(weight, height):
    cmheight=height/100
    bmi=weight/cmheight**2
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

def calculate_everything_from_bmi_and_activity_level(weight, height, age):
    cmheight=height/100
    bmi=weight/cmheight**2
    bmr=10*weight+6.25*height-5*age
    activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee=bmr*activity
    lose=tdee-500
    gain=tdee+500
    return bmi, bmr, tdee, lose, gain

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

def calc():
    cal=ask_for_choice()
    if cal== "1":
        weight=ask_for_weight()
        height=ask_for_height()
        bmi=calculate_bmi(weight, height)
        print("Your BMI is", bmi)
        againcalc()
        
    elif cal== "2":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        bmr=calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
        againcalc()
        
    elif cal== "3":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        activity=ask_for_activity_level()
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
        againcalc()
        
    elif cal== "4":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        activity=ask_for_activity_level()
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        lose=calculate_calories_needed_to_lose_weight(tdee)
        print("You need", lose, "calories to lose weight")
        againcalc()
        
    elif cal== "5":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        activity=ask_for_activity_level()
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        gain=calculate_calories_needed_to_gain_weight(tdee)
        print("You need", gain, "calories to gain weight")
        againcalc()
        
    elif cal== "6":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        bmr=calculate_bmr(weight, height, age)
        tdee=calculate_tdee(bmr, activity)
        print("You need", tdee, "calories to maintain weight")
        againcalc()
        
    elif cal== "7":
        weight=ask_for_weight()
        height=ask_for_height()
        age=ask_for_age()
        bmi, bmr, tdee, lose, gain = calculate_everything_from_bmi_and_activity_level(weight, height, age)
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
