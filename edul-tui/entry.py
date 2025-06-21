# ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
# │███████╗██████╗ ██╗   ██╗██╗     ██╗███╗   ██╗██╗  ██╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ████████╗██╗   ██╗██╗│
# │██╔════╝██╔══██╗██║   ██║██║     ██║████╗  ██║██║ ██╔╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ╚══██╔══╝██║   ██║██║│
# │█████╗  ██║  ██║██║   ██║██║     ██║██╔██╗ ██║█████╔╝        ██║   █████╗  ██████╔╝██╔████╔██║██║██╔██╗ ██║███████║██║            ██║   ██║   ██║██║│
# │██╔══╝  ██║  ██║██║   ██║██║     ██║██║╚██╗██║██╔═██╗        ██║   ██╔══╝  ██╔══██╗██║╚██╔╝██║██║██║╚██╗██║██╔══██║██║            ██║   ██║   ██║██║│
# │███████╗██████╔╝╚██████╔╝███████╗██║██║ ╚████║██║  ██╗       ██║   ███████╗██║  ██║██║ ╚═╝ ██║██║██║ ╚████║██║  ██║███████╗       ██║   ╚██████╔╝██║│
# │╚══════╝╚═════╝  ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝       ╚═╝   ╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝       ╚═╝    ╚═════╝ ╚═╝│
# └────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

# +=================+
# |Created by Sodium|
# +=================+
#
# Edul is not and has never been created, affiliated or endorsed by Overnet Data
# This software is provided as is without warranty of any kind
#

import sys
import json
import os

# handler is imported here, and it no longer tries to import from entry.py
from handler import timetable, auth, intro, help, homework, homeworkold, homeworkinfo

selected_login_id = 1 # Using None as a default, means no specific ID is selected

if len(sys.argv) > 1:

    # Revised logic to handle optional login ID for timetable/homework
    if sys.argv[1] == '--timetable' or sys.argv[1] == '-t':
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            selected_login_id = sys.argv[2]
        auth(login_id=selected_login_id) # Pass the selected_login_id
        timetable()

    elif sys.argv[1] == '--homework' or sys.argv[1] == '-h':
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            selected_login_id = sys.argv[2]

        auth(login_id=selected_login_id) # Pass the selected_login_id

        if len(sys.argv) > 2 and sys.argv[2] == 'old':
            homeworkold()
        elif len(sys.argv) > 2 and sys.argv[2] == 'info':
            if len(sys.argv) > 3:
                homeworkid = sys.argv[3]
                homeworkinfo(homeworkid)
            else:
                print("You need to supply a homework ID. Use: edul -h info <homework_id> . You can find a homework ID at the bottom of a homework block.")
        else:
            homework()

    elif sys.argv[1] == '--login' or sys.argv[1] == '-l':

        print("Which saved login ID would you like this to be? eg. 1, 2, 3, 4, 5")
        loginid = input("Login ID:") # This 'loginid' is local to this block.

        print("")

        print("Please input your login details:")
        username = input("Username:")
        password = input("Password:")
        schoolid = input("SchoolID:")

        data = {
            'username': username,
            'password': password,
            'schoolid': schoolid,
        }

        # Expand the user's home directory path
        json_file_path = os.path.expanduser(f'~/edul/data/data{loginid}.json') # Use the local 'loginid' here

        # Extract the directory path from the full file path
        directory = os.path.dirname(json_file_path)

        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")
            sys.exit(1)

        try:
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"Login details saved successfully to {json_file_path}")
        except IOError as e:
            print(f"Error writing login details to file {json_file_path}: {e}")
            sys.exit(1)

    elif sys.argv[1] == '--help': # Use elif for mutual exclusion
        help()

    else: # Added a general catch for unknown commands
        print("Unknown command. Please do edul --help to see the list of commands.")

else:
    intro()