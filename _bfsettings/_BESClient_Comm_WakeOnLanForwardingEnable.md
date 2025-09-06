
Default: 0 (Disabled)

Recommendation: 1 (Enabled)

As far as I can tell, there is no harm in having 100% of computers having this setting enabled.

If enabled, then the client will sometimes be told to send Wake On LAN packets to other computers on it's subnet to wake them when needed.

Successful use of Wake On LAN requires that at least 1 computer per subnet be awake and configured for Wake On LAN.

If Wake On LAN is not used, then this setting will have no real affect.

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/clientsettings/Set%20__BESClient_Comm_WakeOnLanForwardingEnable_%20to%20_1_%20-%20Universal.bes
