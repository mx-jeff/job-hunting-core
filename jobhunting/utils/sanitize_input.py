import string


def sanitize_input(input_string):
    """
    Sanitize input string.
    :param input_string: input string
    :return: sanitized input string
    """
    input_string = input_string.strip()
    input_string = input_string.lower()
    input_string = input_string.replace(" ", "-")

    table = str.maketrans(dict.fromkeys(string.punctuation))
    input_string = input_string.translate(table)

    return input_string
