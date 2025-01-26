import pandas as pd

class MalfunctionService:
    def __init__(self, reports_df):
        """
        Initialize the MalfunctionService with an existing reports DataFrame.
        """
        self.reports_df = reports_df

    def add_malfunction_report(self, station_name, description, address):
        """
        Adds a new malfunction report for a charging station.
        """
        new_report = pd.DataFrame([{
            "station_name": station_name,
            "report_description": description,
            "address": address
        }])
        self.reports_df = pd.concat([self.reports_df, new_report], ignore_index=True)
        self.reports_df.to_csv("./charging/infrastructure/repositories/malfunction_reports.csv", sep=";", index=False)
        return self.reports_df
