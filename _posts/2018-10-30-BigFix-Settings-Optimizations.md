---
title: BigFix Settings Optimizations
author: "@JGStew"
date: November 8, 2018
---

<!-- git pull;pandoc 2018-10-30-BigFix-Settings-Optimizations.md -o BigFix_tmp.pptx;open BigFix_tmp.pptx -->

## BigFix is Extremely Flexible

- There are tons of setting that can be tweaked for almost every part of the BigFix platform.
  - Root Server: `_BESRelay_` & `_BESGather_`
  - Relays: `_BESRelay_` & `_BESGather_`
  - Clients: `_BESClient_`
  - and more!
- No matter what your use case is, there is a setting that can help!


## Many Defaults Should Be Changed!

- There are many default BigFix Settings that are sub-optimal for almost all use cases!
  - This will cover the ones with the biggest impact, that are also safest to deploy.
- BigFix is very conservative about Defaults, and especially changing them once they have been established.


## _BESClient_Resource_PowerSaveEnable

### Default: Disabled (0)

### Recommendation: Enabled (1)

- This setting should be enabled on:
  - Laptops
  - VMs
  - Docker Containers
  - & probably everything else
- This setting tells the client to stop evaluating relevance if things are not changing.
  - The client will "wake" automatically if notified of new content.


## _BESRelay_HealthCheck_EnableAtStartup

### Default: Disabled (0)

### Recommendation: Enabled (1)

- Applies to Relays
- HealthCheck process validates site data integrity, and re-requests any site data that is corrupt so it can be properly served to clients.
- Can Fix `FAILED to Synchronize` errors in client logs


## _BESClient_Log_Days

### Default: 10 days (10)

### Recommendation: 31 days (31)

- This setting controls how many log files the client will keep before deleting the oldest. 
- The default of 10 days is often too short to catch issues before logs are rotated.


## _BESRelay_RelaysFileUpdater_RefreshSeconds

### Default: 1 minute (60)

### Recommendation: 1 hour (3600) or more

Applicability: root server only (exists main gather service)

- This setting controls how often the Relays.dat file is propagated when new Relays are created.
- This setting matters most if new Relays are created frequently, but the default setting is extremely aggressive.


## _BESClient_Comm_CommandPollEnable

### Default: Disabled (0)

### Recommendation: Enabled (1)

- It should be enabled on 100% of endpoints, it is just a matter of how frequent the command polling should be done.
- The frequency of command polling is controlled by [the setting](https://github.com/jgstew/jgstew.github.io/blob/master/_bfsettings/_BESClient_Comm_CommandPollIntervalSeconds.md): 
  - `_BESClient_Comm_CommandPollIntervalSeconds`


## _BESClient_Comm_CommandPollIntervalSeconds

### Default: 12 hours (43200)

### Recommendation: 3 hours (10800) or less

- This setting controls how often a client polls for commands, if [enabled by](https://github.com/jgstew/jgstew.github.io/blob/master/_bfsettings/_BESClient_Comm_CommandPollEnable.md): 
  - `_BESClient_Comm_CommandPollEnable`
- Recommend all systems have command polling enabled, but the interval is less obvious.
- All systems should have it set to at least once every 6 hours.
- Those not getting UDP should have a more aggressive value.
  - Generally not more often than once every 30 minutes


## _BESClient_Download_UtilitiesCacheLimitMB

### Default: 10MB (10)

### Recommendation: 200MB (200) or more

- This setting controls the maximum size of the pool of storage to hold utilities in a separate cache that does not get cleared out in the same way as the Client's Download Cache.
- This cache is designed for small files that are used across many different actions where you would not want them to have to be redownloaded everytime.


## I'm Convinced, Now What?

### 4 Actions Designed to Target ALL COMPUTERS:

- ***Run Once:*** Set initial client settings if unset
- ***Run Always:*** Force command polling to be enabled
- ***Run Always:*** Set command polling to at least once every 6 hours
- ***Run Once:*** Set `_BESClient_Resource_PowerSaveEnable` after 2 days in BigFix


## Questions?

### forum.bigfix.com
### bigfix.slack.com

## References:

- https://github.com/jgstew/jgstew.github.io/tree/master/_bfsettings
- https://github.com/jgstew/bigfix-content/issues/2
- https://github.com/jgstew/bigfix-content/blob/master/dashboards/ClientSettingsManager.ojo
