import re


def increment_day(day_str):
    """
    Increment the day number in a string like 'Day 1' to 'Day 2'.

    :param day_str: The string with the day to increment.
    :type day_str: str
    :return: The incremented day string.
    :rtype: str
    """
    match = re.match(r'(Day )(\d+)', day_str, re.IGNORECASE)
    if match:
        day_word = match.group(1).capitalize()
        day_number = int(match.group(2)) + 1
        return f"{day_word}{day_number}"
    else:
        return day_str  # Return the original string if it doesn't match the pattern


def filename_to_day(filename):
    """
    Changes filename like 'day1.csv' to 'Day 1'.

    :param filename: The filename string to convert.
    :type filename: str
    :return: Capitalized filename with space between words and extention removed.
    :rtype: str
    """
    # Step 1: Remove the file extension
    name_without_extension = filename.split('.')[0]

    # Step 2: Extract the day part and convert it
    match = re.match(r'(day)(\d+)', name_without_extension, re.IGNORECASE)
    if match:
        day_word = match.group(1).capitalize()
        day_number = match.group(2)
        return f"{day_word} {day_number}"
    else:
        return filename  # Return the original filename if it doesn't match the pattern


def day_to_filename(day):
    """
    Converts string like 'Day 1' to 'day1.csv'.

    :param day: The string to convert.
    :type day: str
    :return: Lower the letters, remove spaces and add extension '.csv'.
    :rtype: str
    """
    filename = day.lower().replace(" ", "") + ".csv"
    return filename
