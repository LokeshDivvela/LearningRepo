# n = int(input("Enter a number : "))
# i = 1
# c = 0
# while (i<n):
#     if n%i == 0:
#         c += 1
#     i += 1

# if c > 2:
#     print("Not a prime number.")
# else:
#     print("It is a Prime Number.")

n = int(input("Enter a number : "))
i = 1
c = 0
for i in range(1, int(n/2 + 1)):
    if n%i == 0:
        c += 1

if c > 2:
    print("Not a prime number.")
else:
    print("Prime Number!!")
