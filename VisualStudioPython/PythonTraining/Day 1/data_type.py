i = input("Enter an input : ")
if i.isdigit():
    print("Int")

# Float doesn't work.
elif i.replace(".", " ", 1).isdigit() and i.count('.') < 2:
    print("Float")

# elif float(i)%1 > 0:
#     print("Float")
else:
    print("String")