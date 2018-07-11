import pandas as pd
import numpy as np
import random
import seaborn as sns
from matplotlib import pyplot as plt
import folium
import plotly.graph_objs as go
plt.style.use('seaborn')

adjincome = pd.read_csv('CleanedSchoolData.csv')
y = pd.DataFrame(adjincome.groupby(adjincome['city'])).mean()
print(y['income'])

#The following plots are some simple metrics to check the average income by school and relationship between race and ENI
fig, axes = plt.subplots(nrows=2,ncols=1)
sns.distplot(adjincome['income'], ax=axes[0],color='blue').set_title('Income Distribution')
axes[1] = plt.bar(y['city'],y['income'],color = 'blue')
plt.xticks(rotation = 90)
plt.title('Average Income for Students by City')
plt.show()

plt.subplot(2,2,1)
sns.regplot(adjincome['eni'],adjincome['white'],color = 'black')
plt.title('ENI for White Student pop')
plt.xticks(rotation = 90)

plt.subplot(2,2,2)
sns.regplot(adjincome['eni'],adjincome['asian'],color = "blue")
plt.title('ENI for Asian Student pop')
plt.xticks(rotation = 90)


plt.subplot(2,2,3)
sns.regplot(adjincome['eni'],adjincome['black'],color = 'purple')
plt.title('ENI for Black Student pop')
plt.xticks(rotation = 90)


plt.subplot(2,2,4)
sns.regplot(adjincome['eni'],adjincome['hispanic'],color = 'pink')
plt.title('ENI for Hispanic Student pop')
plt.xticks(rotation = 90)

plt.show()

#First map shows the income by school
map = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(adjincome)):
    popup = folium.Popup(adjincome.iloc[i]['name'],parse_html=True)
    folium.Circle(location=[adjincome.iloc[i]['latitude'],adjincome.iloc[i]['longitude']],popup = popup,
                  radius=adjincome.iloc[i]['income']/500, color = 'blue', fill = True, fill_color = 'blue').add_to(map)
map.save('IncomeMap.html')

#The following maps show the percentage of students by race
map1 = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(adjincome)):
    popup = folium.Popup(adjincome.iloc[i]['name'],parse_html=True)
    folium.Circle(location=[adjincome.iloc[i]['latitude'],adjincome.iloc[i]['longitude']],popup = popup,
                  radius=adjincome.iloc[i]['white'], color = 'white', fill = True, fill_color = 'white').add_to(map1)
map1.save('RaceMapWhite.html')

map2 = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(adjincome)):
    popup = folium.Popup(adjincome.iloc[i]['name'],parse_html=True)
    folium.Circle(location=[adjincome.iloc[i]['latitude'],adjincome.iloc[i]['longitude']],popup = popup,
                  radius=adjincome.iloc[i]['black'], color = 'red', fill = True, fill_color = 'red').add_to(map2)
map2.save('RaceMapBlack.html')

map3 = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(adjincome)):
    popup = folium.Popup(adjincome.iloc[i]['name'],parse_html=True)
    folium.Circle(location=[adjincome.iloc[i]['latitude'],adjincome.iloc[i]['longitude']],popup = popup,
                  radius=adjincome.iloc[i]['asian'], color = 'purple', fill = True, fill_color = 'purple').add_to(map3)
map3.save('RaceMapAsian.html')

map4 = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(adjincome)):
    popup = folium.Popup(adjincome.iloc[i]['name'],parse_html=True)
    folium.Circle(location=[adjincome.iloc[i]['latitude'],adjincome.iloc[i]['longitude']],popup = popup,
                  radius=adjincome.iloc[i]['hispanic'], color = 'pink', fill = True, fill_color = 'pink').add_to(map4)
map4.save('RaceMapHisp.html')

#Correlations between race and ENI
print("Correlation between White Student Population and ENI: " + str(adjincome['eni'].corr(adjincome['white'])))
print("Correlation between Asian Student Population and ENI: " + str(adjincome['eni'].corr(adjincome['asian'])))
print("Correlation between Black Student Population and ENI: " + str(adjincome['eni'].corr(adjincome['black'])))
print("Correlation between Hispanic Student Population and ENI: " + str(adjincome['eni'].corr(adjincome['hispanic'])))
print('')

cr = pd.read_csv('CleanedCrimeData.csv')

#Shows the distribution of different crimes, petit larceny is by far the most common, then by borough
plt.bar(cr['description'].value_counts().index,cr['description'].value_counts())
plt.title('Distribution of Crime')
plt.xlabel('Category of Crime')
plt.ylabel('Count')
plt.xticks(rotation = 90)
plt.show()
plt.bar(cr['boro'].value_counts().index,cr['boro'].value_counts())
plt.title('Crime Count by Borough')
plt.xlabel('Town')
plt.ylabel('Count')
plt.xticks(rotation = 90)
plt.show()

#time to combine the sets, make a loop for unique values in the schools column and calculate the distance between schools
#and crimes within a certain distance so we can see if theres a correlation between underperforming schools and crime
map = folium.Map(location=[40.7,-74.0], tiles="CartoDB dark_matter", zoom_start=12)
for i in range(len(cr.sample(2000))):
    popup = folium.Popup(cr.iloc[i]['type'],parse_html=True)
    folium.Circle(location=[cr.iloc[i]['lat'],cr.iloc[i]['long']],popup = popup,
                  radius=50, color = 'blue', fill = True, fill_color = 'blue').add_to(map)
map.save('CityCrime.html')


felony = pd.read_csv('CrimeDistances.csv')

df = pd.DataFrame({'crimes':felony['name'].value_counts()})
x = adjincome.set_index('name').join(df,lsuffix='name')
x = x.dropna(how='any')
x.to_csv('SchoolvCrime.csv')

nl = x['crimes'].nlargest(20)
inc = x.loc[nl.index,'income']

print(len(nl),len(inc))

#shows the schools with the most nearby crime
fig, (ax1,ax2) = plt.subplots(nrows=2,ncols=1,sharex=True)
ax1.bar(nl.index,nl)
ax1.set_ylabel('# of Crimes')
ax2.bar(nl.index,inc)
plt.xticks(rotation = 90)
plt.xlabel('School Name')
ax2.set_ylabel('Income')
plt.show()


