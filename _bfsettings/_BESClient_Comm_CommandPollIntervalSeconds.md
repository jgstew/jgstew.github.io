
Default: 12 hours (in seconds)

This setting controls how often a client polls for commands, if enabled by: `_BESClient_Comm_CommandPollIntervalSeconds`

I would recommend all systems have command polling enabled, but the interval is less obvious.

I would generally recommend all systems have it set to at least once every 3 to 6 hours, but those that are behind a NAT and can't otherwise get notifications about new content from their parent relay should have more aggressive settings.

