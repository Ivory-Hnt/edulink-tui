import sys

from handler import timetable, auth, intro, help, homework, homeworkold, homeworkinfo

if len(sys.argv) > 1:

    if sys.argv[1] == '--timetable' or sys.argv[1] == '-t':
        auth()
        timetable()

    if sys.argv[1] == '--homework' or sys.argv[1] == '-h':
        auth()
        # Check if there's a third argument AND if it's 'old'
        if len(sys.argv) > 2 and sys.argv[2] == 'old':
            homeworkold()  # Call homeworkold if 'old' is specified
        elif len(sys.argv) > 2 and sys.argv[2] == 'info':  # Changed from 'else' to 'elif' for correct logic flow
            if len(sys.argv) > 3:
                homeworkid = sys.argv[3]
                homeworkinfo(homeworkid)  # Pass the homeworkid to the function
            else:
                print(
                    "You need to supply a homework ID. Use: edul -h info <homework_id> . You can find a homework ID at the bottom of a homework block.")
        else:
            homework()  # Otherwise, call homework for current tasks

    if sys.argv[1] == '--login' or sys.argv[1] == '-l':
        print("Please input your new login details:")
        username = input("Username:")
        password = input("Password:")
        schoolid = input("SchoolID:")

        import json

        # Define the data as a Python dictionary
        data = {
            'username': username,
            'password': password,
            'schoolid': schoolid,
        }

        # Write data to a JSON file
        with open('/usr/local/bin/data/data.json', 'w') as f:
            json.dump(data, f)

    if sys.argv[1] == '--help':
        help()

else:
    intro()

