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

import Student
import re
import html
from Student import Student
import os
import json
from datetime import date, timedelta

me = Student()

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

# MODIFIED: auth now reads the active account from a config file.
def auth():
    active_account_path = os.path.expanduser('~/edul/data/active_account.txt')

    try:
        with open(active_account_path, 'r') as f:
            login_id = f.read().strip()
            if not login_id:
                raise FileNotFoundError # Treat empty file as not found
    except FileNotFoundError:
        print("Error: No active account is set.")
        print("Please set an active account using: edul -a <id>")
        exit()

    json_file_path = os.path.expanduser(f'~/edul/data/data{login_id}.json')

    try:
        with open(json_file_path, 'r') as f:
            data = json.load(f)
        username = data.get('username')
        password = data.get('password')
        schoolid = data.get('schoolid')
    except FileNotFoundError:
        print(f"Error: Login details for active account ID {login_id} not found.")
        print(f"Please run 'edul -l' to configure account {login_id}, or switch accounts with 'edul -a <id>'.")
        exit()
    except json.JSONDecodeError:
        print(f"Error: The login details file for account {login_id} is malformed.")
        print("Please run 'edul -l' to re-login and create a valid file.")
        exit()
    except Exception as e:
        print(f"An unknown error occurred while fetching login details: {e}")
        exit()

    try:
        print(f"Authenticating with account ID: {login_id}...")
        me.authenticate(username=username, password=password, school_postcode=schoolid)
        print("Authentication successful.")
    except Exception as e:
        print(f"\nAn error occurred during authentication for account {login_id}: {e}")
        exit()

def help() :
    print("\n" * 79)
    print("                 ------- Edulink Terminal Interface Help -------                 ")
    print("\n" * 2)
    print("               -l or --login        -  Set up a new login account profile.")
    print("               -a or --account <id> -  Set the active account to use for commands.")
    print("")
    print("               -t or --timetable [days] -  Show timetable. [days] is optional.")
    print("                                          (e.g., '-t' for today, '-t 1' for tomorrow)")
    print("")
    print("               -h or --homework [sub] -  Show homework. [sub] can be 'old' or 'info <id>'.")
    print("\n" * 2)
    print("            Please view the README.md file for more detailed usage.")
    print("\n" * 2)
    print("                 -----------------------------------------------                 ")
    print("\n" * 15)

# MODIFIED: Function now takes an integer for days in the future and provides clearer output.
def timetable(days_in_future=0):
    target_date = date.today() + timedelta(days=days_in_future)
    api_date_str = target_date.strftime("%Y-%m-%d")

    # Generate a more descriptive, user-friendly title for the timetable
    if days_in_future == 0:
        day_name = "Today"
    elif days_in_future == 1:
        day_name = "Tomorrow"
    else:
        day_name = target_date.strftime("%A")

    display_date_str = f"{day_name} ({target_date.strftime('%d %B %Y')})"
    header = f"--- Timetable for {display_date_str} ---"

    try:
        timetable_data = me.timetable(date=api_date_str)

        print("\n" * 104)
        print(header)
        print("-" * len(header))
        print("")

        if not timetable_data:
            print(f"    No lessons found for this day.")
        else:
            period = 0
            for lesson in timetable_data:
                teacher = lesson.get('teachers', 'N/A')
                room = lesson.get('room', {}).get('name', 'N/A')
                subject = lesson.get('teaching_group', {}).get('subject', 'N/A')
                group = lesson.get('teaching_group', {}).get('name', 'N/A')
                period += 1

                print(f"    Lesson: {subject}")
                print(f"    Period: {period}")
                print(f"    Teacher: {teacher}")
                print(f"    Room: {room}")
                print(f"    Class: {group}")
                print("-" * 30)
                print("")

    except Exception as e:
        # Gracefully handle the specific error when no timetable data is available
        if "No timetable data was found for the EXACT date" in str(e):
            print("\n" * 104)
            print(header)
            print("-" * len(header))
            print(f"\n    No timetable data is available for this day.")
        else:
            print(f"An unexpected error occurred while fetching the timetable: {e}")

    finally:
        print("\n" * 4)

def homework():
    try:
        homework_data = me.homework()
        current_homework = homework_data.get('current', [])

        print("\n" * 82)
        print("                 ------- Your Current Homework -------                 ")
        if not current_homework:
            print("\n                 No upcoming homework assignments found.")
        else:
            print("-" * 30)
            for hw in current_homework:
                activity = hw.get('activity', 'N/A')
                subject = hw.get('subject', 'N/A')
                due_date = hw.get('due_date', 'N/A')
                due_text = hw.get('due_text', 'N/A')
                set_by = hw.get('set_by', 'N/A')
                status = hw.get('status', 'N/A')
                hw_id = hw.get('id', 'N/A')

                print(f"\nActivity: {activity}")
                print(f"Subject: {subject}")
                print(f"Due Date: {due_date} ({due_text})")
                print(f"Set By: {set_by}")
                print(f"Status: {status}")
                print(f"ID: {hw_id}")
                print("-" * 30)
        print("\n" * 14)

    except Exception as e:
        print(f"An error occurred while fetching your homework: {e}")

def homeworkold():
    try:
        homework_data = me.homework()
        past_homework = homework_data.get('past', [])

        print("\n" * 80)
        print("                 ------- Your Past Homework -------                 ")
        if not past_homework:
            print("\n                 No past homework assignments found.")
        else:
            print("-" * 30)
            for hw in past_homework:
                activity = hw.get('activity', 'N/A')
                subject = hw.get('subject', 'N/A')
                due_date = hw.get('due_date', 'N/A')
                due_text = hw.get('due_text', 'N/A')
                set_by = hw.get('set_by', 'N/A')
                status = hw.get('status', 'N/A')

                print(f"\nActivity: {activity}")
                print(f"Subject: {subject}")
                print(f"Due Date: {due_date} ({due_text})")
                print(f"Set By: {set_by}")
                print(f"Status: {status}")
                print("-" * 30)
    except Exception as e:
        print(f"An error occurred while fetching your past homework: {e}")

def homeworkinfo(homework_id):
    try:
        homeworkinfo_data = me.homeworkInfo(homework_id=homework_id)
        activity_name = homeworkinfo_data.get('activity', 'unnamed assignment')

        print("\n" * 80)
        print(f"                 ------- Homework Details: {activity_name} -------                 ")
        if homeworkinfo_data:
            raw_description = homeworkinfo_data.get('description', 'No description available.')
            clean_description = ' '.join(re.sub(r'<[^>]+>', '', html.unescape(raw_description)).split()).strip()

            print("-" * 30)
            print(f"Activity: {activity_name}")
            print(f"Subject: {homeworkinfo_data.get('subject', 'N/A')}")
            print(f"Due Date: {homeworkinfo_data.get('due_date', 'N/A')} ({homeworkinfo_data.get('due_text', 'N/A')})")
            print(f"Set By: {homeworkinfo_data.get('set_by', 'N/A')}")
            print(f"Status: {homeworkinfo_data.get('status', 'N/A')}")
            print(f"Description: {clean_description}")
            print(f"Available From: {homeworkinfo_data.get('available_date', 'N/A')} ({homeworkinfo_data.get('available_text', 'N/A')})")

            attachments = homeworkinfo_data.get('attachments', [])
            if attachments:
                print("\n    Attachments:")
                for att in attachments:
                    print(f"      - {att.get('filename', 'N/A')} ({att.get('filesize', 'N/A')} bytes)")
            print("-" * 30)
        else:
            print(f"\n                 No detailed information found for homework ID: {homework_id}")
        print("\n" * 14)
    except Exception as e:
        print(f"An error occurred fetching details for homework ID {homework_id}: {e}")
