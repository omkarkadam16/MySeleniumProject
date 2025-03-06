from faker import Faker

fake = Faker()

print(fake.vendorname())  # Generates a random name
print(
    fake.random_uppercase_letter()
    + fake.random_uppercase_letter()
    + fake.random_uppercase_letter()
    + fake.random_uppercase_letter()
    + fake.random_uppercase_letter()
    + str(fake.random_int(min=1000, max=9999))
    + "P"
)  # Generates a fake PAN No.
print(fake.address())  # Generates a random address
