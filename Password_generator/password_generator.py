import random
import string

def generate_password(length = 12, use_upper=True, use_digits = True, use_symbols = True):
    chara = string.ascii_lowercase
    30
    if use_upper:
        chara += string.ascii_uppercase
    if use_digits:
        chara += string.digits 
    if use_symbols:
        chara += string.punctuation 
    password = ''.join(random.choices(chara, k=length))
    return password

length = int(input("Enter the Password length: "))
password = generate_password(length)
print("password: ", password)

# print(generate_password())
# print(generate_password(16))
# print(generate_password(10, use_symbols=False))