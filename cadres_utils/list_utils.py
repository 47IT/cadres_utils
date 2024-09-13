def chunk_list(lst, chunk_size):
    """Split a list into chunks of the specified size."""
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]

