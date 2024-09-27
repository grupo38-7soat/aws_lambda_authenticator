def validate_document(document: str) -> bool:
    document = ''.join(filter(str.isdigit, document))

    if len(document) != 11:
        return False

    if document == document[0] * 11:
        return False

    sum1 = sum(int(document[i]) * (10 - i) for i in range(9))
    digit1 = (sum1 * 10 % 11) % 10

    sum2 = sum(int(document[i]) * (11 - i) for i in range(10))
    digit2 = (sum2 * 10 % 11) % 10

    return document[-2:] == f'{digit1}{digit2}'
