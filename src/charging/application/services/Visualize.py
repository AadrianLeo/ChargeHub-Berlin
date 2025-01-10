from shared.application import HelperTools     as ht
from charging.application.services import Search

import folium
# from folium.plugins import HeatMap
import streamlit as st
from streamlit_folium import folium_static
from branca.colormap import LinearColormap


# -----------------------------------------------------------------------------
@ht.timer
def make_streamlit_electric_Charging_resid(dfr1, dfr2):
    """Makes Streamlit App with Heatmap of Electric Charging Stations and Residents"""
    
    dframe1 = dfr1.copy()
    dframe2 = dfr2.copy()


    # Streamlit app
    st.title('Heatmaps: Electric Charging Stations and Residents')

    Search.charging_station_search_by_postal_code(dframe1, dframe2)
    # Create a radio button for layer selection
    # layer_selection = st.radio("Select Layer", ("Number of Residents per PLZ (Postal code)", "Number of Charging Stations per PLZ (Postal code)"))

    layer_selection = st.radio("Select Layer", ("Residents", "Charging_Stations"))

    # Create a Folium map
    m = folium.Map(location=[52.52, 13.40], zoom_start=10)

    if layer_selection == "Residents":
        
        # Create a color map for Residents
        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe2['Einwohner'].min(), vmax=dframe2['Einwohner'].max())

        # Add polygons to the map for Residents
        for idx, row in dframe2.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Einwohner']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Einwohner: {row['Einwohner']}"
            ).add_to(m)
        
        # Display the dataframe for Residents
        # st.subheader('Residents Data')
        # st.dataframe(gdf_residents2)

    else:
        # Create a color map for Numbers

        color_map = LinearColormap(colors=['yellow', 'red'], vmin=dframe1['Number'].min(), vmax=dframe1['Number'].max())

    # Add polygons to the map for Numbers
        for idx, row in dframe1.iterrows():
            folium.GeoJson(
                row['geometry'],
                style_function=lambda x, color=color_map(row['Number']): {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 1,
                    'fillOpacity': 0.7
                },
                tooltip=f"PLZ: {row['PLZ']}, Number: {row['Number']}"
            ).add_to(m)

        # Display the dataframe for Numbers
        # st.subheader('Numbers Data')
        # st.dataframe(gdf_lstat3)

    # Add color map to the map
    color_map.add_to(m)
    
    folium_static(m, width=800, height=600)
