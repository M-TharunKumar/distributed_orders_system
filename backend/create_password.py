#This code is used to generate hashed passwords for the application's users, such as ADMIN, OPERATOR, and VIEWER.
from auth.password import hash_password


print("ADMIN:")
print(hash_password("admin123"))

print("\nOPERATOR:")
print(hash_password("operator123"))

print("\nVIEWER:")
print(hash_password("viewer123"))