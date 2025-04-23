# init 2d list
c = [[(i+1)*(j+1) for i in range(9) if i % 2 == 0] for j in range(9) if j % 2 == 0]
for a in c:
    print(a)

# print as a matrix with 2 spaces between each number
for a in c:
    for b in a:
        print(b if b>9 else ' ' + str(b), end=' ')
    print()
