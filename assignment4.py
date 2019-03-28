'''
In this assignment, I will be using the Pandas, Matplotlib and Folium Python libraries 
to manipulate and visualize two datasets which contain population and crime incident information 
at different neighborhoods in Edmonton.  
'''
import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import folium


def task_1(connection):
    '''
    Given a range of years and crime type, 
    show (in a bar plot) the month-wise total count of the given crime type. 
    '''
    # require inputs
    s_year = input("Enter start year (YYYY): ")
    

    #input start year and check if the input is valid
    while (s_year.isdigit() == False):
        s_year = input("Enter start year (YYYY): ")
    if s_year.isdigit() == True :
        s_year_tuple = int(s_year)

    #input end year and check if the input is valid
    e_year = input("Enter end year (YYYY): ")
    while (e_year.isdigit() == False):
        e_year = input("Enter end year (YYYY): ")
    if e_year.isdigit()==True:
        e_year_tuple = int(e_year)
    
    #input crime type
    c_type = input("Enter crime type: ")
    c_type_tuple = "'"+c_type+"'"

    if s_year_tuple>e_year_tuple:           # if start year is greater than end year then return
        return print("Invalid start year and end year.")

    #inp_tuple = ("'"+c_type+"'",s_year,e_year,)
    #print(type(t_1))

    # sql query
    statement = "select Month, sum(Incidents_Count) as count from crime_incidents where Crime_Type = %s and Year between %d and %d group by Month;"
    df = pd.read_sql_query(statement%(c_type_tuple,s_year_tuple,e_year_tuple,) ,connection)
    
    #add empty month to the dataframe
    for i in range(12):
        m = i+1
        if m not in df['Month'].values:
            print(i,"Not in dataframe")
            df = df.append({'Month': m,'count':0},ignore_index=True)
    
    df = df.sort_values(by=['Month'])   #sort the dataframe according to the month

    #print(df)
    
    if df.empty:
        return print("No crime occcured in that range\n")
    else:
        #print(df)
        #print("\n")

        #print the output
        plot = df.plot.bar(x="Month")
        plt.plot()
        plt.show()
        return


def task_2(connection):
    pass

def task_3(connection):
    connection=sqlite3.connect("a4.db")
    #enter 4 inputs
    start_year = int(input("Enter start year (YYYY): "))
    end_year = int(input("Enter end year (YYYY): "))
    type_crime = str(input("Enter crime type: "))
    num_neighbor = int(input("Enter number of neighborhoods: "))
    
    #write the query for Q3
    df = pd.read_sql_query('''SELECT C1.Neighbourhood_Name, sum(C1.Incidents_Count) as count, C2.Latitude, C2.Longitude FROM crime_incidents C1, coordinates C2 WHERE C1.Neighbourhood_Name = C2.Neighbourhood_Name AND Year >= %d AND Year <= %d AND Crime_Type = %s GROUP BY C1.Neighbourhood_Name ORDER BY sum(C1.Incidents_Count) DESC limit %d;'''%(start_year,end_year,type_crime,num_neighbor),connection)
    
    print(df)
    array_data = np.array(df)#np.ndarray()
    list_data= array_data.tolist()#list
    print(list_data)
    #print(list_data[][2])
    #instantiating a map
    # location = latitude and longitude of thecurrent location
    # zoom_start = zoom level
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)

    #Creating bubble marker on the map -
    # Useful for comparison of an attribute (population, crime rate etc.) in different locations
    #Each bubble has a size related to a specific value.
    for i in range(len(list_data)):
        folium.Circle(
                      location=[list_data[i][2],list_data[i][3]],
                      # location
                      popup= ("%s <br> %s" % (list_data[i][0],list_data[i][1])),
                      # popup text
                      radius= list_data[i][1],
                      # size of radius in meter
                      color= 'crimson',
                      fill= True,
                      # whether to fill the map
                      fill_color= 'crimson'
                      # color to fill with
                      ).add_to(m)

    # creating the marker with a popup and add it to map
    # saving the marker
    m.save("Q3.html")

def task_4(connection):
    pass


def main():
    connection=sqlite3.connect("a4.db")  # change the database input here.
    while(1):
        print("1: Q1")
        print("2: Q2")
        print("3: Q3")
        print("4: Q4")
        print("E: Exit")
        print("Enter your choice: ")
        tasks=['E','1','2','3','4']
        inp = input()
        while inp in tasks:
            if inp == 'E':
                return
            elif inp == '1':
                task_1(connection)
                break
            elif inp == '2':
                task_2(connection)
                break
            elif inp == '3':
                task_3(connection)
                break
            elif inp == '4':
                task_4(connection)
                break
            else:
                inp=input("Please choose a valid task\n")

if __name__ == '__main__':
    main()

