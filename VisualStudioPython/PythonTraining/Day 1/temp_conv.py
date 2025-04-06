def convert(c):
    f = (c * 9/5) + 32
    return f

def main():
    c = int(input("Enter temperature in Celsius : "))
    print("Temperature in Farenhiet is : ", convert(c))

main()  