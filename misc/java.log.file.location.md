The default location (directory) of the trace and log files is:
```
* <user.home>/.java/deployment/log on UNIX, Linux
* ~/Library/Application Support/Oracle/Java/Deployment/log on Mac OS X
* <User Application Data Folder>\Sun\Java\Deployment\log on Windows
```

If the environment variable USER_JPI_PROFILE is set to <user plugin home> then the trace and log files will be written to:
```
* <user plugin home>/.java/deployment/log on UNIX, Linux
* <user plugin home>/Library/Application Support/Oracle/Java/Deployment/log on Mac OS X
* <user plugin home>\Sun\Java\Deployment\log on Windows
```