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
    return weight / height**2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(bmr, activity, lose_or_gain):
    tdee = calculate_tdee(bmr, activity)
    return tdee + lose_or_gain if lose_or_gain == "gain" else tdee - lose_or_gain

def display_results(bmi, bmr, tdee, lose_calories, gain_calories):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose_calories, "calories to lose weight")
    print("You need", gain_calories, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")

def calculate_and_display_choice(cal):
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))

    if cal == "1":
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
    elif cal == "2":
        bmr = calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
    elif cal == "3":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
    elif cal == "4":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose_calories = calculate_calories_needed(bmr, activity, "lose")
        print("You need", lose_calories, "calories to lose weight")
    elif cal == "5":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        gain_calories = calculate_calories_needed(bmr, activity, "gain")
        print("You need", gain_calories, "calories to gain weight")
    elif cal == "6":
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        print("You need", tdee, "calories to maintain weight")
    elif cal == "7":
        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose_calories = calculate_calories_needed(bmr, activity, "lose")
        gain_calories = calculate_calories_needed(bmr, activity, "gain")
        display_results(bmi, bmr, tdee, lose_calories, gain_calories)
    else:
        print("Invalid number, choose a wise one next time")

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    calculate_and_display_choice(cal)
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
