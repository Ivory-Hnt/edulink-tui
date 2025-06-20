# Edulink Terminal CUI - Made by Sodium

import Student
import login
import re
import html
from Student import Student

me = Student()

import json

def error127() :
    print("Command not found. Please do edul --help to see the list of commands.")

def intro() :
    print("\n" * 84)
    print("                 ------- Edulink Terminal Interface -------                 ")
    print("\n" * 2)
    print("Edulink Terminal Interface (edul) is a way of accessing Edulink through a Linux")
    print("command line.")
    print("")
    print("Edul is not and has not ever been associated or endorsed with/by Overnet Data.")
    print("The author/s of edul is not responsible for anything and everything that you may")
    print("choose to do with the code. This includes but is not limited to illegal activities.")
    print("\n" * 4)
    print("             Do edul --help for a list of available commands.")
    print("\n" * 2)
    print("                 ------------------------------------------                 ")
    print("\n" * 15)


def auth() :

    # Define the path to your JSON file
    json_file_path = '/usr/local/bin/data/data.json'

    try:
        # Open the JSON file in read mode
        with open(json_file_path, 'r') as f:
            # Load the JSON data into a Python dictionary
            data = json.load(f)

        # Assign the values to variables
        username = data.get('username')
        password = data.get('password')
        schoolid = data.get('schoolid')

    except Exception as e:
        print(f"Could not fetch login details. Please run edul -l to login. Full error: {e}")
        exit()

    try:
        me.authenticate(username=username, password=password, school_postcode=schoolid)
    except Exception as e:
        print(f"An error occurred during authentication: {e}")
        exit()

def help() :
    print("\n" * 79)
    print("                 ------- Edulink Terminal Interface Help -------                 ")
    print("\n" * 2)
    print("               -t or --timetable  -  Shows your timetable for today.")
    print("")
    print("               -l or --login  -  Sets your login details for edulink.")
    print("\n" * 2)
    print("                 -----------------------------------------------                 ")
    print("\n" * 20)


# --- Timetable Output ---
def timetable() :
    try:
        timetable_data = me.timetable()

        print("\n" * 104)

        # --- Print the timetable in a readable format ---
        print("-" * 30) # Prints a separating line
        print("")

        period = 0



        for lesson in timetable_data:
            teacher = lesson.get('teachers', 'N/A')
            room = lesson.get('room', {}).get('name', 'N/A')
            subject = lesson.get('teaching_group', {}).get('subject', 'N/A')
            group = lesson.get('teaching_group', {}).get('name', 'N/A')
            period = period + 1

            print(f"    Lesson: {subject}")
            print(f"    Period: {period}")
            print(f"    Teacher: {teacher}")
            print(f"    Room: {room}")
            print(f"    Class: {group}")
            print("")
            print("-" * 30) # Separator for the next lesson
            print("")

        print("\n" * 4)

    except Exception as e:
        print(f"An error occurred while fetching the timetable: {e}")


# handler.py

# ... (rest of your imports and code) ...

def homework():
    try:
        homework_data = me.homework()  # Call the homework method to get the data

        print("\n" * 82)

        current_homework = homework_data.get('current', [])

        if not current_homework:
            print("                 No upcoming homework assignments found.")
            print("")
        else:

            print("-" * 30)  # Separator for the next homework

            for hw in current_homework:
                activity = hw.get('activity', 'N/A')
                subject = hw.get('subject', 'N/A')
                due_date = hw.get('due_date', 'N/A')
                set_by = hw.get('set_by', 'N/A')
                status = hw.get('status', 'N/A')
                due_text = hw.get('due_text', 'N/A')  # This often gives "today", "in X days", etc.
                id = hw.get('id', 'N/A') # Homework ID. Will probably be useful in a future update.


                print("")
                print(f"Activity: {activity}")
                print(f"Subject: {subject}")
                print(f"Due Date: {due_date} ({due_text})")
                print(f"Set By: {set_by}")
                print(f"Status: {status}")
                print(f"ID: {id}")

                # Optional: Display attachments if any
                attachments = hw.get('attachments', [])
                if attachments:
                    print("")
                    print("    Attachments:")
                    for att in attachments:
                        print(f"      - {att.get('filename', 'N/A')}")

                print("")
                print("-" * 30)  # Prints a separating line

        # Add more blank lines for spacing if desired
        print("\n" * 14)  # Prints 14 blank lines

    except Exception as e:
        print(f"An error occurred while fetching your homework: {e}")

# handler.py

# ... (rest of your imports and other functions like homework, auth, etc.) ...

def homeworkold():
    try:
        homework_data = me.homework()  # Call the homework method to get all data

        print("\n" * 80)
        print("                 ------- Your Past Homework -------                 ")
        print("")

        past_homework = homework_data.get('past', []) # Get only the 'past' homework

        if not past_homework:
            print("                 No past homework assignments found.")
            print("")
        else:
            print("-" * 30)  # Separator for the first homework item

            for hw in past_homework:
                activity = hw.get('activity', 'N/A')
                subject = hw.get('subject', 'N/A')
                due_date = hw.get('due_date', 'N/A')
                set_by = hw.get('set_by', 'N/A')
                status = hw.get('status', 'N/A')
                due_text = hw.get('due_text', 'N/A')  # This often gives "X days ago", etc.

                print("")
                print(f"Activity: {activity}")
                print(f"Subject: {subject}")
                print(f"Due Date: {due_date} ({due_text})")
                print(f"Set By: {set_by}")
                print(f"Status: {status}")

                # Optional: Display attachments if any
                attachments = hw.get('attachments', [])
                if attachments:
                    print("")
                    print("    Attachments:")
                    for att in attachments:
                        print(f"      - {att.get('filename', 'N/A')}")

                print("")
                print("-" * 30)  # Prints a separating line

        print("\n" * 14)  # Prints 14 blank lines

    except Exception as e:
        print(f"An error occurred while fetching your past homework: {e}")

def homeworkinfo(homework_id):
    try:
        homeworkinfo_data = me.homeworkInfo(homework_id=homework_id)

        print("\n" * 80)
        print(f"                 ------- Homework Details for {homeworkinfo_data.get('activity', 'unnamed assignment')} -------                 ")
        print("")

        if homeworkinfo_data:
            raw_description = homeworkinfo_data.get('description', 'No description available.')

            # --- Manual HTML Stripping and Entity Decoding ---
            # Removes HTML tags using regex as it originally came out a bit unclean and had some HTML and CSS elements.
            clean_description = re.sub(r'<[^>]+>', '', raw_description)
            clean_description = html.unescape(clean_description)
            clean_description = ' '.join(clean_description.split()).strip()

            print("\n" * 30)
            print(f"Activity: {homeworkinfo_data.get('activity', 'N/A')}")
            print(f"Subject: {homeworkinfo_data.get('subject', 'N/A')}")
            print(f"Due Date: {homeworkinfo_data.get('due_date', 'N/A')} ({homeworkinfo_data.get('due_text', 'N/A')})")
            print(f"Set By: {homeworkinfo_data.get('set_by', 'N/A')}")
            print(f"Status: {homeworkinfo_data.get('status', 'N/A')}")
            print(f"Description: {clean_description}") # Use the manually cleaned description here
            print(f"Available From: {homeworkinfo_data.get('available_date', 'N/A')} ({homeworkinfo_data.get('available_text', 'N/A')})")
            print(f"Duration: {homeworkinfo_data.get('duration', 'N/A')} minutes")
            print(f"Source: {homeworkinfo_data.get('source', 'N/A')}")

            attachments = homeworkinfo_data.get('attachments', [])
            if attachments:
                print("\n    Attachments:")
                for att in attachments:
                    print(f"      - Filename: {att.get('filename', 'N/A')}")
                    print(f"        Filesize: {att.get('filesize', 'N/A')} bytes")
                    print(f"        MIME Type: {att.get('mime_type', 'N/A')}")
            print("\n" * 30)
        else:
            print(f"                 No detailed information found for homework ID: {homework_id}")

        print("\n" * 14)

    except Exception as e:
            print(f"An error occurred while fetching homework info for ID {homework_id}: {e}") # The e shows the error in more depth
