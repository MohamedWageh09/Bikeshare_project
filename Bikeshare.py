import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'cleaned_chicago.csv',
              'nyc': 'cleaned_nyc.csv',
              'washington': 'washington.csv' }
DAYS = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All' ]
def get_filters():
    CITIES = CITY_DATA.keys()
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        city= input("\n Which city would you like to analyse? (chicago, nyc or washington): ").lower()
        if city in CITIES:
            break
        else:
            print("\n Please enter a valid city name")

    '''
    get user input for month (all, january, february, ... , june)
    '''
    MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
    month = str(input("Which month would you like to analyse? (full month name or 'all'): ")).lower()
    while month not in MONTHS:
        print("Please enter a valid month")
        month = str(input("Which month would you like to analyse? (full month name or 'all'): ")).lower()
    '''
    get user input for day of week (all, monday, tuesday, ... sunday)
    '''
    day = str(input("Enter the day name or use 'all' for all days: ")).title()
    while day not in DAYS:
        print("Please enter a valid day")
        day = str(input("Enter the day name or use 'all' for all days: ")).title()


    return city, month, day


def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['month'] = df['Start Time'].dt.month
    df['hour'] = df['Start Time'].dt.hour

    if month != 'all':
        MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
        month = MONTHS.index(month)+1
        df = df[df['month']== month]

    if day != 'All':
        df = df[df['day_of_week']== day.title()]

    return df

'''
ask user is he would like to view raw data
'''
def raw_data_selection(df):

    df= df.sort_values(by= ['Start Time'])
    response = ['y', 'n']
    start = 0
    while True:
        answer = input("Would you like to take a look at the raw data you filtered? y/n: ").lower()
        if answer not in response:
            print("Please choose from y/n (n to proceed to your chosen filters and analysis): ")
        elif answer == 'y':
                print(df.iloc[start:start+5, 1:])
                start += 5
        elif answer == 'n':
            break
    if answer == 'y':
        while True:
            answer_two = input("Would you like to load more raw data? y/n: ").lower()
            if answer_two in response:
                if answer_two == 'y':
                    start += 5
                    print(df.iloc[start:start+5, 1:])
                else:
                    break
            else:
                print("Please choose from y/n (n to proceed to your chosen filters and analysis): ")

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    common_month = df['month'].mode()[0]
    print("The most common month is: ", common_month)
    # display the most common day of week
    common_day = df['day_of_week'].mode()[0]
    print("The most common day is: ", common_day)
    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print("The most common hour is: ", common_hour)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' *40)
    return common_month, common_day, common_hour

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("The most common start station is: ", common_start_station)
    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("The most common end station is: ", common_end_station)
    # display most frequent combination of start station and end station trip
    common_combination = df[['Start Station', 'End Station']].mode()
    print("The most common combination station is: \n", common_combination)
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' *40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("The total travel time is: ", total_travel_time)
    # display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("The average travel time is: ", avg_travel_time)
    # display max travel time
    max_travel_time = df['Trip Duration'].max()
    print("The max travel time is: ", max_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' *40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types_count = df['User Type'].value_counts()
    print("# of users for each user type: ", user_types_count)
    # Display counts of gender
    if 'Gender' in df:
        gender_count = df['Gender'].value_counts()
        print('\nCount of Gender:\n {}'.format(gender_count))
    else:
        print('\nError: the dataset does not contain information for \'Count of Gender\'')


    # Display earliest, most recent, and most common year of birth

    if 'Birth Year' in df:
        earliest_yob= int(df['Birth Year'].min())
        print('\nEarliest Date of Birth: {}\n'.format(earliest_yob))
    else:
        print('\nError: the dataset does not contain information for \'Earliest Birth Year\'\n')

    if 'Birth Year' in df:
        most_recent_yob= int(df['Birth Year'].max())
        print('\nMost Recent Year of Birth: {}\n'.format(most_recent_yob))
    else:
        print('\nError: the dataset does not contain information for \'Most Recent Birth Year\'\n')

    if 'Birth Year' in df:
        Most_common_yob= int(df['Birth Year'].mode())
        print('\nMost Common Year of birth: {}\n'.format(Most_common_yob))
    else:
        print('\nError: the dataset does not contain information for \'Most Common Birth Year\'\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-' *40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        raw_data_selection(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)


        restart = input('\nWould you like to restart? Enter y/n.\n')
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
