a = int(input("Range starts from? "))
b = int(input("Range ends at? "))

print("Prime number in range are : ", end = "")
for i in range(a, b+1):
    c = 0
    for j in range(1, i+1):
        if (i%j == 0):
            # print(i, end = ', ')
            c += 1
    if c == 2:
        print(i, end = ", ")
