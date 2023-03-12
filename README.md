## Synchronize Two Folders:
#### It is a Python script, synchronizes two folders: source and replica. The program should maintain a full, identical copy of source folder at replica folder.

#### 1- synchronisation will be in one-way: after the synchronisation, the content of the replica folder is modified to exactly match content of the source folder.
#####           - Check of content will be done twice. One to see if we need to reload the file the one after creating/ copying operations to be sure that the process was happened smoothly without any issues.

#### 2- Synchronization is performed periodically: Use apscheduler.schedulers.background package to schedule the process where the script to synchronize the Source and Replica folders will run every 3600 seconds till specific date.

#### 3- File creation/copying/removal operations are logged to a file (log.txt) and to the console output.

#### 4- Folder paths, synchronisation interval and log file path are provided using the command line arguments.

#### 5-  MD5 message-digest algorithm is used as a checksum to verify data integrity against unintentional corruption.

#### 6- Message box is provided to quick message access to the user to inform about the status of the process.
