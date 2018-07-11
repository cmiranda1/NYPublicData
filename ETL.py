import pandas as pd
import numpy as np
import random
from matplotlib import pyplot as plt
from math import sin, cos, sqrt, atan2, radians
plt.style.use('seaborn')

#Load in the Data taken from Kaggle
schooldata  = pd.read_csv('2016 School Explorer.csv')

income = schooldata['School Income Estimate'].astype(str)
name = schooldata['School Name'].astype(str)
city = schooldata['City'].astype(str)
long = schooldata['Longitude'].astype(float)
lat = schooldata['Latitude'].astype(float)
addr = schooldata['Address (Full)'].astype(str)
white = schooldata['Percent White'].astype(str)
black = schooldata['Percent Black'].astype(str)
hispa = schooldata['Percent Hispanic'].astype(str)
asian = schooldata['Percent Asian'].astype(str)
atten = schooldata['Student Attendance Rate'].astype(str)
eni = schooldata['Economic Need Index'].astype(float)

#Clean out the characters and null values disrupting the data
adjincome = []
for i in range(len(income)):
    adjincome.append(income[i].strip('$'))
adjincome = pd.DataFrame({'income':adjincome, 'city':city, 'longitude':long, 'latitude':lat, 'white':white, 'black':black,
                          'hispanic':hispa, 'asian':asian, 'address':addr,'attendance':atten, 'name':name, 'eni':eni})
adjincome['income'] = adjincome['income'].str.strip()

adjincome['income'].replace(['nan'], np.nan, inplace = True)
adjincome['income'] = adjincome['income'].str.replace(',','').astype(float)
adjincome['white'] = adjincome['white'].str.strip('%').astype(float)
adjincome['black'] = adjincome['black'].str.strip('%').astype(float)
adjincome['hispanic'] = adjincome['hispanic'].str.strip('%').astype(float)
adjincome['asian'] = adjincome['asian'].str.strip('%').astype(float)
adjincome['attendance'] = adjincome['attendance'].str.strip('%').astype(float)
adjincome['address'] = adjincome['address'].str.strip()
adjincome['name'] = adjincome['name'].astype(str)
adjincome = adjincome.dropna(how='any')


#Make a csv to access in the analysis script
adjincome = adjincome.reset_index()
adjincome.to_csv('CleanedSchoolData.csv')

#Now time to repeat the process for the Crime Data
crime = pd.read_csv('NYPD_Complaint_Data_Current_YTD.csv')
lat = crime['Latitude'].astype(float)
long = crime['Longitude'].astype(float)
victim = crime['VIC_AGE_GROUP']
susrace = crime['SUSP_RACE'].astype(str)
sussex = crime['SUSP_SEX'].astype(str)
vicrace = crime['VIC_RACE'].astype(str)
vicsex = crime['VIC_SEX'].astype(str)
type = crime['LAW_CAT_CD'].astype(str)
desc = crime['OFNS_DESC'].astype(str)
prem = crime['PREM_TYP_DESC'].astype(str)
susage = crime['SUSP_AGE_GROUP'].astype(str)
boro = crime['BORO_NM'].astype(str)

df = pd.DataFrame({'lat':lat,'long':long,'victim age':victim,'suspect race':susrace,'suspect sex':sussex,
                   'victim race':vicrace,'victim sex':vicsex,'type':type,'description':desc,'place':prem,
                   'suspect age':susage,'boro':boro})
df['victim age'].replace(to_replace='nan',value='UNKNOWN',inplace=True)
df['victim race'].replace(to_replace='nan',value='UNKNOWN',inplace=True)
df['suspect sex'].replace(to_replace='nan',value='UNKNOWN',inplace=True)
df['suspect race'].replace(to_replace='nan',value='UNKNOWN',inplace=True)
df['suspect age'].replace(to_replace='nan',value='UNKNOWN',inplace=True)

# df = df[df.description != 'THEFT OF SERVICES']
# vc = df['description'].value_counts()
## print(vc)
list = ['victim age','suspect race', 'suspect sex', 'victim race', 'victim sex', 'type', 'description', 'suspect age']
# for i in range(len(vc)):
#     if vc[i].astype(float)<150:
#         df = df[df.description != vc.index[i]]

#Get rid of crime instances below a certain threshold
for x in range(len(list)):
    vc = df[list[x]].value_counts()
    for i in range(len(vc)):
        if vc[i].astype(float)<150:
            df = df[df[list[x]] != vc.index[i]]
for i in range(len(df.columns)):
    df[str(df.columns[i])].replace(['nan'], np.nan, inplace = True)
df = df.dropna(how='any')

#Save to an accessible file
df.to_csv('CleanedCrimeData.csv')


#Time to find crimes nearby to schools in the former dataframe. I only used a random sample from the crime file for
#this measurement since my comp didn't have the processing power to calculate for every registered crime
school = []
distances = []
type = []
for i in range(len(adjincome)):
    for x in range(500): #len(df.sample(1000))):
        j = random.randint(0,len(df)-1)
        #if df.iloc[x]['type'] == 'FELONY':
        print('Running...')
        R = 6373.0
        a = radians(df.iloc[j]['lat'])
        b = radians(df.iloc[j]['long'])
        c = radians(adjincome.iloc[i]['latitude'])
        d = radians(adjincome.iloc[i]['longitude'])
        lon = d - b
        lat = c - a
        x = sin(lat/2)**2 + cos(a)*cos(c)*sin(lon/2)**2
        y = 2*atan2(sqrt(x),sqrt(1-x))
        distance = R*y
        if distance < 1.0:
                distances.append(distance)
                school.append(adjincome.iloc[i]['name'])
                type.append(df.iloc[j]['type'])
                print('Added!')

#Save the last file
felony = pd.DataFrame({'name': school, 'distances':distances, 'type':type})
felony.to_csv('CrimeDistances.csv')



