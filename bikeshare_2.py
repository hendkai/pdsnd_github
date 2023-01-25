import time
import pandas as pd
import numpy as np
import datetime as dt

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Would you like to see data for Chicago, New York City, or Washington? ").lower()
        if city not in ('chicago', 'new york city', 'washington'):
            print("Please enter a valid city name.")
            continue
        else:
            break

    # get user input for month (all, january, february, ... , june)
    while True:
        month = input("Which month? January, February, March, April, May, June? ").lower()
        if month not in ('january', 'february', 'march', 'april', 'may', 'june'):
            print("Please enter a valid month.")
            continue
        else:
            break

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input("Which day? Please type your response as an integer (e.g., 1=Sunday, 2=Monday). ").lower()
        if day not in ('1', '2', '3', '4', '5', '6', '7'):
            print("Please enter a valid day.")
            continue
        else:
            break

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek + 1

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == int(day)]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # skip evaluation steps if given column does not exist
    if 'Start Time' not in df.columns:
        print('No data available for this filter.')
        return
    
    # display the most common month
    df['month'] = df['Start Time'].dt.month
    popular_month = df['month'].mode()[0]

    # display the most common day of week according to variable day from load_data
    df['day_of_week'] = df['Start Time'].dt.dayofweek + 1
    popular_day = df['day_of_week'].mode()[0]

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]

    # change day integer to day name
    if popular_day == 1:
        popular_day_int = 'Sunday'
    elif popular_day == 2:
        popular_day_int = 'Monday'
    elif popular_day == 3:
        popular_day_int = 'Tuesday'
    elif popular_day == 4:
        popular_day_int = 'Wednesday'
    elif popular_day == 5:
        popular_day_int = 'Thursday'
    elif popular_day == 6:
        popular_day_int = 'Friday'
    elif popular_day == 7:
        popular_day_int = 'Saturday'

    # Print Most popular hour, Count:, Filter:
    print('Most popular hour:', popular_hour, 'Count:', df['hour'].value_counts()[popular_hour], 'Filter:', 'hour')
    print('Most popular day:', popular_day_int, 'Count:', df['day_of_week'].value_counts()[popular_day], 'Filter:', 'day_of_week')
    print('Most popular month:', popular_month, 'Count:', df['month'].value_counts()[popular_month], 'Filter:', 'month')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # skip evaluation steps if given column does not exist
    if 'Start Station' not in df.columns:
        print('No Start Station available for this filter.')
        return
    
    if 'End Station' not in df.columns:
        print('No End Station available for this filter.')
        return

    # count most commonly used start station
    startstation = df['Start Station'].mode()[0]

    # count most commonly used end station
    endstation = df['End Station'].mode()[0]

    # count most frequent combination of start station and end station trip
    df['Start and End Station'] = df['Start Station'] + ' and ' + df['End Station']
    startendstation = df['Start and End Station'].mode()[0]

    # Print Most popular start station, Count:, Filter:
    print('Most popular start station:', startstation, 'Count:', df['Start Station'].value_counts()[startstation], 'Filter:', 'Start Station')
    print('Most popular end station:', endstation, 'Count:', df['End Station'].value_counts()[endstation], 'Filter:', 'End Station')
    print('Most popular start and end station:', startendstation, 'Count:', df['Start and End Station'].value_counts()[startendstation], 'Filter:', 'Start and End Station')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # skip evaluation steps if given column does not exist
    if 'Trip Duration' not in df.columns:
        print('No Trip Duration available for this filter.')
        return

    # display total travel time in minutes
    traveltime_sum = df['Trip Duration'].sum()

    # display mean travel time in minutes
    traveltime_mean = df['Trip Duration'].mean()

    print('Total travel time:', traveltime_sum, 'Filter:', 'Trip Duration in Minutes')
    print('Mean travel time:', traveltime_mean, 'Filter:', 'Trip Duration in Minutes')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # skip evaluation steps if a column does not exist
    if 'User Type' in df.columns:
        # Display counts of user types
        user_types = df['User Type'].value_counts()
    else:
        user_types = 'No User Type available for this filter.'

    if 'Gender' in df.columns:
        # groupby Gender and count values
        df_gender = df.groupby(['Gender']).size()
    else:
        df_gender = 'No Gender available for this filter.'

    if 'Birth Year' in df.columns:
        # Display earliest, most recent, and most common year of birth
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
    else:
        earliest_year = 'No Birth Year available for this filter.'
        most_recent_year = 'No Birth Year available for this filter.'
        most_common_year = 'No Birth Year available for this filter.'


    print('User types:', user_types, 'Filter:', 'User Type')
    print('Count:', df_gender , 'Filter:', 'Gender Count')
    print('Earliest year:', earliest_year, 'Filter:', 'Birth Year')
    print('Most recent year:', most_recent_year, 'Filter:', 'Birth Year')
    print('Most common year:', most_common_year, 'Filter:', 'Birth Year')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def view_data(df):
    # ask user if he wants to view the first 5 lines of raw data
    # bases on the city and the filters he chose
    view_data = input('\nWould you like to view 5 lines of individual trip data? Enter yes or no\n')
    start_loc = 0
    while (view_data.lower() == 'yes'):
        print(df.iloc[start_loc:start_loc+5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        view_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
