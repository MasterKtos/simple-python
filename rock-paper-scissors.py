import random

# Write your code here

# option: what it defeats
warrior = {"paper": "rock", "rock": "scissors", "scissors": "paper"}

name = input("Enter your name: ")
print(f"Hello, {name}")

file_highscore = open('rating.txt', 'r+')
score = 0
for line in file_highscore:
    if line.split()[0] == name:
        score = int(line.split()[1])
        break


def computer_win(chosen_option):
    computer_choice = ""
    for key, value in warrior.items():
        if value == chosen_option:
            computer_choice = key
            break
    print(f"Sorry, but computer chose {computer_choice}")


def play_rps(chosen_option):
    global score
    random.seed()
    computer_choice = random.choice(list(warrior))
    if chosen_option == computer_choice:
        print(f"There is a draw ({chosen_option})")
        score += 50
    elif computer_choice in warrior[chosen_option]:
        print(f"Well done. Computer chose {computer_choice} and failed")
        score += 100
    else:
        print(f"Sorry, but computer chose {computer_choice}")


def generate_warriors(*player_options):
    if len(player_options) == 1:
        return
    global warrior
    options = list(player_options)
    foe_quantity = int((len(options)-1)/2)
    # print(foe_quantity)
    warrior = dict()
    for i in range(len(options)):
        actual_option = options[0]
        warrior[actual_option] = options[-foe_quantity:]
        options = options[1:]
        options.append(actual_option)
        # print(actual_option, ":", warrior[actual_option])


generate_warriors(*input().split(","))
user_input = input()
print("Okay, let's start")

while user_input != "!exit":
    if user_input == "!rating":
        print("Your rating:", score)
    elif user_input in warrior:
        play_rps(user_input)
    else:
        print("Invalid input!")
    user_input = input()

file_highscore.close()
print("Bye!")
