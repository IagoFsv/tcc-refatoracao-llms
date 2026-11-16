def calculate_bmi(weight, height):
    return weight / (height ** 2)

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(tdee, goal):
    if goal == "lose":
        return tdee - 500
    elif goal == "gain":
        return tdee + 500
    elif goal == "maintain":
        return tdee

def print_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your BMR is", bmr)
    print("Your TDEE is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

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
    cal = input("Choose a number:\n 1 for BMI,\n 2 for BMR,\n 3 for TDEE,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")

    if cal == "1":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in meters?"))
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
        againcalc()
        
    elif cal == "2":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        print("Your BMR is", bmr)
        againcalc()
        
    elif cal == "3":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        print("Your TDEE is", tdee)
        againcalc()
        
    elif cal == "4":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_needed(tdee, "lose")
        print("You need", lose, "calories to lose weight")
        againcalc()
        
    elif cal == "5":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        gain = calculate_calories_needed(tdee, "gain")
        print("You need", gain, "calories to gain weight")
        againcalc()
        
    elif cal == "6":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        print("You need", tdee, "calories to maintain weight")
        againcalc()
        
    elif cal == "7":
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_needed(tdee, "lose")
        gain = calculate_calories_needed(tdee, "gain")
        print_results(calculate_bmi(weight, height), bmr, tdee, lose, gain)
        againcalc()
        
    else:
        print("Invalid number, choose a wise one next time")

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
