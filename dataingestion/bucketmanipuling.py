# -----------------------------------------------------------
# Data ingestion to Minio bucket
#
# (C) 2023 Rodrigo Costa, Ananindeua, Brasil
# 
# email eng.rodrigomdc@gmail.com
# -----------------------------------------------------------

from minio import Minio
import credentials
import os 
import sys

class DataBucket:

    def __init__(self, server_addr, server_port): 
        #IP address of the Minio Server       
        self._server_addr = server_addr
        #API port of the Minio Service
        self._server_port = server_port

    def _createConnection(self):

        """
        This function initializes a new client object to access MinIO service
       
        Returns
        -------
            Minio object        
        """

        client = Minio(            
            #endpoint: Hostname of the Minio server
            #access_key: Access key created by Minio Service.
            #secret_key: Secret Key created by Minio Service.
            endpoint = f"{self._server_addr}:{self._server_port}",
            access_key = credentials.access_key,
            secret_key = credentials.secret_key,
            secure = False 
        )
        return client 
 
    def sendToBucket(self, source_dir, bucket_name, status):    

        """
        This function is responsible for sending json file to specific bucket in Minio server

        Parameters
        ----------
            source_dir is the path to the local temporary directory that stores the JSON file
            bucket_name is the destination bucket that storage the json files
            status enables tracking of file sending to the destination bucket
        """

        obj_name = os.listdir(source_dir)[0]
        file_name = source_dir + os.listdir(source_dir)[0]
        cli_bucket = self._createConnection()
        if not os.listdir(source_dir):
           print(f"No file to send in directory: {source_dir}!")   
        if not cli_bucket.bucket_exists(bucket_name):
            print(f"Bucket <{bucket_name}> not exist")
        try:            
            cli_bucket.fput_object(
                bucket_name, 
                obj_name,  
                file_name, 
                content_type = "application/json"
            )
            if status:   
                print("File is successfully uploaded!")
                print(f"Object: '{obj_name}'")
                print(f"Bucket: '{bucket_name}/'")
                print("\n")
        except Exception as e:
            print("Error: ", e)
            sys.exit(0)
