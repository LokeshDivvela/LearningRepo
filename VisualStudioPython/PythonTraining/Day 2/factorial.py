a = int(input("Enter a number : "))
f = 1
for i in range(2, a+1):
    f *= i

print("Factorial : ", f)