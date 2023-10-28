# -----------------------------------------------------------
# Manipulate data collected from an application hosted on ThingSpeak IoT platform
#
# (C) 2023 Rodrigo Costa, Ananindeua, Brasil
# 
# email eng.rodrigomdc@gmail.com
# -----------------------------------------------------------

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import sys
import json

class DataSensor:

    def __init__(self, src_url): 
        self._src_url = src_url

    def _collectTSData(self):

        """
        This function collects data in JSON format based on the URL (Uniform Resource Locators) of application hosted on ThingSpeak platform
        
        Return:
        -------
            JSON object containing data extracted from the ThingSpeak platform
        """
        json_resp = {}
        try:
            with urlopen(self._src_url) as response:
                json_resp = json.loads(response.read())
        except ValueError:
            print(f"Error: Invalid URL.")
            sys.exit(0)
        except HTTPError:
            print("Error: A HTTP Error occurred")
            sys.exit(0)
        except URLError:
            print("Error: URL not found")
            sys.exit(0)
        return json_resp   
        
    def saveToFile(self, path_tosave):

        """
        This function saves the collected data to a file in JSON format

        Parameters:
        ----------             
             path_tosave is the location to save JSON file       
        """

        data_sensor = self._collectTSData()
        tmsp_info = data_sensor["created_at"]
        file_name = path_tosave + f"data-sensor-{tmsp_info}.json"
        try:
            #For convenience, create a file with the most recent data collected on the platform 
            with open(file_name, 'w') as outfile:
                json.dump(data_sensor, outfile)
        except FileNotFoundError:
            print("The file "+ file_name + "does not exist.") 
