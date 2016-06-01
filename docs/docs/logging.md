---
title: Logging
---

# Accessing Log Information

Jenkins utilizes java.util.logging to generate logs. This system sends each log above the logging level INFO to stdout, which is captured and stored by Jenkins and can be viewed in the web GUI. By default, Jenkins contains one log recorder that displays all logs of level INFO or above. 

Fortunately, Jenkins allows for the configuration of custom log recorders of your choosing. This is useful for troubleshooting/debugging interesting behavior (i.e. looking at resource offers made to the Jenkins Scheduler when it is not running builds but should be).

The following example details how to access the system log in the Jenkins web GUI and set up a custom logger that looks at the logs for just the Jenkins-Mesos scheduler.


#### Accessing the system log in the Jenkins UI


From the 'Manage Jenkins' page of the web UI, select 'System Log'
![Accessing the system log in the Jenkins UI]({{site.baseurl}}/img/access-system-log.png)


#### Creating and configuring a new custom logger


Here you will see the default log recorder provided by Jenkins and the option to create a custom log recorder.
![Create a new log recorder]({{site.baseurl}}/img/create-log-recorder.png)


After creating a new logger and naming it, you will reach the logger configuration page. Here you will be able to add and configure loggers by specifying the logger level and specific places to look at. In this example, we want to observe only the scheduler in the Jenkins-Mesos plugin. This can be done by either typing the exact package name that leads to the scheduler or typing a keyword like 'scheduler' and using the drop-down. Additionally, we will set the logger level to FINE since that is logging level of resource offers in the plugin. 

![Configure a logger]({{site.baseurl}}/img/logger-configuration.png)

#### Viewing logger output
At this point, Jenkins requires a quick restart for the new log recorder to begin doing work. Afterwards, navigate back to the 'System Log' page and select your new log recorder. We can now see that the log recorder has begun recording messages from the Jenkins-Mesos scheduler.

![Viewing Logger Output]({{site.baseurl}}/img/log.png)