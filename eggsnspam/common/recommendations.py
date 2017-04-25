def dot_product(d1, d2, default_value=0):
    """Calcualte the dot product for the intersection of two dictionary objects.

    If the key does not exist in d2, default_value is used instead.
    """
    return sum([float(d1[x]) * float(d2.get(x, default_value)) for x in list(d1.keys())])
