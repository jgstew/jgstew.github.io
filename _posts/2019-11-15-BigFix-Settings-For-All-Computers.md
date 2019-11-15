
In this document I'm going to outline what I feel are conservative tweaks to BigFix Client Settings that should be safe for 99% of computers in 99% of BigFix deployments. In some cases more aggressive settings are warranted, while in others less aggressive settings are needed, which often depends on size of the deployment and resources available in various components.

## BigFix Client Settings Recommendations:
<br/>


### _BESClient_Log_Days

- This setting controls how many log files the client will keep before deleting the oldest. 

#### Default: 10 days (10)
#### Recommendation: 31 days (31)

- The default of 10 days is often too short to catch issues before logs are rotated.
- 1 full month of logs is very useful


### _BESClient_Comm_CommandPollEnable

#### Default: Disabled (0)
#### Recommendation: Enabled (1)

- It should be enabled on 100% of endpoints, it is just a matter of how frequent the command polling should be done.
- Even better would be a setting to tell BigFix to do command polling only if UDP hasn't been recieved in longer than the command polling interval.


### _BESClient_Download_UtilitiesCacheLimitMB

#### Default: 10MB (10)

#### Recommendation: 200MB (200) or more

- This setting controls the maximum size of the storage for utilities in a cache that does not get cleared out in the same way as the Client's Download Cache.

<br/>

## Related:

- https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-30-BigFix-Settings-Optimizations.md
- https://github.com/jgstew/bigfix-content/issues/2
- https://github.com/jgstew/bigfix-content/tree/master/fixlet/clientsettings
- https://github.com/jgstew/bigfix-content/blob/master/dashboards/ClientSettingsManager.ojo
