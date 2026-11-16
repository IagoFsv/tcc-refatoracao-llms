def ask_choice():
    cal = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    return cal

def ask_weight():
    weight = int(input("What is your weight in kg?"))
    return weight

def ask_height():
    height = int(input("What is your height in meters?"))
    return height

def ask_age():
    age = int(input("What is your age in years?"))
    return age

def ask_activity():
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return activity

def calculate_bmi(weight, height):
    bmi = weight / height**2
    return bmi

def calculate_bmr(weight, height, age):
    bmr = 10 * weight + 6.25 * height - 5 * age
    return bmr

def calculate_tdee(bmr, activity):
    tdee = bmr * activity
    return tdee

def calculate_calories_to_lose(tdee):
    lose = tdee - 500
    return lose

def calculate_calories_to_gain(tdee):
    gain = tdee + 500
    return gain

def calculate_calories_to_maintain(tdee):
    return tdee

def print_results(bmi, bmr, tdee, lose, gain):
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
    choice = ask_choice()
    if choice == "1":
        weight = ask_weight()
        height = ask_height()
        bmi = calculate_bmi(weight, height)
        print("Your BMI is", bmi)
        againcalc()
    elif choice == "2":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        bmr = calculate_bmr(weight, height, age)
        print("Your bmr is", bmr)
        againcalc()
    elif choice == "3":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        activity = ask_activity()
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        print("Your tdee is", tdee)
        againcalc()
    elif choice == "4":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        activity = ask_activity()
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_to_lose(tdee)
        print("You need", lose, "calories to lose weight")
        againcalc()
    elif choice == "5":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        activity = ask_activity()
        bmr = calculate_bmr(weight, height, age)
        tdee = calculate_tdee(bmr, activity)
        gain = calculate_calories_to_gain(tdee)
        print("You need", gain, "calories to gain weight")
        againcalc()
    elif choice == "6":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        activity = ask_activity()
        tdee = calculate_tdee(calculate_bmr(weight, height, age), activity)
        print("You need", tdee, "calories to maintain weight")
        againcalc()
    elif choice == "7":
        weight = ask_weight()
        height = ask_height()
        age = ask_age()
        cmheight = height / 100
        bmi = calculate_bmi(weight, cmheight)
        bmr = calculate_bmr(weight, height, age)
        activity = ask_activity()
        tdee = calculate_tdee(bmr, activity)
        lose = calculate_calories_to_lose(tdee)
        gain = calculate_calories_to_gain(tdee)
        print_results(bmi, bmr, tdee, lose, gain)
        againcalc()
    else:
        print("Invalid number, choose a wise one next time")

def executar():
    return calc()

if __name__ == "__main__":
    executar()
