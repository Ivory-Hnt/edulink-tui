# Edul - Edulink-TUI 
A text based Edulink client for Linux.

## Notice: Edul only works on Linux and Android, not Windows, Mac or IOS. To use Edul on Windows, switch to Linux (or setup a WSL instance such as Arch or Ubuntu if your stuborn).

# Installation

Desktop/PC:

Please copy this, paste it then execute it in your shell:

```
git clone https://github.com/Ivory-Hnt/edulink-tui.git
cd edulink-tui
sudo chmod +x install.sh
sudo ./install.sh
```

4. Run edul -l
5. Enjoy!

Android (Termux):

Please copy and paste each command into your termux shell one by one:

```
git clone https://github.com/Ivory-Hnt/edulink-tui.git
cd edulink-tui
chmod +x install-tmux.sh
sudo ./install-tmux.sh
```

### Troubleshooting

It may tell you that the edul file exists but is not executable, or you do not have permission to run the file. To fix this, do `cd ~/usr/local/bin`, then `sudo chmod +x edul` (this only works on desktop and not termux).

If you are on an older version of edulink-tui, it may give you an error any time you try to use any file using python. This is because the python module `requests` is not installed. To install it, simply do `pip install requests`.

If it tells you something along the lines of, the folder edul/data can not be created or edul/data/data1.json can not be created/does not exist, create a directory in your home directory called edul. Within that, create a directory called data. Then, within that, create a file called data1.json. You can also create a data2.json ect for as many accounts you have saved.

If you get errors with making the installer executable on Termux, just simply execute `bash install-tmux.sh` (this only works on bash shell. If you don't know what this is, or haven't changed your shell, you are running bash).

You should now be able to execute the `edul` command without any errors. If you can't, send me a DM on discord (sodiumicecream).

## Quick Notice

This information might be out of date as updating the readme.md for this project is the least of my worries in life. If you need assistance, dm me on discord at `sodiumicecream` or email me at `ivory@ivoryhnt.dev`. The instructions for installing edul and `edul --help` are always up to date.

# Setup

To setup edul, you first need to login. To login, do `edul -l`. It will then prompt you to tell it which login ID you would like to save this as. This is because you can have as many edulink logins as you like. To learn more about this, find the edulink accounts section in the list of commands below.
For your first login, you should pick 1 as the login ID. This is because when you execute a command and do not specify which account it will use, it will default to the account saved as 1. 

Please now enter your login details when it requests it.

Your school ID may also be what edulink sometimes calls your schools postcode. You have to enter this on the website anyway when you log into an edulink account. Example: MK40 1RZ

Hopefully, you are now logged in. Here is a list of commands you can do:


## List of commands:

If a longer version of a command is available in the main command, it is avaiable for all sub commands. For example, `edul -h old` doesent show the full `--homework` command, but both `-h` and `--homework` will work. The same goes for login, timetable ect.

### Misc

`edul --help` -  Shows a list of all available commands. This command may be out of data bit.
`edul --login` or `-l`  -  Sets the login details for edul. This will be remembered after a shutdown, but is stored in plain text. This WILL be encrypted in the next update.

### Homework

`edul --homework` or `-h`  -  Shows a list of all current homework.
`edul -h old`  -  Shows a list of all old homework.
`edul -h info <homework_id>`  -  Shows more info about a homework, including description and attachment sizes. Some info such as subject may appear as an ID or not appear at all (may appear as N/A).

### Timetable

`edul --timetable` or `-t`  -  Shows you your timetable for the current day.

### Accounts

As stated above, you can have a near infinite amount of edulink accounts for edul. When you execute a command such as `edul --timetable`, it will default to the account that has the account ID, 1. To make it show the timetable for the account that has the account ID, 2, you can do this: `edul --timetable 2`. By adding the account ID as an argument at the end of a command, it tells it that it will run this command with the login details for the account with the ID, 2. This works for every other command. Obviously it won't work for commands such as `edul --help`





