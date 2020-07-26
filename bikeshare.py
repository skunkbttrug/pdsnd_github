import time
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", 100)#General setting for the layout output of the Dataframe

CITY_DATA = { 'Chicago': 'raw_data/chicago.csv',
              'New York City': 'raw_data/new_york_city.csv',
              'Washington': 'raw_data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data! \n')
    
    # get user input for city (chicago, new york city, washington)
    city = input('Which city would you like to investigate? Choose one between "Chicago", "New York City" or "Washington".\n').title()
    
    while city not in ['Chicago', 'New York City', 'Washington']:
        city = input('\nYour input is incorrect. Valid options are: "Chicago", "New York City" or "Washington".\n').title()
	
    print()
	
    # get user input for month (all, january, february, ... , june)
    month = input('Would you like to filter the data for a particular month? If yes, choose one between "January", "February", "March", "April", "May" or "June". If not, type "All" to see the data for all months.\n').title()
    
    while month not in ['January', 'February', 'March', 'April', "May", 'June', 'All']:
        month = input('\nYour input is incorrect. Valid options are: "January", "February", "March", "April", "May", "June" or "All".\n').title()
    
    print()
    
    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Would you like to filter the data for a particular day of the week? If yes, choose one between "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" or "Sunday". If not, type "All" to see the data for all days of the week.\n').title()
    
    while day not in ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday', 'All']:
        day = input('\nYour input is incorrect. Valid options are: "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" or "All".\n').title()
	
    print()
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
    df = pd.read_csv(CITY_DATA[city], index_col=0)

    df['Start Time'] = pd.to_datetime(df['Start Time']) # This converts the "Start Time" column to datetime
    df['month'] = df['Start Time'].dt.month # This extracts the month from the "Start Time" column and creates a new column
    df['day_of_week'] = df['Start Time'].dt.day_name() # This extracts the day of week from the "Start Time" column and creates a new column

    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'All':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """
	Prints statistics on the most frequent times of travel based on the user's input.
	
	Args:
        df - Pandas DataFrame containing city data filtered by month and day
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        None
	"""
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # prints the most common month only if the user types in "All". Otherwise this statistic is ignored since the answer will be the user's input.
    if month == 'All':
        popular_month = df['month'].value_counts().idxmax()
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        popular_month = months[popular_month - 1]
        print('The most popular month was {}.'.format(popular_month))

    # displays the most common day of week only if the user types in "All". Otherwise it ignores this statistic since the answer will be the user's input.
    if day == 'All':
        popular_day = df['day_of_week'].value_counts().idxmax()
        print('The most popular day of the week was {}.'.format(popular_day))

    # displays the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].value_counts().idxmax()
    print('The most popular starting hour was {}:00.'.format(popular_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Prints statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # displays the most commonly used start station
    popular_start_station = df['Start Station'].value_counts().idxmax()
    print('The most popular starting station was {}.'.format(popular_start_station))

    # displays most commonly used end station
    popular_end_station = df['End Station'].value_counts().idxmax()
    print('The most popular ending station was {}.'.format(popular_end_station))

    #displays most frequent combination of start station and end station trip
    df['trip'] = df['Start Station'] + ' - ' + df['End Station'] # This merges the columns "Start Station" and "End Station" into a new column
    popular_trip = df['trip'].value_counts().idxmax()
    print('The most popular trip was {}.'.format(popular_trip))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Prints statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # displays total travel time
    total_travel_time = df['Trip Duration'].sum()
    total_travel_time = pd.to_timedelta(int(total_travel_time), unit='s')
    print('The total travel time was {} hours.'.format(total_travel_time))

    # displays mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    mean_travel_time = pd.to_timedelta(int(mean_travel_time), unit='s')
    print('The average travel time of a trip was {} hours.'.format(mean_travel_time))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Prints statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    total_user_types = df['User Type'].value_counts()
    print("Number of bike rides by user type:\n{}\n".format(total_user_types.to_string()))#method (.to_string) used just for aesthetic

    # Displays counts of gender
    if city in ['Chicago', 'New York City']:
        total_user_gender = df['Gender'].value_counts(dropna = False)#counts NaN values too
        total_user_gender = total_user_gender.rename(index={np.nan : 'Not specified'}) #renames NaN values to "Not specified"
        print("Number of bike rides by user gender:\n{}\n".format(total_user_gender.to_string()))#method (.to_string) used just for aesthetic

    #Displays earliest, most recent, and most common year of birth
        df['Birth Year'] = pd.to_numeric(df['Birth Year'])# converts column data type to numeric in order get max and min values
        oldest_yob = df['Birth Year'].min()
        print("Year of birth of the oldest customer: {}".format(int(oldest_yob)))
    
        youngest_yob = df['Birth Year'].max()
        print("Year of birth of the youngest customer: {}".format(int(youngest_yob)))
    
        common_yob = df['Birth Year'].value_counts().idxmax()
        print("Most common year of birth: {}\n".format(int(common_yob)))

    print("This took %s seconds." % (time.time() - start_time))
    print('-'*40)


def get_raw(df):
    """Prints 5 lines of raw data each time upon user's request
	
	Args:
        df - Pandas DataFrame containing city data filtered by month and day

    Returns:
        None
	"""   
    df = df.drop(columns=['month', 'day_of_week', 'hour', 'trip']) #removes the columns added by the script to return to the raw data's status
        
    #asks the user the first time
    raw_data = input('\nWould you like to see the first 5 lines of the raw data? Enter yes or no.\n').title()
    while raw_data not in ['Yes', 'No']:
        raw_data = input('\nYour input was incorrect. Please type "yes" or "no".\n').title()
    
    if raw_data == "Yes":
        a = 0
        b = 5
        print(df[a:b])
        
        #asks the user again if the next 5 rows of the data should be displayed
        raw_data_next = input('\nWould you like to see the next 5 lines of the raw data? Enter yes or no.\n').title()
        while raw_data_next not in ['Yes', 'No']:
            raw_data_next = input('\nYour input was incorrect. Please type "yes" or "no".\n').title()
        
        #loop for the next groups of 5 rows until the user answers "No" or the total number of rows in the dataframe is reached
        while (raw_data_next == "Yes"):
            if b <= len(df.index):
                a += 5
                b += 5
                print(df[a:b])
                
                raw_data_next = input('\nWould you like to see next 5 lines of the raw data? Enter yes or no.\n').title()  
                while raw_data_next not in ['Yes', 'No']:
                    raw_data_next = input('\nYour input was incorrect. Please type "yes" or "no".\n').title()
            
            else:
                print('\n-----There are no more lines available-----')
                break
                
                     
def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        get_raw(df)
        
        restart = input('\nWould you like to restart? Enter "yes" or "no".\n')
        if restart.lower() != 'yes':
            print("\nYour analysis is over.\n")
            break


if __name__ == "__main__":
	main()