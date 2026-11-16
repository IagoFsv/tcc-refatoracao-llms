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

def calculate_bmi(weight, height):
    return weight / (height ** 2)

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_to_lose(tdee):
    return tdee - 500

def calculate_calories_to_gain(tdee):
    return tdee + 500

def calculate_calories_to_maintain(tdee):
    return tdee

def bmi(weight, height):
    bmi = calculate_bmi(weight, height)
    print("Your BMI is", bmi)
    againcalc()

def bmr(weight, height, age):
    bmr = calculate_bmr(weight, height, age)
    print("Your BMR is", bmr)
    againcalc()

def tdee(weight, height, age, activity):
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    print("Your TDEE is", tdee)
    againcalc()

def calories_to_lose(weight, height, age, activity):
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    lose = calculate_calories_to_lose(tdee)
    print("You need", lose, "calories to lose weight")
    againcalc()

def calories_to_gain(weight, height, age, activity):
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    gain = calculate_calories_to_gain(tdee)
    print("You need", gain, "calories to gain weight")
    againcalc()

def calories_to_maintain(weight, height, age, activity):
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    maintain = calculate_calories_to_maintain(tdee)
    print("You need", maintain, "calories to maintain weight")
    againcalc()

def calculate_all(weight, height, age, activity):
    bmi(weight, height)
    bmr(weight, height, age)
    tdee(weight, height, age, activity)
    calories_to_lose(weight, height, age, activity)
    calories_to_gain(weight, height, age, activity)
    calories_to_maintain(weight, height, age, activity)

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal == "1":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in meters?"))
        bmi(weight, height)
    elif cal == "2":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr(weight, height, age)
    elif cal == "3":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee(weight, height, age, activity)
    elif cal == "4":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calories_to_lose(weight, height, age, activity)
    elif cal == "5":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calories_to_gain(weight, height, age, activity)
    elif cal == "6":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calories_to_maintain(weight, height, age, activity)
    elif cal == "7":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        calculate_all(weight, height, age, activity)
    else:
        print("Invalid number, choose a wise one next time")

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
