# Step 1: Load YAML Schema
import yaml
from pydantic import BaseModel, field_validator
import hashlib

# Load YAML schema file
with open('number_one/utils/schema.yaml', 'r') as file:
    schema = yaml.safe_load(file)

# Step 2: Identify Sensitive Fields
# Assuming the schema file has a specific way to mark fields as sensitive
sensitive_fields = [field for field, properties in schema['fields'].items() if properties.get('sensitive')]

# Step 3: Define Pydantic Model
class MyModel(BaseModel):
    # Define fields based on the YAML schema
    # Example:
    # name: str
    # email: str
    # password: str  # Assuming this is marked as sensitive in the YAML schema

    # Step 4: Apply Hashing to Sensitive Fields

    def hash_sensitive_fields(cls, v, field):
        if field.name in sensitive_fields:
            return hashlib.sha256(v.encode()).hexdigest()
        return v

# Example usage
model_instance = MyModel(name="John Doe", email="john@example.com", password="secret")
print(model_instance)

