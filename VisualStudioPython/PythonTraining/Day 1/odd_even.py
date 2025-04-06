def main():
    a = int(input("Enter a number : "))
    if is_even(a):
        print("Even")
    else:
        print("Odd")

def is_even(n):
    return n % 2 == 0

main()

# return True if n % 2 == 0 else False