This directory contains a test suite for the mongoDB daemon. To run the 
core JavaScripts tests, execute "./resmoke.py --suites core" in this 
directory.

For use in Red Hat distributions, you should run the script as user 
mongodb, who is created with nologin shell however, so the best bet is 
something like:
       $ su -
       # cd /usr/share/mongodb-test
       # su -s /bin/bash mongodb -c "./resmoke.py --suites core"

This will use the installed mongodb executables, but will run a private 
copy of the server process (using data files within 
/usr/share/mongodb-test/var/), so you need not start the mongod service 
beforehand.

To clean up afterwards, remove the created "var/*" subdirectories, eg
       # su -s /bin/bash - mongodb -c "rm -rf /usr/share/mongodb-test/var/*"

If one or more tests fail on your system, please read the following 
manual section for instructions on how to report the problem:

http://www.mongodb.org/about/contributors/tutorial/submit-bug-reports/

MongoDB offers several test suites. To get list of provided test suites 
run "./resmoke.py -l".

If you want to run a specific test, simply add path to JavaSctipt file 
from /usr/share/mongodb-test/jstests/ you want to run to the option to 
resmoke.py. It is also possible to specify more files. For example to 
run jstests/disk/*.js files execute "./resmoke.py jstests/disk/*.js"

If you want to use some specific storage engine for mongod server you 
have to specify --storageEngine option. Actualy there are two stable 
storage engines: mmapv1 and wiredTiger (x86_64 only).

For more options run "./resmoke.py --help".


In Red Hat distributions use this syntax:
       $ su -
       # cd /usr/share/mongodb-test
       # su -s /bin/bash mongodb -c "./resmoke.py OPTIONS"

More info about mongoDB testing: 
http://www.mongodb.org/about/contributors/tutorial/test-the-mongodb-server/



Notes:

- ARM architecture is not fully supported - 
  https://jira.mongodb.org/browse/SERVER-1811

- This subpackage does not contain dbtest binary (it is going to be 
  deprecated).

