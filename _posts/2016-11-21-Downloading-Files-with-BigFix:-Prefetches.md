The majority of BigFix content downloads file(s) and then does something with them.

The downloads could be many different things:

- Configuration Files
- Scripts
- Software Installers
- Patches (software or OS)
- Drivers
- ... Others

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

### Prefetch Statements

The most common form of a `prefetch` is called a Prefetch Statement, and it takes this form:

**prefetch `theFileName` sha1:`theSha1` size:`theSize` `http://theURL` sha256:`theSha256`**

#### Example:

- `prefetch unzip.exe sha1:e1652b058195db3f5f754b7ab430652ae04a50b8 size:167936 http://software.bigfix.com/download/redist/unzip-5.52.exe sha256:8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a`

### Prefetch Blocks

Prefetch blocks are a less common form of `prefetch`. They are really only needed for rare extra functionality or very complex situations. It is useful to be able to understand a prefetch block if you come across one, but it is not likely that you will need to create one.

Prefetch blocks have all the same general parts as prefetch statements, but in a block structure:

    begin prefetch block
        add prefetch item name=theFileName sha1=theSha1 sha256=theSha256 size=theSize url=http://theURL
    end prefetch block

It is possible to convert a prefetch statement into a prefetch block and vis versa:

- https://bigfix.me/relevance/details/2999075
- https://bigfix.me/relevance/details/3018837


#### Example:

	begin prefetch block
		add prefetch item name=unzip.exe sha1=e1652b058195db3f5f754b7ab430652ae04a50b8 sha256=8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a size=167936 url=http://software.bigfix.com/download/redist/unzip-5.52.exe
	end prefetch block
