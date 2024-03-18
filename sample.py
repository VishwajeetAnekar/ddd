import re

def validate_datetime(value, dtype):
    if re.match(r'DATETIME\((\d+)\)', dtype):
        length = int(re.search(r'DATETIME\((\d+)\)', dtype).group(1))

        # Convert value to string, strip, and remove '.0'
        value_str = str(value).strip().replace('.0', '')

        if len(value_str) != length:
            error_message = f"Invalid datetime format: Length does not match"
            return False, value_str, error_message

        return True, value_str, "Valid datetime format"

# Test data
value = 20200000000000
dtype = 'DATETIME(14)'

# Perform validation
result, formatted_value, message = validate_datetime(value, dtype)

# Display results
print("Value:", value)
print("Data type:", dtype)
print("Formatted value:", formatted_value)
print("Validation result:", result)
print("Message:", message)
