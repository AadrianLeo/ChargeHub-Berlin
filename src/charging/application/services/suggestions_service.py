# src/charging/infrastructure/services/suggestion_service.py
import pandas as pd

class SuggestionService:
    def __init__(self, suggestions_df):
        self.suggestions_df = suggestions_df

    def add_suggestion(self, postal_code, address, comments):
        """
        Adds a new suggestion for a charging station location.
        """
        new_suggestion = pd.DataFrame([{"postal_code": postal_code, "address": address, "comments": comments}])
        self.suggestions_df = pd.concat([self.suggestions_df, new_suggestion], ignore_index=True)
        self.suggestions_df.to_csv("./charging/infrastructure/repositories/suggestions.csv", sep=";", index=False)
        return self.suggestions_df
