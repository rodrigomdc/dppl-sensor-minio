
from datasource import DataSensor
from bucketmanipuling import DataBucket
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os
import sched
import time


#Schedule tasks to collect and send data to the bucket within a specified period of time
def repeatTask():
    specific_time = time.time() + acquisition_time  
    scheduler.enterabs(specific_time, 1, main, ())
    scheduler.enterabs(specific_time, 1, repeatTask, ())

#Delete the last JSON file uploaded to the bucket, thus keeping the most current one
def clearSrcDir():
    rd_file = tmp_dir + os.listdir(tmp_dir)[0]  
    if os.path.exists(rd_file):
        os.remove(rd_file)
    else:
        print("File not found.")  

def main():   
    
    #Delete the last JSON file present in the directory after uploading it to the bucket, thus keeping the most current one
    src_data = DataSensor(src_url)
    src_data.saveToFile(tmp_dir)    
    
    #Upload JSON file to bucket in Minio
    bucket = DataBucket(server_addr, api_port)
    bucket.sendToBucket(tmp_dir, bucket_name, output_info)
 
    clearSrcDir()

if __name__ == "__main__":

    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)       
    parser.add_argument("srv_addr", default="127.0.0.1", help="Minio server IP Address")
    parser.add_argument("api_port", default="9000", help="Application port to Minio service")
    parser.add_argument("url", help="Url to ThingSpeak data source")
    parser.add_argument("raw_dir", help="Temporary directory to save the JSON file with collected data")
    parser.add_argument("bucket", help="Bucket to store JSON file in Minio server")
    parser.add_argument("schedule_time", default=60, type=int, help="Schedule the task to run the script at a specific time (seconds)")        
    parser.add_argument("-o","--output", action="store_true", help="Shows whether the file was sent to the bucket successfully")
    args = vars(parser.parse_args())

    server_addr = args["srv_addr"]
    api_port = args["api_port"]
    src_url = args["url"]
    tmp_dir = args["raw_dir"]        
    bucket_name = args["bucket"]
    acquisition_time = args["schedule_time"]
    output_info = args["output"]

    #Repeat execution every x seconds
    scheduler = sched.scheduler(time.time, time.sleep)
    repeatTask()
    scheduler.run()
   