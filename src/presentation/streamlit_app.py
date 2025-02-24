# src/presentation/streamlit_app.py
import streamlit as st
from charging.application.services.search_service import SearchService
import folium
from streamlit_folium import st_folium
import pandas as pd
from charging.application.services.suggestions_service import SuggestionService
from charging.application.services.malfunction_report_service import MalfunctionService


def render_search_page(df_lstat):
    """Render the Search by Postal Code page."""
    search_service = SearchService(df_lstat)  # Initialize SearchService with data
    st.title('Search for Postal Charging Location 🔍⚡')
    postal_code = st.text_input("Enter your postal code :", "")
    if postal_code:
        st.write(f"Searching for postal code: {postal_code}")
        stations = search_service.search_by_postal_code(postal_code)
        st.write(f"those are the stations in postal code :{postal_code}")
        st.write(pd.DataFrame(stations))
        print("station are as follow" )
        print(stations)
        # st.write("Debug - Stations Data:", stations)   # Debug output
        if stations:
            m = folium.Map(location=[52.5200, 13.4050], zoom_start=12)
            for station in stations:
                folium.Marker(
                    location=station["location"],
              #      popup=f"{station['name']} ({station['status']})",
                    popup=f"{station['name']} Is ready for you)",
                    # icon=folium.Icon(color="green" if station["status"] == "available" else "red"),
                ).add_to(m)
            st_folium(m, width=700, height=500)
        else:
            st.warning("No charging stations found for this postal code.")
def render_submit_suggestion_page(df_suggestions):
    st.title("Submit Suggestion for New Charging Location 📝⚡📍")
    with st.form("suggestion_form"):
        postal_code = st.text_input("Postal Code")
        address = st.text_input("Address")
        comments = st.text_area("Comments")
        submitted = st.form_submit_button("Submit")
        if submitted:
            suggestion_service = SuggestionService(df_suggestions)
            df_suggestions = suggestion_service.add_suggestion(postal_code, address, comments)
            st.success("Your suggestion has been submitted!")


def render_malfunction_report_page(df_lstat, df_reports):
    """
    Renders the malfunction report submission page in Streamlit.
    """
    st.title("Report Malfunction at Charging Station 🚨⚡📢")
    malfunction_service = MalfunctionService(df_reports)

    with st.form("malfunction_report"):
        station_name = st.selectbox("Select Charging Station", df_lstat["Anzeigename (Karte)"].unique())
        report_description = st.text_area("Describe the Malfunction")
        report_location = st.text_input("Address")
        submitted = st.form_submit_button("Submit")

        if submitted:
            # Add the malfunction report using the service
            malfunction_service.add_malfunction_report(station_name, report_description, report_location)
            st.success("Your report has been submitted!")



def render_view_suggestions_page(df_suggestions):
    st.title("View Suggestions for New Charging Locations 👀💡⚡📍")
    st.dataframe(df_suggestions)

def render_view_malfunction_reports_page(df_reports):
    st.title("View Malfunction Reports 👀⚠️📄")
    st.dataframe(df_reports)