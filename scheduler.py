import subprocess
import os
import xml.etree.ElementTree as ET
import getpass
import win32api
import win32security
from datetime import datetime

# Get the current UserID
user_id = getpass.getuser()

# Get the current SID
user_sid = win32security.GetTokenInformation(
    win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_READ),
    win32security.TokenUser
)[0]
user_sid_string = win32security.ConvertSidToStringSid(user_sid) # Convert the SID to string format

# Get the working directory
work_dir = os.getcwd()

# Get the script directory
file_direc = work_dir + '\\main.py'

# Let user type in scheduled time
user_time = input("Enter time to start in 24 hour format (HH:MM:SS): ")
current_date = datetime.now().date().strftime("%Y-%m-%d")
timestamp = current_date + "T" + user_time

# Parsing and modify the XML file
ET.register_namespace('', 'http://schemas.microsoft.com/windows/2004/02/mit/task')
mytree = ET.parse('CrawlerProc.xml')
myroot = mytree.getroot()

# Modify USER ID
Author_tag = myroot.find(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}Author")
Author_tag.text =  user_id 

# Modify USER SID
SID_tag = myroot.find(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}UserId")
SID_tag.text = user_sid_string

#Modify working directory 
WorkDir_tag = myroot.find(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}WorkingDirectory")
WorkDir_tag.text = work_dir

#Modify script directory 
Command_tag = myroot.find(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}Command")
Command_tag.text = file_direc

#Modify StartBoundary
StartBound = myroot.find(".//{http://schemas.microsoft.com/windows/2004/02/mit/task}StartBoundary")
StartBound.text = timestamp

# Write back the modified XML
mytree.write('CrawlerProc.xml')


# Define the schtasks command arguments to query the task
query_command = [
    'schtasks', '/Query',
    '/TN', 'Crawler\\CrawlerTask'
]
# Run the schtasks command to query the task
result = subprocess.run(query_command, capture_output=True)

if result.returncode == 0:
    # Task exists, delete it
    delete_command = [
        'schtasks', '/Delete',
        '/TN', 'Crawler\\CrawlerTask',
        '/F'  # Force delete without confirmation
    ]
    subprocess.run(delete_command, check=True)

# Create task
create_command = [
    'schtasks', '/Create',
    '/TN', 'Crawler\\CrawlerTask',
    '/XML', os.getcwd() + '\\CrawlerProc.xml'
]
subprocess.run(create_command, check=True)

