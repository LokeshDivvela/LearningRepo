n = int(input("Enter the upper limit : "))
a = 0
b = 1
i = 2
print("0, 1", end = '')
while(i<n):
    c = a + b
    a = b
    b = c
    i += 1
    print(c, end=', ')