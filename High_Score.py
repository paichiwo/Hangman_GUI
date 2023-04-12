# High Score for Hangman
import json
from collections import Counter

# Load and display high score
with open("High_Score.txt", "r") as hs:
    high_score = json.load(hs)
k = Counter(high_score)
top_three = k.most_common(3)
for i in top_three:
    print(i[0], ":", i[1])

# set variables for the game
points = 0
lives = 10

# game loop
while lives > 0:
    a_or_b = input("a=1 or b=2?: ")
    if a_or_b == "a":
        points += 1
        lives -= 1
    elif a_or_b == "b":
        points += 2
        lives -= 1

# lost lives
print("Game Over")

# if points > than any of top three scores = high score
# enter name and save entry to high score file
k = Counter(high_score)
top_three = k.most_common(3)
first_best = top_three[0][1]
second_best = top_three[1][1]
third_best = top_three[2][1]
if points > first_best or points > second_best or points > third_best:
    print("High score!")
    name = input("Enter your name: ")
    high_score[name] = points
    with open("High_Score.txt", "w") as hs:
        json.dump(high_score, hs)
