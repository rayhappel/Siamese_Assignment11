# File Name : Processor.py
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

import csv

class DataLoader:
    """
    Loads data from a CSV file into a list of dictionaries.
    """
    def __init__(self, filepath):
        """
        Constructor to initialize the DataLoader class with a file path.
        @param filepath: The path to the CSV file to be loaded.
        """
        self.filepath = filepath

    def load_data(self):
        """
        Loads CSV data into a list of dictionaries (one per row).
        @return: A list of dictionaries representing each row in the CSV file.
        """
        with open(self.filepath, mode='r', newline='', encoding='utf-8') as file:
            return list(csv.DictReader(file))


class DataWriter:
    """
    Writes cleaned data and anomalies to separate CSV files.
    """
    def __init__(self, cleaned_path, anomaly_path):
        """
        Constructor to initialize the DataWriter class with output file paths.
        @param cleaned_path: Path to write the cleaned data CSV.
        @param anomaly_path: Path to write the anomaly data CSV.
        """
        self.cleaned_path = cleaned_path
        self.anomaly_path = anomaly_path

    def write(self, cleaned_data, anomaly_data):
        """
        Writes cleaned and anomaly data to their respective CSV output files.
        @param cleaned_data: A list of dictionaries containing the cleaned dataset.
        @param anomaly_data: A list of dictionaries containing the anomaly dataset.
        @return: None
        """
        print("Writing cleaned data CSV...") 
        if cleaned_data:
            with open(self.cleaned_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=cleaned_data[0].keys())
                writer.writeheader()
                writer.writerows(cleaned_data)

        print("Writing anomalies CSV...")
	    # Write anomaly data to new csv file
        if anomaly_data:
            with open(self.anomaly_path, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=anomaly_data[0].keys())
                writer.writeheader()
                writer.writerows(anomaly_data)






