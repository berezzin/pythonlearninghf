def search4letters(request: str, search_in: str = 'aeiou') -> set:
    return set(request).intersection(search_in)
