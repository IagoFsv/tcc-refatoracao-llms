"""Calculadora de condicionamento fisico  (IMC, TMB, gasto diario e calorias).

Ponto de entrada publico: executar(). Nao altere o nome nem a assinatura
dessa funcao; o restante do arquivo pode ser reorganizado livremente.
"""

def get_bmi(weight, height):
    return weight/height**2

def get_bmr(weight, height, age):
    return 10*weight+6.25*height-5*age

def get_tdee(bmr, activity):
    return bmr*activity

def get_calories(weight, height, age, activity, operation):
    bmr = get_bmr(weight, height, age)
    tdee = get_tdee(bmr, activity)
    if operation == "lose":
        return tdee - 500
    elif operation == "gain":
        return tdee + 500
    else:
        return tdee

def againcalc():
    againcalcu=input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu== "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif againcalcu== "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calc():
    cal=input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight  \n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal== "1":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in meters?"))
        print("Your BMI is", get_bmi(weight, height))
        againcalc()
        
    elif cal== "2":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        print("Your bmr is", get_bmr(weight, height, age))
        againcalc()
        
    elif cal== "3":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary 1.2, lightly active 1.375, moderately active 1.55, very active 1.725, extra active 1.9"))
        print("Your tdee is", get_tdee(get_bmr(weight, height, age), activity))
        againcalc()
        
    elif cal== "4":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary 1.2, lightly active 1.375, moderately active 1.55, very active 1.725, extra active 1.9"))
        print("You need", get_calories(weight, height, age, activity, "lose"), "calories to lose weight")
        againcalc()
        
    elif cal== "5":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary 1.2, lightly active 1.375, moderately active 1.55, very active 1.725, extra active 1.9"))
        print("You need", get_calories(weight, height, age, activity, "gain"), "calories to gain weight")
        againcalc()
        
    elif cal== "6":
        weight=int(input("What is your weight in kg?"))
        height=int(input("What is your height in cm?"))
        age=int(input("What is your age in years?"))
        activity=int(input("What is your activity level? Sedentary 1.2, lightly active 1.375, moderately active 1.55, very active 1.725, extra active 1.9"))
        print("You need", get_calories(weight, height, age, activity, "maintain"), "calories to maintain weight")
        againcalc()
        
    elif cal== "7":
        weight=int(input("what is your weight in kg?"))
        height=int(input("what is your height in cm?"))
        age=int(input("what is your age in years?"))
        cmheight=height/100
        print("Your BMI is", get_bmi(weight, cmheight))
        print("Your bmr is", get_bmr(weight, height, age))
        print("Your tdee is", get_tdee(get_bmr(weight, height, age), activity))
        print("You need", get_calories(weight, height, age, activity, "lose"), "calories to lose weight")
        print("You need", get_calories(weight, height, age, activity, "gain"), "calories to gain weight")
        print("You need", get_calories(weight, height, age, activity, "maintain"), "calories to maintain weight")
        againcalc()
        
    else:
        print("Invalid number, choose a wise one next time")


def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()


if __name__ == "__main__":
    executar()
