---
title: BigFix Settings Optimizations
author: "@JGStew"
date: November 8, 2018
---

<!-- git pull;pandoc 2018-10-30-BigFix-Settings-Optimizations.md -o BigFix_tmp.pptx;open BigFix_tmp.pptx -->

## BigFix is Extremely Flexible

- There are tons of setting that can be tweaked for almost every part of the BigFix platform.
  - Root Server
  - Relays
  - Clients
  - and more!
- No matter what your use case is, there is a setting that can help!

## Many Defaults Should Be Changed!

- There are many default BigFix Settings that are sub-optimal for almost all use cases!
- BigFix is very conservative about Defaults, and especially changing them once they have been established.

## _BESClient_Resource_PowerSaveEnable

### Default: Disabled (0)

### Recommendation: Enabled (1)

- This setting should be enabled on:
  - Laptops
  - VMs
  - Docker Containers
  - & probably everything else

- This setting tells the client to sleep (stop evaluating relevance) if things are not changing.

## Questions?

### forum.bigfix.com
### bigfix.slack.com
