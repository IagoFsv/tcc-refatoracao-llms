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

def _ask_for_choice():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def _ask_for_weight():
    weight=int(input("What is your weight in kg?"))
    return weight

def _ask_for_height():
    height=int(input("What is your height in meters?"))
    return height

def _ask_for_age():
    age=int(input("What is your age in years?"))
    return age

def _ask_for_height_cm():
    height=int(input("What is your height in cm?"))
    return height

def _ask_for_activity_level():
    activity=int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return activity

def _compute_bmi(weight, height):
    return weight/height**2

def _compute_bmr(weight, height, age):
    return 10*weight+6.25*height-5*age

def _compute_tdee(bmr, activity):
    return bmr*activity

def _compute_calories_to_lose(tdee):
    return tdee-500

def _compute_calories_to_gain(tdee):
    return tdee+500

def _compute_calories_to_maintain(tdee):
    return tdee

def _print_bmi(bmi):
    print("Your BMI is", bmi)

def _print_bmr(bmr):
    print("Your bmr is", bmr)

def _print_tdee(tdee):
    print("Your tdee is", tdee)

def _print_calories_to_lose(calories):
    print("You need", calories, "calories to lose weight")

def _print_calories_to_gain(calories):
    print("You need", calories, "calories to gain weight")

def _print_calories_to_maintain(calories):
    print("You need", calories, "calories to maintain weight")

def _print_all_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def calc():
    cal=_ask_for_choice()
    if cal== "1":
        weight=_ask_for_weight()
        height=_ask_for_height()
        bmi=_compute_bmi(weight, height)
        _print_bmi(bmi)
        againcalc()
        
    elif cal== "2":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        bmr=_compute_bmr(weight, height, age)
        _print_bmr(bmr)
        againcalc()
        
    elif cal== "3":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        activity=_ask_for_activity_level()
        bmr=_compute_bmr(weight, height, age)
        tdee=_compute_tdee(bmr, activity)
        _print_tdee(tdee)
        againcalc()
        
    elif cal== "4":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        activity=_ask_for_activity_level()
        bmr=_compute_bmr(weight, height, age)
        tdee=_compute_tdee(bmr, activity)
        lose=_compute_calories_to_lose(tdee)
        _print_calories_to_lose(lose)
        againcalc()
        
    elif cal== "5":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        activity=_ask_for_activity_level()
        bmr=_compute_bmr(weight, height, age)
        tdee=_compute_tdee(bmr, activity)
        gain=_compute_calories_to_gain(tdee)
        _print_calories_to_gain(gain)
        againcalc()
        
    elif cal== "6":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        activity=_ask_for_activity_level()
        tdee=_compute_tdee(_compute_bmr(weight, height, age), activity)
        _print_calories_to_maintain(tdee)
        againcalc()
        
    elif cal== "7":
        weight=_ask_for_weight()
        height=_ask_for_height_cm()
        age=_ask_for_age()
        cmheight=height/100
        bmi=_compute_bmi(weight, cmheight)
        bmr=_compute_bmr(weight, height, age)
        activity=_ask_for_activity_level()
        tdee=_compute_tdee(bmr, activity)
        lose=_compute_calories_to_lose(tdee)
        gain=_compute_calories_to_gain(tdee)
        _print_all_results(bmi, bmr, tdee, lose, gain)
        againcalc()
        
    else:
        print("Invalid number, choose a wise one next time")


def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()


if __name__ == "__main__":
    run()
