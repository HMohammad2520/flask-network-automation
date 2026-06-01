def bool_normalizer(input: str) -> bool|None:
    if input.lower() in ['true', 'yes', '1']:
        return True

    elif input.lower() in ['false', 'no', '0']:
        return False

    elif input.lower() in ['none', 'null']:
        return None
    
    else:
        raise ValueError(f'Invalid bool value as string: `{input}`')