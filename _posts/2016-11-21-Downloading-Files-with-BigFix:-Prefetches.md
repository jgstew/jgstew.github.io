The majority of BigFix content downloads file(s) and then does something with them.

The downloads could be many different things:

- Configuration Files
- Scripts
- Software Installers
- Patches (software or OS)
- Drivers
- ...etc...

The "Best" way to download files with BigFix is to use something called a `prefetch`.

## Why Prefetches? Speed and Security

A `prefetch` allows BigFix to securely download files while validating that the downloaded file is not corrupted or maliciously altered.

A `prefetch` allows the BigFix client to check it's own caches before downloading a file it may already have, which speeds things up. It also allows the client to request the file from a Relay server which has it's own cache. This allows many BigFix clients to all download the same file at the same time without having to reach far outside of the local network. This can be a huge advantage for slow WAN links, or even local links between floors and buildings.

## What is a Prefetch?

A `prefetch` has a few components, the most important being the size of the file and it's hash(es).

- Filename
- SHA1
- SHA256
- Size
- URL

The most common form of a `prefetch` is called a Prefetch Statement, and it takes this form:

prefetch FileName sha1:`theSha1` size:`theSize` http://URL sha256:`theSha256`

### Examples:

- prefetch VSCodeSetup.exe sha1:0f88ffb5da19828690baceca512c9dc3c3a99888 size:33446608 https://az764295.vo.msecnd.net/stable/02611b40b24c9df2726ad8b33f5ef5f67ac30b44/VSCodeSetup-1.7.1.exe sha256:4f1a406321af2f90d16e5b753529d205e66d4f6eeaa5f925566c43b8f8e70638
