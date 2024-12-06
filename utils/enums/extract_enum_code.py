def extract_enum_code(enum_value):
    if hasattr(enum_value, 'code'):
        return enum_value.code
    raise AttributeError(f"У данного Enum нет атрибута code")