import pandas as pd
import numpy as np
import sqlite3
import folium

connection=sqlite3.connect("a4.db")

#now user have to give a range of year
#start_year = int(input("Enter start year (YYYY): "))
#end_year = int(input("Enter end year (YYYY): "))

start_year = 2009
end_year = 2018



#give an integer N
N = int(input("Enter an integer:"))

#ratio = pd.read_sql_query('''select ''')

df = pd.read_sql_query(
    '''
    SELECT c1.Neighbourhood_Name, c1.Latitude, c1.Longitude
    
    FROM population p, coordinates c1, crime_incidents c2
    
    WHERE c2.year BETWEEN %d AND %d
    
    AND c1.Neighbourhood_Name = c2.Neighbourhood_Name 
    AND c2.Neighbourhood_Name = p.Neighbourhood_Name
    
    GROUP BY c2.Incidents_Count/(p.CANADIAN_CITIZEN + p.NON_CANADIAN_CITIZEN + p.NO_RESPONSE) 
    
    LIMIT %d;'''
    % (start_year, end_year, N), connection)

print(df)



