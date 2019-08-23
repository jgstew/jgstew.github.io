
For this example I'm going to use Windows Patches specifically, but the concept of mapping CVEs to specific patches apply to all operating systems.

When you want to make sure that you are deploying patches to fix a particular vulnerability, it can be quite complicated to figure out which patches deal with which vulnerabilities. A single exploit found could result in many distinct CVEs which could result in many distinct Microsoft KB articles for the patches for those CVEs, which could then involve different patches for different platforms that map to those Microsoft KB articles. Then each individual patch released by Microsoft will result in an individual patch being made available within BigFix as content to be deployed. All of this means that there is not a simple 1:1 relationship between an Exploit, CVEs, KB articles, and Patches.

Right now, (this will change over time) there are **7883 distinct patches with CVEs** in the BigFix Patches for Windows site as given by the following BigFix Session Relevance: `number of fixlets whose(exists cve id list whose(it != "Unspecified" AND it != "N/A") of it) of bes sites whose("Patches for Windows" = display name of it)`

These 7883 distinct patches in BigFix help resolve **2825 distinct CVEs** as given by: `number of unique values of (it as trimmed string) whose(it != "") of substrings separated by ";" of cve id lists whose(it != "Unspecified" AND it != "N/A") of fixlets of bes sites whose("Patches for Windows" = display name of it)`

These 7883 distinct patches are for **2279 distinct Microsoft KB Articles** as given by: `number of unique values of source ids whose(it does not contain "Unspecified") of fixlets whose(exists cve id list whose(it != "Unspecified" AND it != "N/A") of it) of bes sites whose("Patches for Windows" = display name of it)`

See this article to test the above BigFix Session Relevance yourself in the BigFix Windows Console Presentation Debugger: https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md

### Search for which windows patches in BigFix resolve a particular CVE or Microsoft KBs:

The following BigFix Session Relevance will find all patches which resolve **CVE-2019-1162**:

`names of fixlets whose(exists (cve id list of it | ""; source id of it | "") whose(it as lowercase contains "CVE-2019-1162" as trimmed string as lowercase) ) of bes sites whose("Patches for Windows" = display name of it)`

The following BigFix Session Relevance will find all patches which resolve Microsoft **KB4511553**:

`names of fixlets whose(exists (cve id list of it | ""; source id of it | "") whose(it as lowercase contains "KB4511553" as trimmed string as lowercase) ) of bes sites whose("Patches for Windows" = display name of it)`

Notice that both of these examples are using the same BigFix Session Relevance, only changing which value is being queried. This could easily be turned into a BigFix Windows Console Dashboard which would make it easier to search for windows patches based upon CVE or KB article. 

### How to find the related Session Relevance Inspectors:

I was able to figure out how to write the BigFix Session Relevance for Fixlet CVEs by searching on [developer.bigfix.com](https://developer.bigfix.com/relevance/search/) for CVE like the following photo: 

![Search Results for CVE](http://jgstew.github.io/images/posts/BigFix-Mapping-CVEs-to-Patches-01.png)


Which lead me to: [https://developer.bigfix.com/relevance/reference/bes-fixlet.html#cve-id-list-of-bes-fixlet-string](https://developer.bigfix.com/relevance/reference/bes-fixlet.html#cve-id-list-of-bes-fixlet-string)


### Example Session Relevance

`number of fixlets whose(source release date of it > current date - 45*day) of bes sites whose("Patches for Windows" = display name of it)`
