# Imports
import pandas as pd
from datetime import date, timedelta
import folium
from folium import Marker
from folium.plugins import MarkerCluster
import math
import webbrowser



# Population Data
populationData = pd.read_csv('https://raw.githubusercontent.com/jasperdebie/VisInfo/master/us-state-capitals.csv')

# Get the most recent date for filtering
freshDate = date.today() - timedelta(days=1)
freshDate = date.strftime(freshDate,"%Y%m%d")
freshDate = freshDate[0:4] + "-" + freshDate[4:6] + "-" + freshDate[6:8]

# Vaccination data, for most recent date
vaccinationData = pd.read_csv('https://raw.githubusercontent.com/owid/covid-19-data/master/public/data/vaccinations/us_state_vaccinations.csv')
vaccinationByLocation = vaccinationData.loc[(vaccinationData.date == '2022-11-09')][["location", "people_vaccinated",'total_vaccinations']]

# Vaccination and population data
vaccinationAndPopulationByLocation = pd.merge(populationData, vaccinationByLocation, left_on='name',right_on='location').drop(columns="location")

# Calculate percentage vaccinated by state
vaccinationAndPopulationByLocation["percent_vaccinated"] = vaccinationAndPopulationByLocation["people_vaccinated"] / vaccinationAndPopulationByLocation["total_vaccinations"]

# vaccinationAndPopulationByLocation

print("Date ran:", date.today())

# Calculate the total percent vaccinated in the US

percentageTotal = vaccinationAndPopulationByLocation["people_vaccinated"].sum() / vaccinationAndPopulationByLocation["total_vaccinations"].sum()
print('Percentage Vaccinated in the US: {}%'.format(round(percentageTotal*100, 2)))


# Create the map
v_map = folium.Map(location=[42.32,-71.0589], tiles='cartodbpositron', zoom_start=4)

# Add points to the map
mc = MarkerCluster()

for idx, row in vaccinationAndPopulationByLocation.iterrows():
    if not pd.isnull(row['longitude']) and not pd.isnull(row['latitude']):
        mc.add_child(Marker(location=[row['latitude'], row['longitude']],
                            tooltip=str(round(row['percent_vaccinated']*100, 2))+"%"))
v_map.add_child(mc)

# Display the map
v_map.save('map.html')
webbrowser.open('map.html')