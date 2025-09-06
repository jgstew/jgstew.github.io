
### Default: Disabled (0)

### Recommendation: Enabled (1)

I recommend enabling this setting, especially for Laptops, VMs, Docker containers, etc...

This setting tells the client to sleep (stop evaluating relevance) if things are not changing for a period of time, then do another evaluation loop, and if things continue to not change, then sleep again.

This setting causes the idle CPU usage of the BigFix client to drop significantly, which ends up saving battery life on laptops, while also reducing the idle CPU usage consumed by VMs, which can take a lot of load off of the hypervisor in aggregate.

The default duration the client sleeps is 10 minutes, which generally does not cause any noticeable loss of responsiveness in the client.

The sleep duration is configurable by another client setting.

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/clientsettings/Set%20__BESClient_Resource_PowerSaveEnable_%20to%20_1_%20-%20Universal.bes
