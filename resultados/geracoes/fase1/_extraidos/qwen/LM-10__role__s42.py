def calculate_bmi(weight, height):
    return weight / height ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories_needed(lose_or_gain, tdee):
    return tdee + lose_or_gain

def display_results(bmi, bmr, tdee, lose, gain):
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
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

def handle_choice(choice):
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    if choice == "1":
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
    elif choice in ["2", "3", "4", "5", "6"]:
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        if choice == "4":
            lose = calculate_calories_needed(-500, tdee)
            print("You need", lose, "calories to lose weight")
        elif choice == "5":
            gain = calculate_calories_needed(500, tdee)
            print("You need", gain, "calories to gain weight")
        elif choice == "6":
            print("You need", tdee, "calories to maintain weight")
    elif choice == "7":
        bmi = calculate_bmi(weight, height)
        bmr = calculate_bmr(weight, height, age)
        activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_needed(-500, tdee)
        gain = calculate_calories_needed(500, tdee)
        display_results(bmi, bmr, tdee, lose, gain)
    else:
        print("Invalid number, choose a wise one next time")

def calc():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    handle_choice(cal)
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
