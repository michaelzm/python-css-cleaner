# python-css-cleaner
Small python script for web development. 
Will search all html, css and js files for div classes in order to find unused classes.

## Features:
* find css classes without matching html div classes
* find div classes without matching css classes or js functions
* ignore folders or files for the script

Works well with jQuery functions inside js files.
  
Run the script inside the root directory of your project and input folders/files you wish to ignore.

Will create a report.txt containing all unused classes.

Use pyhon3

Start the script with "python compare.py"
