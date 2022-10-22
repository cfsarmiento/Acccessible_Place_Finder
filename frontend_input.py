# Libraries
from accessible_place_finder import place_finder

# User Input
cond = 'N'
while cond == 'N':
    user_address = input('Please Provide an Address (Address, City, State, Zip Code): ')
    radius = int(input('Enter a range for nearby establishments (meters): '))
    user_type = input('Please enter a type of establishment')
     # Function Call
    place_finder(user_address, radius, user_type)

    # Exit Condition
    cond = input('Would You Like to Continue? (Y/N): ').upper()
    if cond == 'Y':
        print('Thank You!')