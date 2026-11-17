def get_user_input(prompt, type_cast=None):
    user_input = input(prompt)
    if type_cast:
        user_input = type_cast(user_input)
    return user_input

def calculate_bmi(weight, height):
    return weight / height ** 2

def calculate_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def calculate_tdee(bmr, activity):
    return bmr * activity

def calculate_calories(tdee, operation, amount=500):
    if operation == "lose":
        return tdee - amount
    elif operation == "gain":
        return tdee + amount
    else:
        return tdee

def calculate_and_print(cal, weight, height, age, activity):
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    if cal == "1":
        print("Your BMI is", calculate_bmi(weight, height))
    elif cal == "2":
        print("Your bmr is", bmr)
    elif cal == "3":
        print("Your tdee is", tdee)
    elif cal == "4":
        print("You need", calculate_calories(tdee, "lose"), "calories to lose weight")
    elif cal == "5":
        print("You need", calculate_calories(tdee, "gain"), "calories to gain weight")
    elif cal == "6":
        print("You need", tdee, "calories to maintain weight")
    elif cal == "7":
        print("Your BMI is", calculate_bmi(weight, height))
        print("Your bmr is", bmr)
        print("Your tdee is", tdee)
        print("You need", calculate_calories(tdee, "lose"), "calories to lose weight")
        print("You need", calculate_calories(tdee, "gain"), "calories to gain weight")
        print("You need", tdee, "calories to maintain weight")

def againcalc():
    againcalcu = get_user_input("Do you want to calculate again? y/n: ")
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
    cal = get_user_input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    weight = get_user_input("What is your weight in kg?", int)
    height = get_user_input("What is your height in cm?", int)
    age = get_user_input("What is your age in years?", int)
    activity = get_user_input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9", float)
    calculate_and_print(cal, weight, height, age, activity)
    againcalc()

def run():
    """Runs the interactive calculator. Public entry point of this unit."""
    return calc()

if __name__ == "__main__":
    run()
