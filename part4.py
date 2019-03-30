import pandas as pd
import numpy as np
import sqlite3
import folium

connection=sqlite3.connect("a4.db")
x = True
#now user have to give a range of year
while x:
    start_year = int(input("Enter start year (YYYY): "))
    end_year = int(input("Enter end year (YYYY): "))
    if start_year < end_year:
        x = False

#start_year = 2014
#end_year = 2016

#give an integer N
N = int(input("Enter an integer:"))
 
df1 = pd.read_sql_query(
    '''
    SELECT c1.Neighbourhood_Name, c1.Latitude, c1.Longitude, c2.crime_type, (c2.crime_count/p.people) as ratio
    
    FROM (SELECT Neighbourhood_Name, (CANADIAN_CITIZEN + NON_CANADIAN_CITIZEN + NO_RESPONSE) as people from population) as p,
    coordinates c1, 
    (select Neighbourhood_Name, Crime_Type as crime_type, sum(Incidents_Count) as crime_count from crime_incidents where year between %d and %d group by Neighbourhood_Name) as c2
    
    WHERE c1.Neighbourhood_Name = c2.Neighbourhood_Name 
    AND c2.Neighbourhood_Name = p.Neighbourhood_Name
    
    ORDER BY ratio DESC
    LIMIT %d;'''
    % (start_year, end_year, N), connection)

print(df1['crime_type'])

m = folium.Map(location=[53.5444,-113.323], zoom_start=11)
#print(df1.iloc[1])

for i in range(len(df1)):
    folium.Circle(
        location = [df1.iloc[i]['Latitude'],df1.iloc[i]['Longitude']],
        popup = df1.iloc[i]['Neighbourhood_Name']+ ' ' + str(df1.iloc[i]['ratio']),
        radius = df1.iloc[i]['ratio'] * 0.1,
        color = 'crimson',
        fill = True,
        fill_color = 'crimson',
        ).add_to(m)
m.save('Q4.html')
