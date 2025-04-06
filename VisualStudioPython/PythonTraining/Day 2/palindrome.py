s = input("Enter a string : ").lower()

l = len(s) - 1
i = 0
f = 0
while (i < l):
    if s[i] != s[l]:
        print("Not a palindrome.")
        break
    l -= 1
    i += 1
if i == l:
    print("Palindrome.")

#functions, modules, collections