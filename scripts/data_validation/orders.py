from pydantic import BaseModel, ValidationError, field_validator, EmailStr, conlist


class Address(BaseModel):
    street: str
    city: str
    zip_code: str

    # Custom field_validator for the zip_code field
    @field_validator('zip_code')
    def zip_code_must_be_five_digits(cls, v):
        if len(v) != 5 or not v.isdigit():
            raise ValueError('Zip code must be 5 digits')
        return v

class Item(BaseModel):
    name: str
    description: str = None  # Optional field
    price: float
    tax: float = None  # Optional field

    # Custom method to calculate total price including tax
    def total_price(self):
        return self.price + (self.tax if self.tax else 0)

class Order(BaseModel):
    user_email: EmailStr
    address: Address
    is_gift: bool = False

    def check_min_items(cls, v):
        if len(v) < 1:
            raise ValueError('Must contain at least one item')
        return v

    # Custom field_validator to ensure email is not from a specific domain
    @field_validator('user_email')
    def email_not_from_blocked_domain(cls, v):
        if v.endswith('@blockeddomain.com'):
            raise ValueError('Emails from @blockeddomain.com are not allowed')
        return v

# Example of creating an Order instance with valid data
order_data = {
    "user_email": "john.doe@example.com",
    "address": {
        "street": "123 Main St",
        "city": "Anytown",
        "zip_code": "12345"
    },
    "items": [
        {"name": "Widget", "description": "A useful widget", "price": 9.99, "tax": 0.8},
        {"name": "Gadget", "price": 12.99}
    ],
    "is_gift": False
}

try:
    order = Order(**order_data)
    print(order)
    # Output includes the order data with models validated and parsed
except ValidationError as e:
    print(e)