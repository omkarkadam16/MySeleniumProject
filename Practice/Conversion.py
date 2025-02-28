a = "Omkar"
Questions = input(
    "Ask Any one Question: (How are You,How's your Day?, Your favorite color?):"
)

if Questions.lower() == "how are you":
    print(f"Hello {a}, I'm doing well. How about you?")
    print("I'm doing well too. Thanks for asking!")
elif Questions.lower() == "how's your day":
    print(f"Hello {a}, I'm glad you're doing well. I'm also doing well. How about you?")
    print("I'm doing well too. Thanks for asking!")
elif Questions.lower() == "Your favorite color?":
    print(
        f"Hello {a}, I'm not a person. I don't have a favorite color. But I can tell you that I like red and blue. Which one do you like?"
    )
    print("I like red and blue. Thanks for asking!")
    color = input("Enter your favorite color: ")
    print(f"Hello {a}, I agree that {color} is a great color!")
    print("I'm glad to hear that!")
    print("Thanks for asking!")
    print("Goodbye!")
    exit()
