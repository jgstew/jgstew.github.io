---
published: false
---

For this example I'm going to use Windows Patches specifically, but the concept of mapping CVEs to specific patches apply to all operating systems.

When you want to make sure that you are deploying patches to fix a particular vulnerability, it can be quite complicated to figure out which patches deal with which vulnerabilities. A single exploit found could result in many distinct CVEs which could result in many distinct Microsoft KB articles for the patches for those CVEs, which could then involve different patches for different platforms that map to those Microsoft KB articles. Then each individual patch released by Microsoft will result in an individual patch being made available within BigFix as content to be deployed. All of this means that there is not a simple 1:1 relationship between an Exploit, CVEs, KB articles, and Patches.

Right now, (this will change over time) there are 7883 distinct patches with CVEs in the BigFix Patches for Windows site as given by the following BigFix Session Relevance: `number of fixlets whose(exists cve id list whose(it != "Unspecified" AND it != "N/A") of it) of bes sites whose("Patches for Windows" = display name of it)`

These 7883 distinct patches in BigFix help resolve 2825 distinct CVEs as given by: `number of unique values of (it as trimmed string) whose(it != "") of substrings separated by ";" of cve id lists whose(it != "Unspecified" AND it != "N/A") of fixlets of bes sites whose("Patches for Windows" = display name of it)`

### Example Session Relevance

`number of fixlets whose(source release date of it > current date - 45*day) of bes sites whose("Patches for Windows" = display name of it)`
