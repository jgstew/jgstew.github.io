
Default: 10MB (10)

Recommendation: 200MB to 1000MB

This setting controls the maximum size of the pool of storage to hold utilities in a separate cache that does not get cleared out in the same way as the Client's Download Cache.

In order for things to be stored in the client utility cache, they have to be explicitly added through actionscript command.

This cache is designed for small files that are used across many different actions where you would not want them to have to be redownloaded everytime. 

### Actionscript:

`utility __Download\common.exe`

### Examples:

- https://github.com/jgstew/bigfix-content/blob/master/fixlet/add%20NirCmd%202.8.1%20to%20bigfix%20client%20utility%20cache%20-%20Windows.bes

### References:

- https://developer.bigfix.com/action-script/reference/file/utility.html
