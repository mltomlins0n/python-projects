import random
import string

print('Password Generator')
print('==================')

# Remove whitespace from printable ascii chars
chars = string.printable.strip()

num_of_passwords = input('Input amount of passwords to generate: ')
num_of_passwords = int(num_of_passwords)

length = input('Input the length of the password: ')
length = int(length)

print('Your passwords: ')

for pwd in range(num_of_passwords):
    passwords = ''
    for c in range(length):
        passwords += random.choice(chars)
    print(passwords)