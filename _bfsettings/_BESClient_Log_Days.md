
### Default: 10 days (10)

### Recommendation: 31 days (31)

This setting controls how many log files the client will keep before deleting the oldest. I think the default of 10 days is too short.

Often issues are reported after the log that would have the origin time / source of the issue is deleted. I think 1 month of logs makes much more sense then the default of 10 days.

The default maximum size of each log is 0.5MB for a maximum total of 15.5MB which is not big enough to worry about. I would also recommend increasing the maximum size of each log to 1MB.

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/clientsettings/Set%20__BESClient_Log_Days_%20to%20_30_%20-%20Universal.bes
