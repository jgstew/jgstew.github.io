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

This setting controls how many log files the client will keep before deleting the oldest. I think the default of 10 days is too short. 


## _BESRelay_RelaysFileUpdater_RefreshSeconds

### Default: 1 minute (60)

### Recommendation: 1 hour (3600) or more

### Applicability: root server only (exists main gather service)

- This setting controls how often the Relays.dat file is propagated through the master action site when new Relays are created.
- This setting matters most if new Relays are created frequently, so it may not need to be changed for most environments, but the default setting is extremely aggressive, which can cause issues.


## Questions?

### forum.bigfix.com
### bigfix.slack.com
