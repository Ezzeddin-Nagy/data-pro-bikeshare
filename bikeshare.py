import sys
import time
import pandas as pd
import numpy as np


class NotValidInput(Exception):
    pass


# Get user input using while loop to handle errors
def input_handler(looking_for, input_message, dict_name):
    i = 1
    key_data = ""
    # Use a while loop to handle invalid inputs
    while True:
        try:
            user_input = input(input_message).lower()
            for key, value in dict_name.items():
                if user_input in value:
                    key_data = key
                    return key_data
                elif not key_data and i == len(dict_name.keys()):
                    i = 1
                    raise NotValidInput(
                        '{} is not a vaild {}'.format(user_input, looking_for))
                i += 1
        except NotValidInput:
            print('{} is not a vaild {}'.format(user_input, looking_for))
        except ValueError:
            print("That wasn't a right choice")
        except KeyboardInterrupt:
            print("User aborted operation, exiting...")
            sys.exit()


CITY_DATA = {'chicago': 'chicago.csv',
             'new_york_city': 'new_york_city.csv',
             'washington': 'washington.csv'}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """

    # Dictionaries to assign various possible input styles to available names
    cities = {"chicago": ["1", "chicago", "ch", "chi", "shicago"],
              "new_york_city": ["2", "new york city", "ny", "nyc",
                                "new york", "newyork", "newyorkcity"],
              "washington": ["3", "washington", "wa", "was", "washington dc", "dc"]}
    months = {'all': ['all', 'a'], 'january': ['january', 'jan', '1'], 'february': ['february', 'feb', '2'], 'march': [
        'march', 'mar', '3'], 'april': ['april', 'apr', '4'], 'may': ['may', '5'], 'june': ['june', 'jun', '6']}
    days = {'all': ['all', 'a'], 'saturday': ['saturday', 'sat'], 'sunday': ['sunday', 'sun'], 'monday': ['monday', 'mon'], 'tuesday': [
        'tuesday', 'tue'], 'wednesday': ['wednesday', 'wed'], 'thursday': ['thursday', 'thu'], 'friday': ['friday', 'fri']}

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT:
    city_input_message = "Which city would you like to explore?\nYou can type chicago, new york city, or washington:\n"
    city = input_handler("City", city_input_message, cities)
    print("Oh, {} Then!".format(city.replace("_", " ").title()))
    # get user input for month (all, january, february, ... , june)
    month_input_message = "Which month would you like to filter by?\nYou can type All for no filters\n"
    month = input_handler("Month", month_input_message, months)
    print("Allright then, let's do", month.title())
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day_input_message = "Would you like to filter by certain day?\nYou can type day full name or All for no filters\n"
    day = input_handler("Day", day_input_message, days)
    print("Let's check for", day.title())

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month_name()
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # filter by month to create the new dataframe
        df = df.loc[df['month'] == month.title()]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    popular_month = df['month'].mode()[0]
    print('The most common month:', popular_month)
    # display the most common day of week
    popular_day = df['day_of_week'].mode()[0]
    print('The most common day of week:', popular_day)
    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print('The most common hour:', popular_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    popular_start_station = df['Start Station'].mode()[0]
    print('The most common Start Station:', popular_start_station)
    # display most commonly used end station
    popular_end_station = df['End Station'].mode()[0]
    print('The most common End Station:', popular_end_station)
    # display most frequent combination of start station and end station trip
    popular_route = df.groupby(
        ['Start Station', 'End Station']).size().idxmax()
    print('the most popular route is:', popular_route)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel = df['Trip Duration'].sum()
    # display mean travel time
    mean_travel = total_travel / df['Trip Duration'].count()
    print('Total trips duration is: {}'.format(total_travel))
    print('The mean trip duration is: {}'.format(mean_travel))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The user types counts:\n {}\n'.format(user_types))
    # Display counts of gender
    if 'Gender' in df:
        gender_types = df['Gender'].value_counts()
        print('Users genders count is : \n {}\n'.format(gender_types))
    else:
        print('No gender data available for this dataset')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df:
        earliest_birth_year = int(df['Birth Year'].min())
        print('the earlist year of birth is :  {}'.format(earliest_birth_year))
        recent_birth_year = int(df['Birth Year'].max())
        print('the most recent year of birth is :  {}'.format(recent_birth_year))
        common_birth_year = int(df['Birth Year'].mode())
        print('the common year of birth is :  {}'.format(common_birth_year))
    else:
        print('No birth year data available for this dataset')
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        print("Number of data rows:", len(df.index))
        consent = ["yes", 'y', "yeah", "yea", "yah", "ya", "1"]
        while True:
            try:
                view_data = input(
                    "\nWould you like to view some individual trip data? Enter yes or no?\n")
                # Let user determine number of rows to show
                if view_data.lower() in consent:
                    view_display = 'yes'
                    rows_per_time = int(
                        input("\nHow many rows would you like to show per time?\n"))
                    start_loc = 0
                    # Get count of remaining rows in df

                    def remaining_rows(start_loc):
                        return len(df.iloc[start_loc:].index)

                    while (view_display in consent):
                        if remaining_rows(start_loc) == 0:
                            print("No more data to preview ...exiting")
                            break

                        print(df.iloc[start_loc:start_loc + rows_per_time])
                        start_loc += rows_per_time
                        print("Remaining rows count:",
                              remaining_rows(start_loc))
                        view_display = input(
                            "Do you wish to continue?: ").lower()
                    break
                else:
                    break
            except ValueError:
                print("wrong input, please make sure to enter a valid integer")
            except KeyboardInterrupt:
                print("No Input Recieved")
                break

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() not in consent:
            print("Thank you, Bye!")
            break


if __name__ == "__main__":
    main()
