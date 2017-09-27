
I love BigFix and I use it for almost everything, but it has some things that need improvement, and this post is about what I think are the biggest missing pieces. 


## BigFix Platform

- DEP & MDM: BigFix needs to provide an easy way to be deployed through MDM for both Windows & Mac.
 - Provide an option to use a free MDM and deploy bigfix through the MDM, and support DEP / AzureAD Enrollment
 - Provide documentation for doing the same with some 3rd party MDMs including MAAS360, Casper, Intune.

- Relays need to be easier, especially for small deployments that shouldn't have to worry about it.
 - Peer to peer file transfer should be an option, especially now that Windows 10 does this for Windows Updates by default.
 - Relays currently offer a lot of control and flexibility, but at the cost of overhead that is a lot to bear for small deployments.

- Too Many Servers for all of the parts of BigFix
 - The core platform really only needs 1 server, but if you want all of the features, you need many
 - Breaking out the servers by function is in many ways a very good thing to be able to do, but having many servers is a burden for small deployments
 - Use something like docker / containerization to make the infrastructure more self-managing and lighter weight.

- Improve MultiTenancy
 - This is already a strength of BigFix, but it could definitely be better and isn't supported by every part of it.

## Relevance Inspectors

### Mac specific

The mac needs some love, especially in inspectors.

- Profiles
 - This is critical for modern MacOS managment. 
- XML
 - Other OSes have this, this is a big omission. 
- OSQuery

### Windows specific

- LocalGPO / Registry.pol

### Universal

- OSQuery
