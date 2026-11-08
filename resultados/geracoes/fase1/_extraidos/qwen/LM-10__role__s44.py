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
    return weight / height ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(bmr, activity, weight, height, age):
    tdee = calculate_tdee(bmr, activity)
    lose = tdee - 500
    gain = tdee + 500
    return tdee, lose, gain

def calculate_all(weight, height, age, activity):
    cmheight = height / 100
    bmi = calculate_bmi(weight, cmheight)
    bmr = calculate_bmr(weight, height, age)
    tdee, lose, gain = calculate_calories_needed(bmr, activity, weight, height, age)
    return bmi, bmr, tdee, lose, gain

def handle_choice(cal, weight, height, age, activity):
    if cal == "1":
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
    elif cal == "2":
        bmr = calculate_bmr(weight, height, age)
        print("Your BMR is", bmr)
    elif cal == "3":
        tdee, _, _ = calculate_calories_needed(calculate_bmr(weight, height, age), activity, weight, height, age)
        print("Your TDEE is", tdee)
    elif cal == "4":
        tdee, lose, _ = calculate_calories_needed(calculate_bmr(weight, height, age), activity, weight, height, age)
        print("You need", lose, "calories to lose weight")
    elif cal == "5":
        tdee, _, gain = calculate_calories_needed(calculate_bmr(weight, height, age), activity, weight, height, age)
        print("You need", gain, "calories to gain weight")
    elif cal == "6":
        tdee, _, _ = calculate_calories_needed(calculate_bmr(weight, height, age), activity, weight, height, age)
        print("You need", tdee, "calories to maintain weight")
    elif cal == "7":
        bmi, bmr, tdee, lose, gain = calculate_all(weight, height, age, activity)
        print("Your BMI is", bmi)
        print("Your BMR is", bmr)
        print("Your TDEE is", tdee)
        print("You need", lose, "calories to lose weight")
        print("You need", gain, "calories to gain weight")
        print("You need", tdee, "calories to maintain weight")

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal in ["1", "2", "3", "4", "5", "6", "7"]:
        weight = int(input("What is your weight in kg?"))
        height = int(input("What is your height in cm?"))
        age = int(input("What is your age in years?"))
        if cal == "2":
            height = height / 100
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        handle_choice(cal, weight, height, age, activity)
    else:
        print("Invalid number, choose a wise one next time")
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
