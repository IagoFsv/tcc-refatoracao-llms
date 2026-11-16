def calc():
    choice = input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if choice == "1":
        return calc_bmi()
    elif choice == "2":
        return calc_bmr()
    elif choice == "3":
        return calc_tdee()
    elif choice == "4":
        return calc_calories_to_lose()
    elif choice == "5":
        return calc_calories_to_gain()
    elif choice == "6":
        return calc_calories_to_maintain()
    elif choice == "7":
        return calc_everything()
    else:
        print("Invalid number, choose a wise one next time")

def calc_bmi():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in meters?"))
    bmi = weight / height ** 2
    print("Your BMI is", bmi)
    againcalc()

def calc_bmr():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    print("Your bmr is", bmr)
    againcalc()

def calc_tdee():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr * activity
    print("Your tdee is", tdee)
    againcalc()

def calc_calories_to_lose():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr * activity
    lose = tdee - 500
    print("You need", lose, "calories to lose weight")
    againcalc()

def calc_calories_to_gain():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr * activity
    gain = tdee + 500
    print("You need", gain, "calories to gain weight")
    againcalc()

def calc_calories_to_maintain():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    bmr = 10 * weight + 6.25 * height - 5 * age
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    tdee = bmr * activity
    print("You need", tdee, "calories to maintain weight")
    againcalc()

def calc_everything():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
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
    againcalc()

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

def executar():
    return calc()

if __name__ == "__main__":
    executar()
