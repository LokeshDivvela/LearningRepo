a = int(input("Enter number 1 : "))
b = int(input("Enter number 2 : "))

# lcm = 0

for i in range(1, (a*b)+1):
    if (i%a == 0) & (i%b == 0):
        lcm = i
        break

print("LCM of the 2 numbers is : ", lcm)