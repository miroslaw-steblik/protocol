from pydantic import BaseModel, ValidationError, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
    is_active: bool = True  # Default value if not provided

# Example of creating a User instance with valid data
user_data = {
    "name": "Alice",
    "age": 30,
    "email": "alice@example.com"
}

user = User(**user_data)
print(user)
# Output: name='Alice' age=30 email='alice@example.com' is_active=True

# Example of trying to create a User instance with invalid data
invalid_user_data = {
    "name": "Bob",
    "age": "not a number",  # Invalid age
    "email": "not an email"
}

try:
    User(**invalid_user_data)
except ValidationError as e:
    print(e)
    # This will print validation errors indicating that 'age' 
    # must be an integer and 'email' must be a valid email address.