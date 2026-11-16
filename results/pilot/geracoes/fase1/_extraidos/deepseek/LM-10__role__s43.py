def againcalc():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight\n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal == "1":
        calculate_bmi()
    elif cal == "2":
        calculate_bmr()
    elif cal == "3":
        calculate_tdee()
    elif cal == "4":
        calculate_calories_to_lose_weight()
    elif cal == "5":
        calculate_calories_to_gain_weight()
    elif cal == "6":
        calculate_calories_to_maintain_weight()
    elif cal == "7":
        calculate_all()
    else:
        print("Invalid number, choose a wise one next time")

def calculate_bmi():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in meters?"))
    bmi = weight/height**2
    print("Your BMI is", bmi)
    againcalc()

def calculate_bmr():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10*weight+6.25*height-5*age
    print("Your bmr is", bmr)
    againcalc()

def calculate_tdee():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10*weight+6.25*height-5*age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr*activity
    print("Your tdee is", tdee)
    againcalc()

def calculate_calories_to_lose_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10*weight+6.25*height-5*age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr*activity
    lose = tdee-500
    print("You need", lose, "calories to lose weight")
    againcalc()

def calculate_calories_to_gain_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10*weight+6.25*height-5*age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr*activity
    gain = tdee+500
    print("You need", gain, "calories to gain weight")
    againcalc()

def calculate_calories_to_maintain_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10*weight+6.25*height-5*age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr*activity
    print("You need", tdee, "calories to maintain weight")
    againcalc()

def calculate_all():
    weight = int(input("what is your weight in kg?"))
    height = int(input("what is your height in cm?"))
    age = int(input("what is your age in years?"))
    cmheight = height/100
    bmi = weight/cmheight**2
    bmr = 10*weight+6.25*height-5*age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr*activity
    lose = tdee-500
    gain = tdee+500
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
