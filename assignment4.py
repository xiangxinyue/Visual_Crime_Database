import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
import matplotlib
import folium

def task_1(connection):
        
    pass

def task_2(connection):
    pass

def task_3(connection):
    connection=sqlite3.connect("a4.db")
    #enter 4 inputs
    start_year = input("Enter start year (YYYY): ")
    end_year = input("Enter end year (YYYY): ")
    type_crime = input("Enter crime type: ")
    num_neighbor = input("Enter number of neighborhoods: ")
    
    #write the query for Q3
    df = pd.read_sql_query("SELECT C1.Neighbourhood_Name, sum(C1.Incidents_Count) as count, C2.Latitude, C2.Longitude FROM crime_incidents C1, coordinates C2 WHERE C1.Neighbourhood_Name = C2.Neighbourhood_Name AND Year >= %d AND Year <= %d AND Crime_Type = %s ORDER BY sum(Incidents_Count) as count limit %d",start_year,end_year,type_crime,num_neighbor,connection)
    
#SELECT C1.Neighbourhood_Name, sum(C1.Incidents_Count) as count, C2.Latitude, C2.Longitude
#FROM crime_incidents C1, coordinates C2
#WHERE C1.Neighbourhood_Name = C2.Neighbourhood_Name AND C1.Year >= 2011
#AND C1.Year <= 2013 AND C1.Crime_Type = "Assault"
#ORDER BY sum(C1.Incidents_Count) LIMIT 3

    #instantiating a map
    # location = latitude and longitude of thecurrent location
    # zoom_start = zoom level
    m = folium.Map(location=[53.5444,-113.323], zoom_start=11)

    #Creating bubble marker on the map -
    # Useful for comparison of an attribute (population, crime rate etc.) in different locations
    #Each bubble has a size related to a specific value.
    for i in range(len(df)):
        folium.Circle(
                      location=[df.iloc[i]['Latitude'],df.iloc[i]['Longitude']],
                      # location
                      popup= df.iloc[i]['Neighbourhood_Name'] + str(df.iloc[i]['count'])
                      # popup text
                      radius= df.iloc[i]['count'], # size of radius in meter
                      color= 'crimson’,
                      fill= True,
                      # whether to fill the map
                      fill_color= 'crimson’
                      # color to fill with
                      ).add_to(m)

    # creating the marker with a popup and add it to map
    #folium.Marker([53.52199, -113.49099], popup=“Strathcona”).add_to(m)
    
    # saving the marker
    m.save(“Q3.html”)

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

