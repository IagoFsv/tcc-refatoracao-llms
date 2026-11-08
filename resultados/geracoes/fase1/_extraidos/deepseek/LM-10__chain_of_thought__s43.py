def get_user_input():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight  \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def perform_calculation(cal, weight, height, age, bmr, activity):
    if cal == "1":
        bmi = weight / height ** 2
        print("Your BMI is", bmi)
    elif cal == "2":
        bmr = 10 * weight + 6.25 * height - 5 * age
        print("Your bmr is", bmr)
    elif cal == "3":
        tdee = bmr * activity
        print("Your tdee is", tdee)
    elif cal == "4":
        lose = tdee - 500
        print("You need", lose, "calories to lose weight")
    elif cal == "5":
        gain = tdee + 500
        print("You need", gain, "calories to gain weight")
    elif cal == "6":
        print("You need", tdee, "calories to maintain weight")
    elif cal == "7":
        bmi = weight / (height / 100) ** 2
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

def calc():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    cal = get_user_input()
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    perform_calculation(cal, weight, height, age, bmr, activity)
    againcalc()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__ == "__main__":
    executar()
