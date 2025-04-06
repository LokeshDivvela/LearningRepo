n = int(input("Enter a number : "))
i = 1
sum = 0

while(n != 0):
    sum = int(sum + n%10)
    n /= 10

print("Sum of digits : ", sum)