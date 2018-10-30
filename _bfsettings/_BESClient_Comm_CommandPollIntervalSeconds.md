
### Default: 12 hours (43200)

### Recommendation: 3 hours (10800) or less

- This setting controls how often a client polls for commands, if [enabled by](https://github.com/jgstew/jgstew.github.io/blob/master/_bfsettings/_BESClient_Comm_CommandPollEnable.md): `_BESClient_Comm_CommandPollEnable`
- Recommend all systems have command polling enabled, but the interval is less obvious.
- all systems should have it set to at least once every 3 to 6 hours, but those that are behind a NAT and can't otherwise get notifications about new content from their parent relay should have more aggressive settings. (generally not more frequent than once every 30 minutes)

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/clientsettings/Set%20__BESClient_Comm_CommandPollIntervalSeconds_%20to%20_4000_%20-%20Universal.bes
