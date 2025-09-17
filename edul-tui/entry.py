# ┌────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
# │███████╗██████╗ ██╗   ██╗██╗     ██╗███╗   ██╗██╗  ██╗    ████████╗███████╗██████╗ ███╗   ███╗██╗███╗   ██╗ █████╗ ██╗         ████████╗██╗   ██╗██╗│
# │██╔════╝██╔══██╗██║   ██║██║     ██║████╗  ██║██║ ██╔╝    ╚══██╔══╝██╔════╝██╔══██╗████╗ ████║██║████╗  ██║██╔══██╗██║         ╚══██╔══╝██║   ██║██║│
# │█████╗  ██║  ██║██║   ██║██║     ██║██╔██╗ ██║█████╔╝        ██║   █████╗  ██████╔╝██╔████▔██║██║██╔██╗ ██║███████║██║            ██║   ██║   ██║██║│
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

from handler import timetable, auth, intro, help, homework, homeworkold, homeworkinfo

if len(sys.argv) > 1:

    # --- Timetable Command ---
    # Usage: edul -t [days_in_future]
    # Example: 'edul -t' for today, 'edul -t 1' for tomorrow.
    if sys.argv[1] == '--timetable' or sys.argv[1] == '-t':
        days_in_future = 0
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            days_in_future = int(sys.argv[2])

        auth()
        timetable(days_in_future=days_in_future)

    # --- Homework Command ---
    # Usage: edul -h [old|info <id>]
    elif sys.argv[1] == '--homework' or sys.argv[1] == '-h':
        auth()
        if len(sys.argv) > 2 and sys.argv[2] == 'old':
            homeworkold()
        elif len(sys.argv) > 2 and sys.argv[2] == 'info':
            if len(sys.argv) > 3:
                homeworkid = sys.argv[3]
                homeworkinfo(homeworkid)
            else:
                print("Error: You must supply a homework ID.")
                print("Usage: edul -h info <homework_id>")
        else:
            homework()

    # --- Login Command ---
    # Creates a new login profile.
    elif sys.argv[1] == '--login' or sys.argv[1] == '-l':
        print("Which saved login ID would you like this to be? (e.g., 1, 2, 3)")
        loginid = input("Login ID: ")

        print("\nPlease input your login details:")
        username = input("Username: ")
        password = input("Password: ")
        schoolid = input("School ID/Postcode: ")

        data = {
            'username': username,
            'password': password,
            'schoolid': schoolid,
        }

        json_file_path = os.path.expanduser(f'~/edul/data/data{loginid}.json')
        directory = os.path.dirname(json_file_path)

        try:
            os.makedirs(directory, exist_ok=True)
            with open(json_file_path, 'w') as f:
                json.dump(data, f, indent=4)
            print(f"\nLogin details for account ID {loginid} saved successfully.")
            print("To use this account, run: edul -a " + loginid)
        except (IOError, OSError) as e:
            print(f"\nError: Could not save login details to file {json_file_path}: {e}")
            sys.exit(1)

    # --- Set Active Account Command ---
    # Usage: edul -a <id>
    elif sys.argv[1] == '--account' or sys.argv[1] == '-a':
        if len(sys.argv) > 2 and sys.argv[2].isdigit():
            account_id = sys.argv[2]
            config_path = os.path.expanduser('~/edul/data/active_account.txt')
            directory = os.path.dirname(config_path)

            try:
                os.makedirs(directory, exist_ok=True)
                # Check if the corresponding data file exists before setting it as active
                if not os.path.exists(os.path.expanduser(f'~/edul/data/data{account_id}.json')):
                     print(f"Error: Login details for account ID {account_id} not found.")
                     print(f"Please create it first using: edul -l")
                else:
                    with open(config_path, 'w') as f:
                        f.write(account_id)
                    print(f"Success: Active account has been set to ID {account_id}.")
            except (IOError, OSError) as e:
                print(f"Error: Could not set active account: {e}")
                sys.exit(1)
        else:
            print("Error: Please provide a valid account ID.")
            print("Usage: edul -a <id>")

    # --- Update Command ---
    # Usage: edul --update or edul -u
    elif sys.argv[1] == '--update' or sys.argv[1] == '-u':
        try:
            from updater import EdulUpdater
            updater = EdulUpdater()
            
            # Check for force flag
            force_update = '--force' in sys.argv or '-f' in sys.argv
            
            success = updater.update(force=force_update)
            if not success:
                sys.exit(1)
                
        except ImportError:
            print("❌ Error: Updater module not found.")
            print("Please reinstall Edul using the installer to get update functionality.")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Update failed: {e}")
            sys.exit(1)

    # --- Version Command ---
    # Usage: edul --version or edul -v
    elif sys.argv[1] == '--version' or sys.argv[1] == '-v':
        try:
            from updater import EdulUpdater
            updater = EdulUpdater()
            current_version = updater.get_current_version()
            
            print(f"Edul version: {current_version}")
            
            # Check if updates are available
            print("\nChecking for updates...")
            has_update, release_info = updater.check_for_updates()
            if has_update and release_info:
                latest_version = release_info['tag_name'].lstrip('v')
                print(f"Latest version available: {latest_version}")
                print("Run 'edul --update' to update.")
            
        except ImportError:
            print("Edul version: unknown")
            print("(Version tracking unavailable - please reinstall with updated installer)")
        except Exception as e:
            print(f"Edul version: unknown (error: {e})")

    # --- Help Command ---
    elif sys.argv[1] == '--help':
        help()

    # --- Catch-all for unknown commands ---
    else:
        print("Unknown command. Please run 'edul --help' to see the list of commands.")

else:
    intro()
