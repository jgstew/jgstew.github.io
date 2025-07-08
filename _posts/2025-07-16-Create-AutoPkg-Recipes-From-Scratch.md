---
published: false
category: Other
---

## Example: Firefox

- Go here: https://www.mozilla.org/en-US/firefox/all/
- Click Firefox under "Desktop" section
- Click macOS
- Click English (US) - English (US)
- This should result in this URL: https://www.mozilla.org/en-US/firefox/all/desktop-release/osx/en-US/
- Right click on "Download Now" button
- Select "Copy Link Address"
- This should give you this URL: https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
- Do the same for Windows: https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
- Do the same for Linux: https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US

These URLs will redirect to the newest Firefox download for each platform. We are going to use these URLs to determine the static download link for the newest version of firefox.

- Click the "Download Now" button
- Open the browser download page
- Copy the link of the actual download
- You should get a link like this: https://download-installer.cdn.mozilla.net/pub/firefox/releases/140.0.4/mac/en-US/Firefox%20140.0.4.dmg

Notice that this URL contains the version number for the latest version of Firefox that we downloaded.

Create an autopkg download recipe to download the latest Firefox for MacOS using the URL above:

```
---
Description: download Firefox for MacOS
Identifier: com.github.macadmins.Firefox-Mac
Input:
  NAME: Firefox-Mac
MinimumVersion: "2.3"
Process:
  - Processor: com.github.jgstew.SharedProcessors/URLDownloaderPython
    Arguments:
      url: https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
      filename: Firefox.dmg
      COMPUTE_HASHES: True
```
