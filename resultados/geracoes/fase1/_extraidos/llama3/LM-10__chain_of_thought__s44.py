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
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal== "1":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
        bmi=weight/height**2
        print("Your BMI is", bmi)
        _againcalc()
        
    elif cal== "2":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        bmr=10*weight+6.25*height-5*age
        _againcalc()
        
    # ... (restante do código)

def _againcalc():
    againcalc()

def _calc_bmi(weight, height):
    return weight/height**2

def _calc_bmr(weight, height, age):
    return 10*weight+6.25*height-5*age

def _calc_tdee(weight, height, age, activity):
    return _calc_bmr(weight, height, age)*activity

# ... (restante do código)
