import csv
from datetime import datetime

DEGREE_SYMBOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees
        and Celcius symbols.

    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and "degrees Celcius."
    """
    return f"{temp}{DEGREE_SYMBOL}"

def convert_date(iso_string):
    """Converts and ISO formatted date into a human-readable format.

    Args:
        iso_string: An ISO date string.
    Returns:
        A date formatted like: Weekday Date Month Year e.g. Tuesday 06 July 2021
    """
    # parse the iso string into datetime object
    iso_datetime = datetime.fromisoformat(iso_string)

    # format date string
    new_format = iso_datetime.strftime("%A %d %B %Y")

    # return formatted date string
    return new_format

def convert_f_to_c(temp_in_fahrenheit):
    """Converts a temperature from Fahrenheit to Celcius.

    Args:
        temp_in_fahrenheit: float representing a temperature.
    Returns:
        A float representing a temperature in degrees Celcius, rounded to 1 decimal place.
    """
    # convert temp using formula 
    temp_in_celcius = (float(temp_in_fahrenheit) - 32) * (5 / 9)

    # round answer to 1 decimal place
    rounded_temp_celcius = round(temp_in_celcius, 1)

    # return rounded celcius temp
    return rounded_temp_celcius

def calculate_mean(weather_data):
    """Calculates the mean value from a list of numbers.

    Args:
        weather_data: a list of numbers.
    Returns:
        A float representing the mean value.
    """
    # variable to hold sum of temps
    temp_total = 0

    # iterate through each temp in list and add to total sum
    for temp in weather_data:
        temp_total += float(temp)

    # calculate mean by dividing sum from total length of list
    mean = temp_total/len(weather_data)

    # return calculated mean value
    return mean

def load_data_from_csv(csv_file):
    """Reads a csv file and stores the data in a list.

    Args:
        csv_file: a string representing the file path to a csv file.
    Returns:
        A list of lists, where each sublist is a (non-empty) line in the csv file.
    """
    # create empty list to store data
    data = []

    # open and read csv file
    with open(csv_file, mode = "r") as file:
        reader = csv.reader(file)
        # skip the header row
        next(reader)
        
        for row in reader:
            # skip empty rows
            if not (row):
                continue
            # extract dates, mins and max from row
            date = str(row[0])
            minimum = int(row[1])
            maximum = int(row[2])
            # append data to list
            data.append([date, minimum, maximum])
    # return list of lists
    return data

def find_min(weather_data):
    """Calculates the minimum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The minimum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    # if list is empty, return empty tuple ()
    if not weather_data:
        return ()

    # reverse list to find last occurence of min value
    reverse_weather = weather_data[::-1]
    # find min value in reversed list
    min_temp = min(reverse_weather)
    # find index of min value in reversed list
    reverse_min_index = reverse_weather.index(min_temp)
    # calculate original index 
    min_index = len(reverse_weather)-reverse_min_index-1
    # create tuple with min value and the index
    answer = (float(min_temp), min_index)
    # return tuple
    return answer

def find_max(weather_data):
    """Calculates the maximum value in a list of numbers.

    Args:
        weather_data: A list of numbers.
    Returns:
        The maximum value and it's position in the list. (In case of multiple matches, return the index of the *last* example in the list.)
    """
    # if list is empty, return empty tuple ()
    if not weather_data:
        return ()

    # reverse list to find last occurence of max value
    reverse_weather = weather_data[::-1]
    # find max value in reversed list
    max_temp = max(reverse_weather)
    # find index of max value in reversed list
    reverse_max_index = reverse_weather.index(max_temp)
    # calculate original index 
    max_index = len(reverse_weather)-reverse_max_index-1
    # create tuple with max value and the index
    answer = (float(max_temp), max_index)
    # return tuple
    return answer

def generate_summary(weather_data):
    """Outputs a summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    # create list to store min and max values for each day
    min_list = []
    max_list = []

    # populate min_list and max_list with daily temps
    for row in weather_data:
        min_list.append(row[1])
        max_list.append(row[2])
    
    # find absolute min and max temp and the index
    min_data = find_min(min_list)
    max_data = find_max(max_list)

    # extract temps in farenheit
    min_temp_farenheit = min_data[0]
    max_temp_farenheit = max_data[0]

    # convert temps from farenheit to celcius and format
    min_temp_celcius = format_temperature(convert_f_to_c(min_temp_farenheit))
    max_temp_celcius = format_temperature(convert_f_to_c(max_temp_farenheit))

    # get the date the min and max temp will occur on
    min_date_index = min_data[1]
    max_date_index = max_data[1]

    min_row = weather_data[min_date_index]
    max_row = weather_data[max_date_index]

    min_date_iso = min_row[0]
    max_date_iso = max_row[0]

    # convert the iso date
    min_date_converted = convert_date(min_date_iso)
    max_date_converted = convert_date(max_date_iso)

    # get the mean min and max values for the week
    avg_min_farenheit = calculate_mean(min_list)
    avg_max_farenheit = calculate_mean(max_list)

    # convert mean from farenheit to celcius and format
    avg_min_celcius = format_temperature(convert_f_to_c(avg_min_farenheit))
    avg_max_celcius = format_temperature(convert_f_to_c(avg_max_farenheit))
    
    # format and return the output summary as string
    return (
        f"{len(weather_data)} Day Overview\n"
        f"  The lowest temperature will be {min_temp_celcius}, and will occur on {min_date_converted}.\n"
        f"  The highest temperature will be {max_temp_celcius}, and will occur on {max_date_converted}.\n"
        f"  The average low this week is {avg_min_celcius}.\n"
        f"  The average high this week is {avg_max_celcius}.\n"
    )


def generate_daily_summary(weather_data):
    """Outputs a daily summary for the given weather data.

    Args:
        weather_data: A list of lists, where each sublist represents a day of weather data.
    Returns:
        A string containing the summary information.
    """
    # create list to hold formatted dates and converted temps
    weather_data_converted = []

    # format iso dates and convert temps to celcius
    for row in weather_data:
        converted_row = [
            convert_date(row[0]),
            format_temperature(convert_f_to_c(row[1])),
            format_temperature(convert_f_to_c(row[2]))
        ]
        # add converted data to new list
        weather_data_converted.append(converted_row)

    # create list to hold formatted daily summaries
    output = []
    # loop through converted weather data to create daily summary strings
    for row in weather_data_converted:
        output.append(f"---- {row[0]} ----\n  Minimum Temperature: {row[1]}\n  Maximum Temperature: {row[2]}\n\n")
    # combine daily summaries into one string
    result = ("".join(output))

    # return formatted string
    return result

