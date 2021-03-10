import numpy  as np
import pandas as pd


"""Asks the user which city he wants to analyze (with data validation).
Returns:
    - loc: name of the city to analyze       """
def get_city():
    while True:
        city = input("* Would you like to see data for Chicago, New York, or Washington?:\n")
        loc  = city.lower().strip()
        if loc == "chicago":
            print("\nOk! let's explore Chicago data")
            return loc
            break
        elif loc == "new york":
            print("\nOk! let's explore New York data")
            return loc
            break
        elif loc == "washington":
            print("\nOk! let's explore Washington data")
            return loc
            break
        else:
            print("*** We need a valid location\n")


"""Asks the user what data to use to analyze (with data validation).
Returns:
    - var1: month to analyze
    - var2: day to analyze         """
def get_filter():
    # Data validation for the filters.
    while True:
        stuff = input("* Would you like to filter the data by month, day, both, or not at all? Type none for no time filter: \n")

        # Data validation to "month" filter
        if stuff.lower().strip() == "month":
            while True:   
                month = input("Which month? January, February, March, April, May or June?:\n")
                var1  = month.lower().strip()
                var2  = None
                if var1=="january" or var1=="february" or var1=="march" or var1=="april" or var1=="may" or var1=="june":
                    return [var1, var2]
                    break
                else:
                    print("*** Please, select a valid month")

        # Data validation to "day" filter.
        elif stuff.lower().strip() == "day":
            while True:
                day  = input("Which day?: \n")
                var1 = None
                var2 = day.lower().strip()
                if var2=="monday" or var2=="tuesday" or var2=="wednesday" or var2=="thursday" or var2=="friday" or var2=="saturday" or var2=="sunday":
                    return [var1,var2]
                    break
                else:
                    print("*** Please, select a valid day")

        #Data validation to "both" filter
        elif stuff.lower().strip() == "both":
            while True:
                month = input("Please, select a month (January, February, March, April, May or June?):\n")
                var1  = month.lower().strip() 
                if var1=="january" or var1=="february" or var1=="march" or var1=="april" or var1=="may" or var1=="june":
                    while True:
                        day  = input("Please, select a day:\n")
                        var2 = day.lower().strip()
                        if var2=="monday" or var2=="tuesday" or var2=="wednesday" or var2=="thursday" or var2=="friday" or var2=="saturday" or var2=="sunday":
                            return [var1, var2]
                            break
                        else:
                            print("*** Please, select a valid day")
                    break
                else:
                    print("*** We need a valid month")   

        # Data validation to "none" filter
        elif stuff.lower().strip() == "none":
            var1 = None
            var2 = None
            return [var1, var2]

        else:
            print("*** We need a valid option")


"""Loads the data according to the specified filters.
Args:
    - loc: city to analyze
    - month: month to analyze (None, if the user does not want month filter)
    - day: day to analyze (None, if the user does not want month filter)
Returns:
    - df = dataframe with filtered data    """
def load_data(loc, month, day):
    CITY_DATA = { 'chicago': 'chicago.csv',
                  'new york': 'new_york_city.csv',
                  'washington': 'washington.csv' }

    df = pd.read_csv(CITY_DATA[loc])
    df.rename(columns={" ": "ID"}, inplace = True)
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df["hour"]  = df['Start Time'].dt.hour
    df["day"]   = df['Start Time'].dt.day_name()
    df["month"] = df['Start Time'].dt.month
    df["combination"] = df['Start Station'] + ", " + df['End Station']

    if month != None:
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month  = months.index(month) + 1
        df = df[df['month'] == month]

    if day != None:
        df = df[df['day'] == day.title()]


    #copy of the dataframe to show to the user
    data_show = df.drop(["combination" ,"day" ,"month" ,"hour"], axis=1)

    number = 5
    print("\n* This is summary of data table\n")
    print(data_show.head(number))

    while True:
        indicator = input("Would you like to see another 5 rows of the table? (type yes/no)\n")
        indicator.lower().strip()
        if indicator == "yes" or indicator== "y":
            number = number + 5 
            print("\n* This is summary of data table\n")
            print(data_show.head(number))
        elif indicator == "no" or indicator== "n":
            break
        else:
            print("***Please, select a valid option")
    return df


"""Print information about filtered data
Args:
    - dataframe: dataframe with filtered data (obtained from load_data() function)
    - loc: city to analyze (obtained from get_city() function)
    - month: month to analyze (obtained from get_filter() function)
    - day: day to analyze (obtained from get_filter() function)
returns:
    - prints data abou consulted information         """
def get_data(dataframe, loc, month, day):

    #Information about popular time of travel
    popular_hour  = dataframe['hour'].mode()[0]
    popular_month = dataframe['month'].mode()[0]
    popular_day   = dataframe['day'].mode()[0]

    #Information about stations anc combinations
    start_station = dataframe['Start Station'].mode()[0]
    end_station   = dataframe['End Station'].mode()[0]
    popular_combination = dataframe['combination'].mode()[0]

    
    #Information about trip times
    trip_sum  = dataframe.groupby(["Start Station", "End Station"])["Trip Duration"].sum()
    trip_mean = dataframe.groupby(["Start Station", "End Station"])["Trip Duration"].mean()
    trip_sum_total  = dataframe["Trip Duration"].sum()
    trip_mean_total = dataframe["Trip Duration"].mean() 

    #Display information
    print("\n---INFORMATION ABOUT TIME OF TRAVEL---")
    list_month =["January", "February", "March", "April", "May", "June"]

    if day == None and month == None:
        print("* The most popular month is:", list_month[popular_month - 1])
        print("* The most popular day is:", popular_day)
        print("* The most popular hour is:", popular_hour, "o\'clock\n")
    elif day == None and month != None:
        print("* The most popular day is:", popular_day)
        print("* The most popular hour is:", popular_hour, "o\'clock\n")
    elif day !=None and month == None:
        print("* The most popular month is:", list_month[popular_month - 1])
        print("* The most popular hour is:", popular_hour, "o\'clock\n")
    else:
        print("*The most popular hour is:", popular_hour, "o\'clock\n")

    print("\n---INFORMATION ABOUT POPULAR STATIONS---")
    print("* Most commonly used start station is:", start_station)
    print("* Most commonly used end station is:", end_station)
    print("* Most commonly used combination of start station and end station trip:", popular_combination, "\n")



    print("\n---INFORMATION ABOUT TRIP TIMES---")
    print("* The total trip time recorded is:", trip_sum_total, "seconds")
    print("* And the mean of trip time is:", trip_mean_total, "seconds")





    
    # Displays additional information on trip times, if the user chooses.
    count_s = 5
    count_m = 5

    while True:
        enter_data = input("* Would you like to see the statistics per trip? (enter yes/no)\n")

        if enter_data.lower().strip() == "yes" or enter_data.lower().strip() == "y":
            print("\n* This is the first", count_s, "files about total time, separated by trip:\n-------------------------------------------------------------------------")
            print(trip_sum.head(count_s), "\n")

            while True:
                selection_files = input("* Would you like to see another 5 rows of the table? (type yes/no)\n")
                selection_files.lower().strip()

                if selection_files == "yes" or selection_files == "y":
                    count_s = count_s + 5
                    print("\n* This is the first", count_s, "files about total time, separated by trip:\n---------------------------------------------------------------")
                    print(trip_sum.head(count_s), "\n")

                elif selection_files == "no" or selection_files == "n":
                    break

                else:
                    print("***Please, select a valid option")
            
            print("\n* And this is the first", count_m, "files about mean of each trip:\n-----------------------------------------------------------------------------")
            print(trip_mean.head(count_m))

            while True:
                sel_files = input("* Would you like to see another 5 rows of the table? (type yes/no)\n")
                sel_files.lower().strip()

                if sel_files == "yes" or sel_files == "y":
                    count_m = count_m + 5
                    print("\n* This is the first", count_m, "files about total time, separated by trip:\n-------------------------------------------------------------")
                    print(trip_sum.head(count_m), "\n")

                elif sel_files == "no" or sel_files == "n":
                    break

                else:
                    print("***Please, select a valid option")

            break

        elif enter_data.lower().strip() == "no" or enter_data.lower().strip() == "n":
            break

        else:
            print("*** Please, enter a valid option")

    print("\n")
    print("\n")
    print("---INFORMATION ABOUT USERS---")

    # Data validation about washington file.
    if loc == "washington":
        print("* There is not information about Gender or Birth Year for this city.")

    
    #Information about users    
    else:
        user_type        = dataframe["User Type"].value_counts()
        gender_count     = dataframe["Gender"].value_counts()
        birth_year_min   = dataframe["Birth Year"].min()
        birth_year_max   = dataframe["Birth Year"].max()
        print("* Here is the summary about user types:\n")
        print(user_type)
        print("\n")
        print("* Here is the summary about user gender:\n")
        print(gender_count)
        print("\n* The youngest person using this service born in:", birth_year_max)
        print("* The oldest person using this service born in:", birth_year_min)
        
  

if __name__ == "__main__":    
    loc     = get_city()
    filters = get_filter()
    data    = load_data(loc, filters[0],filters[1])
    info    = get_data(data, loc, filters[0], filters[1])


    # Confirmation loop
    while True:
        confirmation = input("Would you like to see information about another city? Press yes/no\n")
        if confirmation.lower().strip() == "yes" or confirmation.lower().strip() == "y":
            print("* Ok! Let\'s do it again\n")
            loc     = get_city()
            filters = get_filter()
            data    = load_data(loc, filters[0],filters[1])
            info    = get_data(data, loc, filters[0], filters[1])

        elif confirmation.lower().strip() == "no" or confirmation.lower().strip() == "n":
            print("* Ok! see you later!")
            break

        else:
            print("***Sorry, i don\'t understand that command, can you repeat it again?")

