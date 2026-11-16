def read_input(prompt):
    return int(input(prompt))

def againcalc():
    againcalcu=input("Do you want to calculate again? y/n: ])
    print("----------------------------------------")
    if againcalcu=="y":
        print("Sure, let's do it again")
        print("----------------------------------------")
        calc()
    elif againcalcu=="n":
        print("Goodbye, See You on The Other Side!")
        print("----------------------------------------")
    else:
        print("Invalid input, choose a wise one next time")
        print("----------------------------------------")

def calc():
    cal=read_input("Choose a number:\n 1 for BMI,\n 2 for bmr,\n 3 for tdee,\n 4 for calories needed to lose weight,\n 5 for calories needed to gain weight,\n 6 for calories needed to maintain weight\n 7. for calculating everything from bmi and activity level\n Enter your choice: ")
    if cal==1:
        weight=read_input("What is your weight in kg?")
        height=read_input("What is your height in meters?")
        bmi=weight/height**2
        print("Your BMI is", bmi)
        againcalc()
    # restante do código omitido para brevidade

def executar():
    """Roda a calculadora interativa. Ponto de entrada publico desta unidade."""
    return calc()

if __name__=="__main__":
    executar()
