def againcalc():
    # código original...

def calc():
    # código original...

def calculate_bmi(weight, height):
    return weight/height**2

def calculate_bmr(weight, height, age):
    return 10*weight+6.25*height-5*age

def calculate_tdee(bmr, activity):
    return bmr*activity

def calculate_calories_to_lose_weight(tdee):
    return tdee-500

def calculate_calories_to_gain_weight(tdee):
    return tdee+500

def calculate_calories_to_maintain_weight(tdee):
    return tdee

def calculate_all(weight, height, age, activity):
    bmi = calculate_bmi(weight, height)
    bmr = calculate_bmr(weight, height, age)
    tdee = calculate_tdee(bmr, activity)
    lose = calculate_calories_to_lose_weight(tdee)
    gain = calculate_calories_to_gain_weight(tdee)
    maintain = calculate_calories_to_maintain_weight(tdee)
    return bmi, bmr, tdee, lose, gain, maintain

def executar():
    # código original...
