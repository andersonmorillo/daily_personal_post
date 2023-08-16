def transform_filter(input_string, replacement_char='_'):
    return replacement_char.join(
        char.lower() if char.isupper() else char for char in input_string
    )


