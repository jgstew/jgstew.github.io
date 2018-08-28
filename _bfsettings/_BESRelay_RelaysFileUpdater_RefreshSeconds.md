
Default: 1 minute (60)

Recommendation: 1 hour (3600) or more

Applicability: root server only (exists main gather service)

This setting controls how often the Relays.dat file is propagated through the master action site when new Relays are created.

This setting matters most if new Relays are created frequently, so it may not need to be changed for most environments, but the default setting is extremely aggressive, which can cause issues.

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/clientsettings/Set%20__BESRelay_RelaysFileUpdater_RefreshSeconds_%20to%20_21600_%20-%20Universal.bes
