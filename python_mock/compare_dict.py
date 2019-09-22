from dictdiffer import diff


def is_same_dict(dict1, dict2):
    result = list(diff(dict1, dict2))
    return len(result) == 0, result


