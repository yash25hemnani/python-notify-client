def to_camel_case(snake_str):
    """
        Convert snake_case string to camelCase
    """
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def generate_payload(**kwargs) -> dict:
    """Generate camelCase payload for nodejs notification engine, stripping None values."""
    payload = {}

    for key, value in kwargs.items():
        if value is None:
            continue

        camel_key = to_camel_case(key)
        payload[camel_key] = value

    return payload
    
def generate_params(**kwargs):
    """
        Generate camelCase params for nodejs notification engine
    """
    
    params = {}
    
    for key, value in kwargs.items():
        camel_key = to_camel_case(key)
        params[camel_key] = value
        
    return params
    
    