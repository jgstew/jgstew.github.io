---
published: false
---

For this example I'm going to use Windows Patches specifically, but the concept of mapping CVEs to specific patches apply to all operating systems.

When you want to make sure that you are deploying patches to fix a particular vulnerability, it can be quite complicated to figure out which patches deal with which vulnerabilities. A single exploit found could result in many distinct CVEs which could result in many distinct Microsoft KB articles for the patches for those CVEs, which could then involve different patches for different platforms that map to those Microsoft KB articles. Then each individual patch released by Microsoft will result in an individual patch being made available within BigFix as content to be deployed. All of this means that there is not a simple 1:1 relationship between an Exploit, CVEs, KB articles, and Patches.


`number of fixlets whose(source release date of it > current date - 45*day) of bes sites whose("Patches for Windows" = display name of it)`
