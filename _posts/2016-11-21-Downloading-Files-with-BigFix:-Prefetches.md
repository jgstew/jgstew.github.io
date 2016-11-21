The majority of BigFix content downloads file(s) and then does something with them.

The downloads could be many different things:

- Configuration Files
- Scripts
- Software Installers
- Patches (software or OS)
- Drivers
- ...etc...

The "Best" way to download files with BigFix is to use something called a `prefetch`.

A `prefetch` allows BigFix to securely download files while validating that the downloaded file is not corrupted or maliciously altered.

A `prefetch` has a few components, the most important being the size of the file and it's hash(es).

The `prefetch` allows the BigFix client to check it's own caches before downloading a file it may already have, which speeds things up. It also allows the client to request the file from a Relay server which has it's own cache. This allows many BigFix clients to all download the same file at the same time without having to reach far outside of the local network. This can be a huge advantage for slow WAN links, or even local links between floors and buildings.

