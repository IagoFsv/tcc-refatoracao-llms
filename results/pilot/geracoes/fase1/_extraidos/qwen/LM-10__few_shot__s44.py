def _obter_dados_usuario():
    weight = int(input("What is your weight in kg?"))
    height = int(input("What is your height in cm?"))
    age = int(input("What is your age in years?"))
    activity = int(input("What is your activity level? Sedentary = 1.2, lightly active = 1.375, moderately active = 1.55, very active = 1.725, extra active = 1.9"))
    return weight, height, age, activity

def _calcular_bmi(weight, height):
    return weight / (height / 100) ** 2

def _calcular_bmr(weight, height, age):
    return 10 * weight + 6.25 * height - 5 * age

def _calcular_tdee(bmr, activity):
    return bmr * activity

def _calcular_calorias(lose_or_gain, tdee):
    return tdee + lose_or_gain

def _exibir_resultados(bmi, bmr, tdee, lose, gain):
    print(f"Your BMI is {bmi}")
    print(f"Your bmr is {bmr}")
    print(f"Your tdee is {tdee}")
    print(f"You need {lose} calories to lose weight")
    print(f"You need {gain} calories to gain weight")
    print(f"You need {tdee} calories to maintain weight")

def _executar_calculo(opcao):
    weight, height, age, activity = _obter_dados_usuario()
    if opcao == "1":
        bmi = _calcular_bmi(weight, height)
        print(f"Your BMI is {bmi}")
    elif opcao == "2":
        bmr = _calcular_bmr(weight, height, age)
        print(f"Your bmr is {bmr}")
    elif opcao == "3":
        bmr = _calcular_bmr(weight, height, age)
        tdee = _calcular_tdee(bmr, activity)
        print(f"Your tdee is {tdee}")
    elif opcao == "4":
        bmr = _calcular_bmr(weight, height, age)
        tdee = _calcular_tdee(bmr, activity)
        lose = _calcular_calorias(-500, tdee)
        print(f"You need {lose} calories to lose weight")
    elif opcao == "5":
        bmr = _calcular_bmr(weight, height, age)
        tdee = _calcular_tdee(bmr, activity)
        gain = _calcular_calorias(500, tdee)
        print(f"You need {gain} calories to gain weight")
    elif opcao == "6":
        bmr = _calcular_bmr(weight, height, age)
        tdee = _calcular_tdee(bmr, activity)
        print(f"You need {tdee} calories to maintain weight")
    elif opcao == "7":
        bmi = _calcular_bmi(weight, height)
        bmr = _calcular_bmr(weight, height, age)
        tdee = _calcular_tdee(bmr, activity)
        lose = _calcular_calorias(-500, tdee)
        gain = _calcular_calorias(500, tdee)
        _exibir_resultados(bmi, bmr, tdee, lose, gain)

def againcalc():
    againcalcu = input("Do you want to calculate again? y/n: ")
    print("----------------------------------------")
    if againcalcu == "y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        _executar_calculo(input("Enter your choice: "))
    elif againcalcu == "n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    _executar_calculo(input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight \n 7. for calculating everything from bmi and activity level\n Enter your choice: "))

if __name__ == "__main__":
    executar()
