def validate_wine_entry(entry):
    required_fields = ["wine_id", "name", "vintage", "region", "grapes", "producer"]
    for field in required_fields:
        if field not in entry:
            raise ValueError(f"Missing required field: {field}")
    return True
