# Edulink-TUI
An unofficial terminal user interface for accessing edulink.

## Instructions

I have not added an install script yet, so you will have to do it manually. Make sure all the files are located in /usr/local/bin/. 

You should now be able to execute the edul command. If you can't, send me a DM on discord (sodiumicecream). 

First, you need to log in. Do edul -l to login, then enter your login details. 

You are now logged in. Here is a list of commands you can do:


## List of commands:

If a longer version of a command is available in the main command, it is avaiable for all sub commands. For example, edul -h old doesent show the full --homework command, but both -h and --homework will work. The same goes for login, timetable ect.

### Misc

edul --help  -  Shows a list of all available commands. This command may be out of data bit.
edul --login or -l  -  Sets the login details for edul. This will be remembered after a shutdown, but is stored in plain text. This WILL be encrypted in the next update.

### Homework

edul --homework or -h  -  Shows a list of all current homework.
edul -h old  -  Shows a list of all old homework.
edul -h info <homework_id>  -  Shows more info about a homework, including description and attachment sizes. Some info such as subject may appear as an ID or not appear at all (may appear as N/A).

### Timetable

edul --timetable or -t  -  Shows you your timetable for the current day.
