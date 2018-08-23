import matplotlib.pyplot as plt
import time
import pandas as pd
from pandas import DataFrame as df
import numpy as np
import calendar
import seaborn as sb

class Data_prep:

    """This class contains all methods to filter and load data based on city, month, and day chosen by the user"""

    print('\n Hello, we will explore bikeshare data from three US cities. Let\'s do it! \n')
    
    def __init__(self):
        
        """These dictionaries primarily enable the filtering process of choosing a city, month, and day, 
        including all of cities, months, and day. These dictionaries secondarily facilitate the 
        conversion of cities, months, and days into integers.""" 
        
        self.city_data = { '1': 'chicago.csv',
                     '2': 'new_york_city.csv',
                      '3': 'washington.csv' }
        self.cities = {'Chicago':'1', 'New York': '2', 'Washington': '3', 'All':'4'}
        self.months = {'January':'1', 'February':'2', 'March':'3', 'April':'4','May':'5', 'June':'6', 'All':'7'}
        self.days = {'Monday':'0', 'Tuesday':'1', 'Wednesday':'2', 'Thursday':'3', 
                         'Friday':'4', 'Saturday':'5', 'Sunday':'6', 'All':'7'}
        
        self.err_msg = 'Invalid, try again...'

    def filter_city(self):  #this method filters and returns the city
        global city

        while True:
            city = input('Choose your city to explore: Chicago = 1, New York =2, Washington = 3, All = 4: \n')
            if city in self.cities.values():
                city_name = [k for k,v in self.cities.items() if v == city]
                print('You chose', city_name[0].capitalize())
                print()
                break
            else:
                try:
                    print()
                    print(self.err_msg)

                except:
                    pass

        return city

    def filter_month(self): #filters and returns month from January to June
        global month

        while True:
            print()
            month = input('Choose your month -- Jan = 1, Feb = 2, Mar = 3, Apr = 4, May = 5, June = 6, All = 7: \n').capitalize()
            if month not in self.months.values():
                    print(self.err_msg)
            else:
                try: 
                    if month != str(7):
                        print('You chose', calendar.month_name[int(month)])
                        print()
                    else:
                        print("You chose 'All'")
                    break
                except: 
                    print(self.err_msg)

        month = int(month) #prefer to keep all inputs numerical so use convert the output to integer

        return month

    def filter_day(self): #filters and returns day 
        global day

        while True:
            print()
            day = input('Choose your day -- Mon = 0, Tues = 1, Wed = 2, Thur = 3, Fri = 4, Sat = 5, Sun = 6, All = 7: \n').capitalize()
            if day not in self.days.values():
                    print(self.err_msg)
            else:
                try: 
                    if day != str(7):
                        print('You chose', calendar.day_name[int(day)])
                    else: 
                        print("You chose 'All'")
                    break
                except: 
                    print(self.err_msg)

        day = int(day)

        return day

    def load_data(self, city, month, day):

        #if user inputs 4 this loads the three csv city files into a dataframe with the cities
        #with the city dataframes stacked on top of each other to explore
        #data from all three cities

        if city=='4':
            df = pd.concat([pd.read_csv('chicago.csv'), 
                            pd.read_csv('new_york_city.csv'),
                            pd.read_csv('washington.csv')], 
                           axis=0)
        #else pandas just reads and loads the one chosen city into a pandas dataframe
        else:
            df = pd.read_csv(self.city_data[city])
        
        #this gives the user the option of seeing the raw data
        while True:
            raw_data = input('\n Would you like to see the raw data: Y or N? \n').capitalize()
            if raw_data == 'Y':
                print(df.head(5))
                count = 5
                while True:
                    more = input('\n Would you like to see more?\n').capitalize()
                    if more == 'Y':
                        count += 1
                        more_raw_data = df.head(count)
                        print(more_raw_data)
                    else:
                        print('\nOk, let\'s get those statistics!\n')
                        break
                break
            else:
                print('\nOk, let\'s get those statistics!\n')
                break

        #Changes name of user column from 'Unnamed: 0' to 'User Id'
        column_rename = df.columns.values 
        column_rename[0] = 'User Id'
        df.columns = column_rename

        # convert the Start Time column to datetime
        df['Start Time'] = pd.to_datetime(df['Start Time'])
        df['End Time'] = pd.to_datetime(df['End Time'])

        # extracts month, day of the week, and hour from Start Time to create new columns
        df['year'] = df['Start Time'].dt.year
        df['month'] = df['Start Time'].dt.month
        df['day_of_week'] = df['Start Time'].dt.dayofweek
        df['start hour'] = df['Start Time'].dt.hour
        df['end hour'] = df['End Time'].dt.hour

        # filter by month if applicable
        if month != 7:
            # use the index of the months list to get the corresponding int
            months = list(range(1,8)) 
            month = months.index(month) + 1

            # filters by month to create the new dataframe
            df = df[df['month'].values == month]

        # filters by day of week if applicable
        if day != 7:
            # filter by day of week to create the new dataframe
            df = df[df['day_of_week'].values == day]

        return df
            
class Stats(Data_prep): 
    
    """this class bundles together all statistics about time(months, days, and hours), start and end stations,
    trip durations, and statistics about the user such as gender, birth year, and user type"""
    
    
    def time(self, df): #this method gets the data from the chosen month and day, and gathers data of users for each hour 

        print(str('\nCalculating The Most Frequent Times of Travel...\n').upper())
        start_time = time.time()
        year = df['year'].min()

        print('All data from year:', year)
        print()
        # Displays the most common month
        month_mode = df['month'].mode()[0]
        month_counts = df['month'].value_counts().reset_index()

        base_color = sb.color_palette()[0]#the color for all the seaborn bar plots
        
        if month == 7:
            print('Number of users each month: \n')
            print(month_counts.to_string(header = None, index = None))
            print()
            print('The most common month:', calendar.month_name[month_mode])
            df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
            month_counts = df['month'].value_counts(ascending=True)

            #visualizes the number of users per month
            #month_counts.plot(title='Number of Users per Month', kind='bar', legend = False)
            #plt.show()
            sb.countplot(data=df, x='month', order=['Jan', 'Feb','Mar','Apr','May','Jun'], color=base_color);
            plt.show()
            

        # Displays the most common day of week
        day_mode = df['day_of_week'].mode()[0]
        day_counts = df['day_of_week'].value_counts().reset_index()

        if day == 7:
            print()
            print('The most common day of the week: ', calendar.day_name[day_mode])
            df['day_of_week'] = df['day_of_week'].apply(lambda x: calendar.day_abbr[x])
            day_counts = df['day_of_week'].value_counts(ascending=True)

            #visualizes the number of users per day
            #day_counts.plot(title='Users per Day', kind='bar', legend = False)
            #plt.show()
            sb.countplot(data=df, x='day_of_week', order=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], color=base_color);
            plt.show()

        # Displays the most common start hour of the day
        startHour_mode = df['start hour'].mode()[0]
        print()
        print('The most common start hour of the day: ', startHour_mode)
        print()

        #Displays the most common end hour of the day
        endHour_mode = df['end hour'].mode()[0]
        print('Most common end hour of the day: ', endHour_mode)
        print()

        #Displays the earliest start hour of the day 
        startHr_min = df['start hour'].min()
        print('Earliest start hour:', startHr_min)
        print()

        #Displays latest start hour of the day
        startHr_max = df['start hour'].max()
        print('Latest start hour', startHr_max)
        print()

        #hour_counts.plot(x = 'hour', title='Users Per Hour', kind='bar', legend = False)
        #plt.show()
        sb.countplot(data=df, x='start hour', color=base_color);
        plt.show()

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)


    def station(self,df):
        print(str('\nCalculating The Most Popular Stations and Trip...\n').upper())
        start_time = time.time()

        # Displays most commonly used start station
        start_station_mode = df['Start Station'].mode()[0]
        print('Most common start station: ', start_station_mode)

        # Displays most commonly used end station
        end_station_mode = df['End Station'].mode()[0]
        print()
        print('Most common end station: ', end_station_mode)
        print()

        # TO DO: display most frequent combination of start station and end station trip
        loc_combo_mode = max(df.groupby(['Start Station', 'End Station']).size().index)
        print('Most popular trip -- FROM: %s, TO: %s '  % (loc_combo_mode[0], loc_combo_mode[1]))
        print()
        least_pop_trip = min(df.groupby(['Start Station', 'End Station']).size().index)
        print('Least popular trip -- FROM %s, TO: %s' % (least_pop_trip[0], least_pop_trip[1]))
        print()
        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def trip_duration(self,df):

        print(str('\nCalculating Trip Duration...\n').upper())
        start_time = time.time()

        # TO DO: display total travel time
        total_time = df['Trip Duration'].sum() 
        print('Total travel time: %s days %s hours %s minutes %.2f seconds' % (total_time//3600//24, total_time//3600%24,
                                                                               total_time%3600//60, total_time%3600%60))
        print()

        # TO DO: display mean travel time
        time_avg = df['Trip Duration'].mean()
        print('Travel time average: %s minutes %.2f seconds' % (time_avg//60, time_avg%60))
        print()

        #Displays the median travel time to get a better idea of central tendency
        time_median = df['Trip Duration'].median()
        print('Travel time median: %s minutes %.2f seconds' % (time_median//60, time_median%60))
        print()

        #Displays maximum trip duration
        time_max = df['Trip Duration'].max()
        print('Longest trip: %s hours %s minutes %.2f seconds' % (time_max//3600, time_max%3600//60, 
                                                                time_max%3600%60))
        print()

        #Displays minimum trip duration
        time_min = df['Trip Duration'].min()
        print('Shortest trip: %s seconds' % (time_min))
        print()


        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)

    def user(self, df):
        print(str('\nCalculating User Stats...\n').upper())
        start_time = time.time()

        # Displays counts of user types 
        user_type = df['User Type'].value_counts().reset_index()
        print('User type counts:\n\n', user_type.to_string(header=None, index=None))
        print()

        user_type_counts = df['User Type'].value_counts()
        subscriber = df['User Type'].value_counts()[0] #displays number of subscribers
        customer = df['User Type'].value_counts()[1]#displays number of customers

        percent_subscriber = (subscriber/(subscriber + customer))*100 #shows percent of users as  subscribers
        percent_customer = (customer/(customer + subscriber))*100 #shows percent of users as customers
        print('Percentage of users as subscribers: {0:.2f}%'.format(percent_subscriber))
        print()
        print('Percentage of users as customers: {0:.2f}%'.format(percent_customer))
        print()

        #visualizes the percentages of customers and subscribers in a pie chart for better comparison
        user_type_counts.plot(kind='pie', title='User Type', autopct='%1.0f%%').set_ylabel('')
        plt.show()
        print()
        sb.countplot(data=df, x='User Type');
        plt.show()
        print()


        try:
            #Displays counts of male and female
            gender = df['Gender'].value_counts().reset_index()
            print('Gender counts:\n\n ', gender.to_string(header=None, index=None))
            print()
            gender_counts = df['Gender'].value_counts()
            male = gender_counts[0]
            female = gender_counts[1]

            #Displays percentages of users as male or female
            percentage_male = (male/(male + female))*100
            percentage_female = (female/(female + male))*100
            print('Percentage of users as males: {0:.2f}%'.format(percentage_male))
            print()
            print('Percentage of users as females: {0:.2f}%'.format(percentage_female))
            print()

            #visualizes the percentages of users as female and male as a pie chart
            gender_counts.plot(kind='pie', title='Gender', autopct='%1.0f%%').set_ylabel('')
            plt.show()
            print()
            sb.countplot(data=df, x='Gender');
            plt.show()
            print()
            gender_userType = df.groupby(['Gender', 'User Type']).size().reset_index()
            print(gender_userType.to_string(header=None, index=None))
        except KeyError:
            print('Washington has no gender data')

        print()

        # Displays earliest, the latest, and most common year of birth
        try:
            birthYear_mode = df['Birth Year'].mode()[0]
            print('Most common birth year: ', int(birthYear_mode))
            print()
            mostRecent_birthYear = df['Birth Year'].max()
            print('Most recent birth year:', int(mostRecent_birthYear))
            print()
            earliest_birthYear = df['Birth Year'].min()
            print('Earliest birth year:', int(earliest_birthYear))
            df['Birth Year'].plot(kind='hist', title='Birth Year Histogram')
            plt.show()
        except KeyError:
            print('Washington has no birth year data')

        print("\nThis took %s seconds." % (time.time() - start_time))
        print('-'*40)
        
    def run(self): #this method calls and runs the whole program
        city = Data_prep().filter_city() #gets chosen city
        month = Data_prep().filter_month() #gets chosen month
        day = Data_prep().filter_day() #gets the choice for day
        df = Data_prep().load_data(city, month, day) #loads the data into pandas dataframe for further analysis
        time_stats = Stats().time(df) #get the statistics for time
        station = Stats().station(df) #gets stats for start and end stations
        trip_d = Stats().trip_duration(df) #get stats for trip duration 
        users = Stats().user(df) #get stats about users' birth years, gender, and user type
        return city, month, day, df, time_stats, station, trip_d, users
        
def main():
    while True:
        Stats().run()
        
        while True:
            valid_responses = ['Y', 'N']
            restart = input('\nWould you like to restart? Enter Y or N.\n').capitalize()
            if restart not in valid_responses:
                print('Invalid input. Y or N?')
            elif restart == 'Y':
                Stats().run()
            else:
                print('Goodbye')
                break
        break
            
if __name__ == "__main__":
	main()