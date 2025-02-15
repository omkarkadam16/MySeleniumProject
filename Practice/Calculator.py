a = int(input("Enter Value of A:"))
b = int(input("Enter Value of B:"))
operation = input("Choose Operation (+, -, *, /):")
if operation == "+":
    print(f"The sum of {a} and {b} is {a + b}")
elif operation == "-":
    print(f"The difference between {a} and {b} is {a - b}")
elif operation == "*":
    print(f"The product of {a} and {b} is {a * b}")
elif operation == "/":
    print(f"The quotient of {a} and {b} is {a / b}")
else:
    print("Invalid operation!")
