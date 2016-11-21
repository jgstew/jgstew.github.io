The majority of BigFix content downloads file(s) and then does something with them.

The downloads could be many different things:

- Configuration Files
- Scripts
- Software Installers
- Patches (software or OS)

The "Best" way to download files with BigFix is to use something called a `prefetch`.

A `prefetch` allows BigFix to securely download files while validating that the downloaded file is not corrupted or maliciously altered.

A `prefetch` has a few components, the most important being the size of the file and it's hash(es).

