#Downloads

# pip install folium
# pip install geopandas 
# pip install pandas
# pip install geopy
#pip install Flask  

#Imports
import folium
import folium.plugins
import geopandas as gpds
import pandas as pds
import pyperclip
import json

#Pegando a localização
end = input("Endereço: ") # R. Manoel Santos Chieira, 92
coord = gpds.tools.geocode(end, provider = "nominatim", user_agent = "myGeocode")["geometry"]  # só funciona na janela interativa
string = str(coord[0])
separacao = string.split()
separacao.remove(separacao[0])
lat = (separacao[1].replace(')',''))
lon = (separacao[0].replace('(',''))

#Configurações do mapa
m = folium.Map(location=(-22.2127829,-49.9557924), zoom_start = 12, control_scale = False, )
folium.plugins.Geocoder().add_to(m)
folium.plugins.Fullscreen(position="topright", title="Expand me", title_cancel="Exit me", force_separate_button=True, ).add_to(m)

# Marcador
folium.Marker(location = [lat, lon]).add_to(m)
folium.ClickForLatLng(format_str='"[" + lat + "," + lng + "]"', alert=True).add_to(m)
loc_inv = pyperclip.paste()
print(loc_inv)

# Rodando
m
