# Write your code here
import random

print("H A N G M A N")
# print("The game will be available soon.")

lista = ['python', 'java', 'kotlin', 'javascript']

while input('Type "play" to play the game, "exit" to quit: ') == "play":
    random.seed()
    haslo = random.choice(lista)
    litery = set()
    progres = list("-" * len(haslo))
    tries = 8
    while tries > 0:
        print()
        print(''.join(progres))
        if ''.join(progres) == haslo:
            print("""You guessed the word
You survived!""")
            break

        usrinpt = input("Input a letter: ")

        if usrinpt in litery:
            print("You already typed this letter")
            continue
        elif len(usrinpt) != 1:
            print("You should input a single letter")
            continue
        elif not usrinpt.isalpha() or usrinpt.isupper():
            print("It is not an ASCII lowercase letter")
            continue
        litery.add(usrinpt)
        if usrinpt not in haslo:
            print("No such letter in the word")
            tries -= 1
        else:
            for i in range(len(haslo)):
                if haslo[i] in litery:
                    progres[i] = haslo[i]
    else:
        print("You are hanged!")
