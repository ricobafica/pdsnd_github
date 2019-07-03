import time
import pandas as pd
import calendar

CITY_DATA = { 'Chicago': 'chicago.csv',
              'New York': 'new_york_city.csv',
              'Washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input("Select a city from {}, {} or {}:".format(*CITY_DATA.keys())).strip().title()
        if city in CITY_DATA.keys():
            break
        else:
            print("Incorrect value. Please write an eligible city!")

    times = ['month', 'day', 'none']
    while True:
        time_filter = input("Would you like to filter the data by month, day, or not at all? Type \"none\" no time filter:").lower()
        if time_filter in times:
            break
        else:
            print("Incorrect value. Please write an eligible filter to the time!")

    # TO DO: get user input for month (all, january, february, ... , june)
    if time_filter == 'month':
        eligible_month = False
        months = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
        while eligible_month == False:
            month = input("Which month? January, February, March, April, May, June, or All: ").title()
            if month in months:
                day = 'All'
                eligible_month = True
            else:
                print("Incorrect value. Please write an eligible filter to month!")
    elif time_filter == 'day':
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
        eligible_day = False
        days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']
        while eligible_day == False:
            day = input("Which day of week to filter? Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, All: ").title()
            if day in days:
                month = 'All'
                eligible_day = True
            else:

                print("Incorrect value. Please write an eligible filter to day o week!")
    else:
        month = 'All'
        day = 'All'

    print('-'*80)
    print("Thanks, We will calculate Bikeshare statistics filtered by:\n City: {} \n Month: {} \n Day: {}".format(city, month, day))
    print('-'*80)
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
    start_time = time.time()

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    # Since the month parameter is given as the name of the month,
    # you'll need to first convert this to the corresponding month number.
    # Then, select rows of the dataframe that have the specified month and
    # reassign this as the new dataframe.

    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    print("The first 5 rows for the bikeshare data from {} are:\n".format(city), df.head())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('Calculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()[0]
    print(' Most Common Month:', calendar.month_name[common_month])

    # TO DO: display the most common day of week
    popular_weekday = df['day_of_week'].mode()[0]
    print(' Most Popular Day of Week:', popular_weekday)

    # find the most common hour (from 0 to 23)
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print(' Most Popular Start Hour:', popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('Calculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_popular = df['Start Station'].mode()[0]
    print(' Most Common Start Station:', start_popular)

    # TO DO: display most commonly used end station
    end_popular = df['End Station'].mode()[0]
    print(' Most Common End Station:', end_popular)

    # TO DO: display most frequent combination of start station and end station trip
    df['Trip Combined'] = 'FROM ' + df['Start Station'] + ' TO ' + df['End Station']
    trip_popular = df['Trip Combined'].mode()[0]
    print(' Most Common Trip:', trip_popular)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('Calculating Trip Duration...\n')
    start_time = time.time()
    total_travel_time = df['Trip Duration']

    # TO DO: display total travel time
    print(" Total Travel Time Duration in sec:", total_travel_time.sum())
    print(" Total Travel Time Duration in years:", total_travel_time.sum()/(60*60*24*365))

    # TO DO: display mean travel time
    print("\n Average Travel Time Duration in sec:", total_travel_time.mean())
    print(" Average Travel Time Duration in minutes:", total_travel_time.mean()/60)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('Calculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print(" Counts of each user Type:\n",user_types)

    # TO DO: Display counts of gender
    try:

        gender_qty = df['Gender'].value_counts()
        print("\n Counts of Each Gender:\n",gender_qty)

        # TO DO: Display earliest, most recent, and most common year of birth
        earliest_birth_year = int(df['Birth Year'].min())
        last_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mean())

        print("\n Earliest Year of Birth:", earliest_birth_year)
        print(" Most Recent Year of Birth:", last_birth_year)
        print(" Most Common Year of Birth:", common_birth_year)

    except KeyError:
        print("\n Sorry about earliest, most recent, and most common year of birth information:")
        print(" Washington doesn\'t have data about either Gender and Birth from its users")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*80)


def main():
    while True:

        city, month, day = get_filters()
        df = load_data(city, month, day)
        go_on = False
        index = 0
        while go_on == False:
            index += 1
            next_function = input("To continue press y: ").lower()
            if next_function == 'y':
                if index == 1:
                    time_stats(df)
                elif index == 2:
                    station_stats(df)
                elif index == 3:
                    trip_duration_stats(df)
                elif index == 4:
                    user_stats(df)
                    go_on = True
            else:
                go_on = True

        restart = input('\nWould you like to restart? Enter "yes" to continue or any other key to exit.\n')
        if restart.lower() != 'yes':
            break

if __name__ == "__main__":
   	main()
