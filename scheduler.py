import subprocess
import os

file = os.getcwd() + '\main.py'

# Define the schtasks command arguments
command_crawler = [
    'schtasks', '/Create', 
    '/TN', 'Crawler\\CrawlerTask', 
    '/XML', os.getcwd() + '\\CrawlerProc.xml'
    # '/TR', file,
    # '/SC', 'DAILY', 
    # '/ST', '15:48'
    
]
# Run the schtasks command
subprocess.run(command_crawler, check=True)

print('Task created successfully.')



# import win32com.client as client
# import os
# import win32api
# import win32security
# import getpass

# TASK_CREATE_OR_UPDATE = 6
# TASK_LOGON_NONE = 0
# TASK_FOLDER = '\Crawler'
# TASK_NAME = 'Task'

# # create a Task Scheduler object
# scheduler = client.gencache.EnsureDispatch('Schedule.Service')

# # connect to the local computer's Task Scheduler service
# scheduler.Connect()
# print(type(scheduler))

# # create a new task object
# task_def = scheduler.NewTask(0)
# print(type(task_def))

# # set the task's name and description
# task_def.RegistrationInfo.Description = 'My scheduled task'
# user_id = getpass.getuser() # Get the current UserID
# task_def.RegistrationInfo.Author = user_id
# task_def.RegistrationInfo.URI = TASK_FOLDER + '\\'+ TASK_NAME
# task_def.Settings.Enabled = True

# # create a trigger for the task (run once, 5 minutes from now)
# trigger = task_def.Triggers.Create(2) #2 = CalendarTrigger
# trigger.StartBoundary = '2023-05-12T13:10:00' # change this to the desired start time
# trigger.Id = 'MyTrigger'
# trigger.Enabled = True
# print(type(trigger))

# #Set task principals
# principal = task_def.Principal
# # Get the current user's SID
# user_sid = win32security.GetTokenInformation(
#     win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32security.TOKEN_READ),
#     win32security.TokenUser
# )[0]
# # Convert the SID to string format
# user_sid_string = win32security.ConvertSidToStringSid(user_sid)
# principal.UserId = user_sid_string

# # create an action for the task (run a Python script)
# action = (task_def.Actions).Create(0)
# action = client.CastTo(action,"IExecAction")
# action.Path = os.getcwd() + "\main.py"
# action.WorkingDirectory = os.getcwd()
# action.Arguments = "-NoExit"
# print(type(action))

# print(action.Path)
# print(action.WorkingDirectory)
# print(action.Arguments)

# print(task_def.XmlText)

# try:
#     #Register the task with task scheduler
#     folder = scheduler.GetFolder('\\').CreateFolder(TASK_FOLDER)
#     print(folder)
#     a = folder.RegisterTask(
#         TASK_NAME,  # name of the task
#         task_def.XmlText,  # task object
#         TASK_CREATE_OR_UPDATE,  # create/update the task (6)
#         None,  # user account to run the task
#         None,  # password for the user account
#         3
#     )

#     print('Task registered successfully.')
# except Exception as e:
#     print(f'Error registering task: {str(e)}')


# import win32com.client

# scheduler = win32com.client.gencache.EnsureDispatch('Schedule.Service')

# def PrintAction(action):
#     ty = action.Type

#     if ty == win32com.client.constants.TASK_ACTION_COM_HANDLER: #=5
#         print("COM Handler Action")
#         coma = win32com.client.CastTo(action,"IComHandlerAction")
#         print(coma.ClassId,coma.Data)
#     elif ty == win32com.client.constants.TASK_ACTION_EXEC: #=0
#         print("Exec Action")
#         execa = win32com.client.CastTo(action,"IExecAction")
#         print(execa.Path,execa.Arguments)
#     elif ty == win32com.client.constants.TASK_ACTION_SEND_EMAIL: #=6 This might not work
#         print("Send Email Action") 
#         maila = win32com.client.CastTo(action,"IEmailAction")
#         print(maila.Subject,maila.To)
#     elif ty == win32com.client.constants.TASK_ACTION_SHOW_MESSAGE: #=7
#         print("Show Message Action")
#         showa = win32com.client.CastTo(action,"IShowMessageAction")
#         print(showa.Title,showa.MessageBody)
#     else:
#         print("Unknown Action Type!") #Don't expect this


# scheduler.Connect()
# folders = [scheduler.GetFolder('\\')]
# while folders:
#     folder = folders.pop(0)
#     folders += list(folder.GetFolders(0))
#     for task in folder.GetTasks(0):
#         print('Name       : %s' % task.Name)
#         print('Path       : %s' % task.Path)
#         print('Last Run   : %s' % task.LastRunTime)
#         print('Last Result: %s' % task.LastTaskResult)
#         defn = task.Definition
#         actions = defn.Actions
#         for action in actions:
#             PrintAction(action)
#             print()