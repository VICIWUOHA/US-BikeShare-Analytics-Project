import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'data/chicago.csv',
              'new york city': 'data/new_york_city.csv',
              'washington': 'data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!.. Are you Ready?')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while True:
        cities= ['chicago','new york city','washington']
        city= input("\n Which city would you like to analyse? (Chicago, New york city, Washington) \n").lower()
        if city in cities:
            break
        else:
            print("\n OOps...Please enter a valid city name")
    print(f"\nYou have chosen to see data for {city.title()} .") 


    # get user input for month (all, january, february, ... , june)
    while True:
        months = ['january', 'february', 'march', 'april', 'may', 'june','all']
        print("\nPlease enter a month, between January to June or type 'all' if you don't want to filter the dataset:")
        month = input('\n So.. what month would you like to explore ?: \n').lower()
        if month in months:
            break
        else:
            print('\n Seems you enetered a wrong month name- Kindly Recheck to continue your ride..')

    if month == 'all' :
        print('\n Alright You have opted to see data for all Months.. Lets go')
    else:
        print(f"\nYou have chosen to see data for the month of {month.title()} Let's Continue your ride...")


    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday','All']
        day = input("\nWhich day of the week would you like to consider? (Monday, Tuesday, Wednesday, Thursday,\n"+
        "Friday, Saturday or Sunday)? Type 'all' to see data for all days \n").title()

        if day != 'All' and day in days :
            print(f"\nYou have chosen to see data for {day.title()} Let's get running...")
            break
        elif day == 'All':
            print("\n .....Ok Let's take a ride to explore data for all days")
            break
        else:
            print ('Please enter a correct day as suggested earlier')


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
    df = pd.read_csv(CITY_DATA[city])
   
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time']) 

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
    
        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]
    
    return df


def time_stats(df,month,day):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    if month == 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        most_common_month = df['month'].mode()[0]
        most_common_month_name = months[(most_common_month-1)] 
        print('\n The Most Common month is {}'.format(most_common_month_name).title())

    # display the most common day of week
    if day == 'All':
        most_common_day = df['day_of_week'].mode()[0]
        print('\n The Most popular day for bike rides is {}'.format(most_common_day).title())


    # display the most common start hour
    df['Start Hour'] = df['Start Time'].dt.hour
    most_common_hour = df['Start Hour'].mode()[0]
    print('\n Interestingly, most bike rides started at {} :00 hrs'.format(most_common_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    mostcommon_start_station= df['Start Station'].mode()[0]
    print("\nMost Bike riders commence their journey at {}".format(mostcommon_start_station))


    # display the most commonly used end station
    mostcommon_end_station= df['End Station'].mode()[0]
    print("\nThe most commonly used End Station by Riders is {}".format(mostcommon_end_station))

    # display the most frequent combination of start station and end station trip
    df['StartAndEndStation']=df['Start Station']+" "+"to"+" "+ df['End Station']
    mostcommon_startstop= df['StartAndEndStation'].mode()[0]
    print("\nThe most frequent combination of Start and End Stations is from {} ".format(mostcommon_startstop))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    # get the total travel time in hrs, minutes and seconds
    minute,second=divmod(total_travel_time,60)
    hour,minute=divmod(minute,60)
    print("\nThe total trip duration: {} hour(s) {} minute(s) {} second(s)".format(hour,minute,second))
    
    # display mean travel time
    average_duration=round(df['Trip Duration'].mean())
    mins,secs=divmod(average_duration,60)
    if mins>60:
        hrs,mins=divmod(mins,60)
        print("\nThe total trip duration: {} hour(s), {} minute(s) and {} second(s)".format(hrs,mins,secs))
    else:
        print("The total trip duration: {} minute(s) {} second(s)".format(mins,secs))



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df,city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The Unique User types and their population are as follows:\n {}'.format(str(user_types)))


    # Display counts of gender
    # Washington has no gender, hence a try statement to check if there is gender data within filtered data
    try:
        gender_count = df['Gender'].value_counts()
        print("\n\n For Your Selected data, gender counts are as follows:\n" , gender_count)
    except:
        print("\n There's No Gender data for this dataset...")


    # Display earliest, most recent, and most common year of birth
    try:
        earliest_birthyear = int(df['Birth Year'].max())
        most_recent_birthyear = int(df['Birth Year'].min())
        most_common_birthyear = int(df['Birth Year'].mode()[0])

        print(f"\nThe earliest birth year is : {earliest_birthyear}\n\n" + 
        f"The most recent year of birth is: {most_recent_birthyear}\n\n"+
        f"The most common birth year is: {most_common_birthyear}")
    except:
        print("\nOk...  We couldn't Find any birth year data in this dataset.")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    print("\nThanks For Exploring this BIke Share data. More coming Soon on our web app.")


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df,month,day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df,city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
