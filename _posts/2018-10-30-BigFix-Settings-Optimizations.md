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
- This setting controls how often the Relays.dat file is propagated through the master action site when new Relays are created.
- This setting matters most if new Relays are created frequently, so it may not need to be changed for most environments, but the default setting is extremely aggressive.


## _BESClient_Comm_CommandPollEnable

### Default: Disabled (0)

### Recommendation: Enabled (1)

- It should be enabled on 100% of endpoints, it is just a matter of how frequent the command polling should be done.
- The frequency of command polling is controlled by [the setting](https://github.com/jgstew/jgstew.github.io/blob/master/_bfsettings/_BESClient_Comm_CommandPollIntervalSeconds.md): `_BESClient_Comm_CommandPollIntervalSeconds` (default: 12 hours)


## _BESClient_Comm_CommandPollIntervalSeconds

### Default: 12 hours (43200)

### Recommendation: 3 hours (10800) or less

- This setting controls how often a client polls for commands, if [enabled by](https://github.com/jgstew/jgstew.github.io/blob/master/_bfsettings/_BESClient_Comm_CommandPollEnable.md): `_BESClient_Comm_CommandPollEnable`
- Recommend all systems have command polling enabled, but the interval is less obvious.
- all systems should have it set to at least once every 3 to 6 hours, but those that are behind a NAT and can't otherwise get notifications about new content from their parent relay should have more aggressive settings. (generally not more frequent than once every 30 minutes)


## Questions?

### forum.bigfix.com
### bigfix.slack.com
