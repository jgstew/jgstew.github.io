
Default: 0

By default, command polling is disabled.

I feel that it should be enabled on 100% of endpoints, it is just a matter of how frequent the command polling should be done.

The frequency of command polling is controlled by the setting: `_BESClient_Comm_CommandPollEnable`

Command polling will cause slightly more load on relays by the endpoints configured to use it, but it will make the endpoints much more responsive.

