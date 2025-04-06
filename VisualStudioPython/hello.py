name = input("What is your name? ").strip().title()
first, last = name.split(" ")
print ("Hello World!", first)

x = float(input("What's x? "))
y = float(input("What's y? "))
z = round(x + y)
print(f"{z:,}")