def main():
    print("Welcome to the password generator!")
    print("")
    
    options = ask_user_for_options()
    passwords = generate_passwords(options)
    print_passwords(passwords)
    
    if options['store_in_file']:
        store_passwords_in_file(passwords, options['path'])
    
    while True:
        answer = input("Do you want to generate more passwords? (y/n): ")
        if answer == 'y':
            main()
        elif answer == 'n':
            print("Goodbye.")
            sys.exit()
        else:
            print("Please enter a valid answer.")
            print("")

def ask_user_for_options():
    options = {}
    options['special'] = input("Do you want to include special characters in the password? (y/n): ") == 'y'
    options['uppercase'] = input("Do you want to include uppercase letters in the password? (y/n): ") == 'y'
    options['lowercase'] = input("Do you want to include lowercase letters in the password? (y/n): ") == 'y'
    options['numbers'] = input("Do you want to include numbers in the password? (y/n): ") == 'y'
    options['symbols'] = input("Do you want to include symbols in the password? (y/n): ") == 'y'
    options['store_in_file'] = input("Do you want to store the list of passwords in a text file? (y/n): ") == 'y'
    options['path'] = input("Enter the path to the folder where you want to store the text file: ")
    return options

def generate_passwords(options):
    passwords = []
    if options['special']:
        for i in range(options['length']):
            password = ''
            for j in range(options['length']):
                password += random.choice(string.punctuation)
            passwords.append(password)
            
    if options['uppercase']:
        for i in range(options['length']):
            password = ''
            for j in range(options['length']):
                password += random.choice(string.ascii_uppercase)
            passwords.append(password)
    
    if options['lowercase']:
        for i in range(options['length']):
            password = '' 
            for j in range(options['length']): 
                password += random.choice(string.ascii_lowercase) 
            passwords.append(password) 
    
    if options['numbers']:
        for i in range(options['length']):
            password = '' 
            for j in range(options['length']): 
                password += random.choice(string.digits) 
            passwords.append(password) 
    
    if options['symbols']:
        for i in range(options['length']):
            password = '' 
            for j in range(options['length']): 
                password += random.choice(string.punctuation) 
            passwords.append(password) 
    
    return passwords

def print_passwords(passwords):
    print("")
    print("Here are the generated passwords:")
    for password in passwords:
        print(password)
    print("")
    
def store_passwords_in_file(passwords, path):
    with open(path + "/passwords.txt", "w") as file:
        for password in passwords:
            file.write(password + "\n")
    print("")
    print("The passwords have been stored in the text file.")
