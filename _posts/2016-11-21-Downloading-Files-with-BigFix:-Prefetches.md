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

- SHA1
- SHA256
- Size
- URL
- Filename
 - the Filename can be almost anything
 - the Filename is only used as the name of the file that the download is saved to

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
- https://bigfix.me/relevance/details/2998745


#### Example:

	begin prefetch block
		add prefetch item name=unzip.exe sha1=e1652b058195db3f5f754b7ab430652ae04a50b8 sha256=8d9b5190aace52a1db1ac73a65ee9999c329157c8e88f61a772433323d6b7a4a size=167936 url=http://software.bigfix.com/download/redist/unzip-5.52.exe
	end prefetch block

## Generating Prefetches

You can figure out the needed info for a prefetch many different ways.

- the Filename is whatever you want it to be
- the size is easily determined if you have a copy of the file handy
- the URL is wherever the file can be downloaded from
 - Could be the root server, the public internet, or your own software repo
 - generally it must be available over HTTP or HTTPS
- the SHA1 & SHA256 hashes can be calculated using a copy of the file using many different tools
 - there are thousands of tools that can be used for hashing

Once all the parts are determined, you can just combine them by hand into a prefetch. This isn't ideal and it is much nicer to use BigFix specific tools to more completely automate the process.

----------

### Work In Progress

#### I plan to document many of these options in detail.

- https://bigfix.me/relevance/details/2998745
- https://bigfix.me/relevance/details/2998744
- https://forum.bigfix.com/t/prefetch-automator-services-for-os-x/13855
- https://github.com/hansen-m/bigfix-automator-services/
- https://github.com/CLCMacTeam/AutoPkgBESEngine/blob/master/Code/AutoPkgBESEngine.py#L140
- https://github.com/strawgate/make-prefetch
- https://github.com/bigfix/make-prefetch
- https://forum.bigfix.com/t/prefetch-statement-powershell-4-0-for-local-files/15145/6
- https://github.com/peterj04/PowerShell-MakePrefetch
- BF File Properties: https://bigfix.me/projects/details/7
- https://github.com/jgstew/tools/tree/master/JS/VirusTotal2Prefetch
- https://md5file.com/calculator
- https://github.com/Miserlou/omnihash
 - `omnihash -f SHA256 -f SHA1 -f LENGTH omnihash.exe`

## Related Materials

- https://forum.bigfix.com/t/create-content-to-install-windows-software-from-scratch/19208
 - https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2016-11-14-Create-BigFix-Content-to-Install-Windows-Software-From-Scratch.md
- https://forum.bigfix.com/t/make-prefetch-now-supports-both-python-2-and-3/15101
- http://www-01.ibm.com/support/knowledgecenter/SS63NW_9.2.0/com.ibm.tivoli.tem.doc_9.2/Platform/Action/c_introducing_the_prefetch_block.html?cp=SS63NW_9.2.0&lang=en
- http://marklets.com/BigFixPrefetch%20added%20to%20VirusTotal%20analysis%20table.aspx
