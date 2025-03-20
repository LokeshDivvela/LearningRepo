a = int(input("Enter number 1 : "))
b = int(input("Enter number 2 : "))

gcd = 1

for i in range(1, max(a, b)):
    if (a%i == 0) & (b%i == 0):
        gcd = i

print("GCD of the number is : ", gcd)