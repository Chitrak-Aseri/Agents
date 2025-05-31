def flatten(nested_list):
    """Recursively flatten a nested list structure into a single-level list.
    
    Args:
        nested_list: A list potentially containing other lists as elements.
        
    Returns:
        A new single-level list containing all elements from the nested structure.
    """
    flat_list = []
    for item in nested_list:
        if isinstance(item, list):
            # Recursively flatten nested lists
            flat_list.extend(flatten(item)) 
        else:
            flat_list.append(item)
    return flat_list