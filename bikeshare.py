## Refactoring

import time
import pandas as pd
import numpy as np

CITY_KEY = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTH_KEY = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
DAY_KEY = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('\nWhich city would you like to explore?\n').lower()
        if city not in CITY_KEY:
            print('\nPlease enter either Chicago, New York City or Washington.\n')
            continue
        else:
            break

    # Get user input for month (all, january, february, ... , june)
    while True:
        month = input('\nPlease enter a month to filter by. Type "all" for no filter.\n').lower()
        if month not in MONTH_KEY:
            print('\nPlease enter either January, February, March, April, May, June or all for no filter\n')
            continue
        else:
            break

    # Get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('\nPlease enter a day of week to filter by. Type "all" for no filter.\n').lower()
        if day not in DAY_KEY:
            print('\nPlease enter either Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday or all for no filter\n')
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
    df = pd.read_csv(CITY_KEY[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    #add Start/End combo
    df['station_combo'] = df['Start Station'] + ' to ' + df['End Station']

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTH_KEY.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    print('The most common month of travel is: ',  df['month'].mode()[0])

    # Display the most common day of week
    print('The most common day of travel is: ', df['day_of_week'].mode()[0])

    # Display the most common start hour
    print('The most common hour of travel is: ', df['hour'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    print('The most commonly used start station is', df['Start Station'].mode()[0])

    # Display most commonly used end station
    print('The most commonly used end station is', df['End Station'].mode()[0])

    # Display most frequent combination of start station and end station trip
    print('The most commonly used route is to go from', df['station_combo'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    print('The total travel time is: ', df['Trip Duration'].sum(), ' seconds')

    # Display mean travel time
    print('The average travel time is: ', df['Trip Duration'].mean(), ' seconds')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('Count of user types:\n', df['User Type'].value_counts())

    # Check if chosen city is Washington
    if city == 'washington':
        print('\nWashington does not have statistics on gender')
    # Display counts of gender
    else:
        print('\nCount of gender:\n', df['Gender'].value_counts())

    # Check if chosen city is Washington
    if city == 'washington':
        print('\nWashington does not have statistics on year of birth')
    # Display earliest, most recent, and most common year of birth
    else:
        print('\nEarliest birth year: ', df['Birth Year'].min())
        print('Most recent birth year: ', df['Birth Year'].max())
        print('Most common birth yer: ', df['Birth Year'].mode()[0])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    rd_start = 0
    rd_end = 5
    rd_input = input('\nWould you like to view the first 5 rows of raw data? Enter yes or no. ').lower()
    while True:
        if rd_input == 'yes':
            print(df.iloc[rd_start:rd_end])
            nextrd_input = input('\nWould you like to view the next 5 rows of raw data? Enter yes or no. ').lower()
            if nextrd_input == 'yes':
                rd_start = rd_start + 5
                rd_end = rd_end + 5
                continue
            elif nextrd_input != 'no':
                print('Please enter yes or no.')
                continue
            else:
                break
        elif rd_input != 'no':
            print('Please enter yes or no.')
            rd_input = input('\nWould you like to view the first 5 rows of raw data? Enter yes or no. ').lower()
            continue
        else:
            break

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()
        if restart != 'yes':
            print('See you soon!')
            break

if __name__ == "__main__":
	main()
