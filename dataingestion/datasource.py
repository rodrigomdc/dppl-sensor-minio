# -----------------------------------------------------------
# Manipulate data collected from an application hosted on ThingSpeak IoT platform
#
# (C) 2023 Rodrigo Costa, Ananindeua, Brasil
# 
# email eng.rodrigomdc@gmail.com
# -----------------------------------------------------------

from urllib.request import urlopen
import json

class DataSensor:

    def __init__(self, type_sensor): 
        #Type of sensor present of the application hosted on ThingSpeak platform       
        self._type_sensor = type_sensor

    def _collectTSData(self, src_url):

        """
        This function collects data in JSON format

        Parameters:
        -----------
            src_url is the URL (Uniform Resource Locators) of application hosted on ThingSpeak platform
            
        Return:
        -------
            JSON object containing data extracted from the ThingSpeak platform
        """

        with urlopen(src_url) as response:
            json_resp = json.loads(response.read())
        return json_resp   
        
    def saveToFile(self, src_url, path_tosave):

        """
        This function saves the collected data to a file in JSON format

        Parameters:
        ----------
             src_url is the URL (Uniform Resource Locators) of ThingSpeak public channel
             path_tosave is the path to save JSON file       
        """

        data_sensor = self._collectTSData(src_url)
        tmsp_info = data_sensor["feeds"][-1]["created_at"]
        file_name = path_tosave + f"{self._type_sensor}-sensor-{tmsp_info}.json"
        #For convenience, create a file with the most recent data collected on the platform 
        with open(file_name, 'w') as outfile:
            json.dump(data_sensor["feeds"][-1], outfile)
