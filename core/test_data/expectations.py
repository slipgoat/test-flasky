import string

invalid_alphanumeric_field_values = [
    None,
    " ",
    string.punctuation[:5]
]


invalid_numeric_field_values = [
    *invalid_alphanumeric_field_values,
    string.ascii_lowercase[:5]
]

invalid_token_values = [
    (None, "Token authentication required"),
    ("invalidtoken", "Invalid Token")
]
