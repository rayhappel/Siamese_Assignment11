# File Name : main.py
# Student Name: Ray Happel, Nate Hoang
# email:  happelrc@mail.uc.edu, hoangnd@mail.uc.edu
# Assignment Number: Assignment 11
# Due Date:   04/17/2025
# Course #/Section:   IS 4010-001
# Semester/Year:   Spring 2025
# Brief Description of the assignment:  In this assignment, we were tasked with cleaning up data the fuelPurchaseData csv file we were given. We are required to clean the data and have 2 output csv files that show our cleaned data.

# Brief Description of what this module does. This module performs data cleaning by implementing missing values, removing duplicates rows, and creating output files for cleaned data.
# Citations: ChatGPT, https://stackoverflow.com/questions/78275598/accessing-an-api-using-a-key-in-python, https://stackoverflow.com/questions/52315920/merging-and-removing-duplicates-in-two-csvs-without-using-pandas, https://www.geeksforgeeks.org/writing-csv-files-in-python/, https://stackoverflow.com/questions/71925745/clean-csv-file-with-python, 

# Anything else that's relevant: N/A

from DataProcessor.Processor import DataLoader, DataWriter
from DataCleaner.DataCleaner import (
    GrossPriceFormatter,
    DuplicateRemover,
    AnomalyDetector,
    ZipCodeFiller
)
import os

def main():
    api_key = "fe3d5680-1b0b-11f0-8493-f5422fd0c2a8"  # Our API key for zip code lookups

    loader = DataLoader("Data/fuelPurchaseData.csv") # Load data from the fuelPurchaseData CSV file
    data = loader.load_data()
    print(f"Loaded {len(data)} rows from fuelPurchaseData.csv")

    data = GrossPriceFormatter.format(data) # Reformat the gross price to 2 decimal places
    print("Gross prices formatted to 2 decimal places")

    data = DuplicateRemover.remove(data) # Remove duplicate rows
    print("Duplicate rows removed")

    data, anomalies = AnomalyDetector.separate_pepsi(data) # Ensure we have an output file once we delete the Pepsi fuel type purchases
    print(f" Removed {len(anomalies)} Pepsi rows")

    zip_filler = ZipCodeFiller(api_key) # Fill in the entries with missing zip codes 
    data = zip_filler.fill_missing_zips(data)

    writer = DataWriter("Data/cleanedData.csv", "Data/dataAnomalies.csv") # Output our cleaned data into a new csv file
    writer.write(cleaned_data=data, anomaly_data=anomalies)

    print("Output File Check:") # Confirm output files were successfully created
    for path in ["Data/cleanedData.csv", "Data/dataAnomalies.csv"]:
        if os.path.exists(path):
            print(f"File created: {path}")
        else:
            print(f"File not found: {path}")

if __name__ == "__main__":
    main()