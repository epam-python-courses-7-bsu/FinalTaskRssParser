
This program which receives RSS URL and prints results in human-readable
format.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --version      Print version info
  --json         Print result as JSON in stdout
  --verbose      Outputs verbose status messages
  --limit LIMIT  Limit news topics if this parameter provided



Installation recommendation rss-reader:
1)Open terminal 
2)Enter "pip install setuptools" or "pip3 install setuptools"
3)Go to the folder final_task
4)Enter "python3 setup.py install"
5)Application installed
6)To run the utility, type in the terminal "rss-reader" then a space and url on news
Example : rss-reader  https://news.yahoo.com/rss


To use caching you must have a postgresql database on your computer or laptop
with default parameters:
    database="postgres",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"    
If you do not, follow these commands:    
1)Open terminal
2)sudo apt-get install postgresql
3)sudo -u postgres psql
4)\password
5)1
6)1
7)\conninfo find out the port and if it is not equal 5432, change the config.txt port to your
If after all you couldn’t connect postgresql, change 
localhost in the config.txt file to your IP address,
you can find it using the following commands:
1)Open terminal
2) Enter nslookup localhost
You will need an address in a format similar to this:
"127.0.0.1" in line "Address: 127.0.0.1"

 


You can change the database connection parameters in the "config.txt" file in the project, 
but then you need to update the utility, for this you need:
1) Open a terminal
2) Go to the "final_task" folder
3) Enter "python3 setup.py install"

How to use the --date parameter:
1)--date works with all other arguments (e.g. --limit, --json)
2)If you use --date you do not need an internet connection
3)if you didn’t succeed in correctly downloading the database, 
  you will be deprived of the caching parameter, but everything else will work correctly
4)Usage example:rss-reader https://news.tut.by/rss/ --date 20191120





