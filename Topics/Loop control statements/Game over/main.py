scores = input().split()

correct = 0
wrong = 0
for i in scores:
    if i == 'C':
        correct += 1
    elif i == 'I':
        wrong += 1
        if wrong >= 3:
            print(f"Game over")
            print(correct)
            break
else:
    print(f"You won")
    print(correct)
