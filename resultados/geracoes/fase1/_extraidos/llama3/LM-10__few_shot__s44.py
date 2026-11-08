def ask_user_to_calculate_again():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calculate_bmi():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in meters?"))
    bmi = weight / height ** 2
    print("Your BMI is", bmi)
    ask_user_to_calculate_again()

def calculate_bmr():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    print("Your bmr is", bmr)
    ask_user_to_calculate_again()

def calculate_tdee():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    print("Your tdee is", tdee)
    ask_user_to_calculate_again()

def calculate_calories_needed_to_lose_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    lose = tdee - 500
    print("You need", lose, "calories to lose weight")
    ask_user_to_calculate_again()

def calculate_calories_needed_to_gain_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    tdee = bmr * activity
    gain = tdee + 500
    print("You need", gain, "calories to gain weight")
    ask_user_to_calculate_again()

def calculate_calories_needed_to_maintain_weight():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    print("You need", bmr, "calories to maintain weight")
    ask_user_to_calculate_again()

def calculate_everything_from_bmi_and_activity_level():
    weight = int(input("what is your weight in kg?"))
    height = int(input("what is your height in cm?"))
    age = int(input("what is your age in years?"))
    cmheight = height / 100
    bmi = weight / cmheight ** 2
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr * activity
    lose = tdee - 500
    gain = tdee + 500
    print("Your BMI is", bmi)
    print("Your bmr is", bmr)
    print("Your tdee is", tdee)
    print("You need", lose, "calories to lose weight")
    print("You need", gain, "calories to gain weight")
    print("You need", tdee, "calories to maintain weight")
    ask_user_to_calculate_again()

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calculate_bmi()

if __name__ == "__main__":
    executar()
