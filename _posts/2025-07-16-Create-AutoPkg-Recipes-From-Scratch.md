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

Create an autopkg download recipe `Firefox-Mac.download.recipe.yaml` to download the latest Firefox for MacOS using the URL above:

```
---
Description: Download Firefox for MacOS
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

  - Processor: EndOfCheckPhase
```

Run the recipe and see the output. It should download the newest version of firefox.

Add the following to the end of the download recipe to also get the version number:

```
  - Processor: com.github.jgstew.SharedProcessors/TextSearcher
    Arguments:
      input_string: "%download_url%"
      re_pattern: 'releases/(?P<version>\d+(\.\d+)+)/'
```

Run the recipe again. You should see that firefox does not download again, and this time a version number is shown in the output.

Now compare the download links for macos and windows:

```
https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
```

The only difference is the macos one uses `osx` and the windows one uses `win64`. We can restructure the download recipe to make this easier to reuse.

```
---
Description: Download Firefox for MacOS
Identifier: com.github.macadmins.Firefox-Mac
Input:
  NAME: Firefox-Mac
  os: osx
  filename: Firefox.dmg
MinimumVersion: "2.3"
Process:
  - Processor: com.github.jgstew.SharedProcessors/URLDownloaderPython
    Arguments:
      url: https://download.mozilla.org/?product=firefox-latest-ssl&os=%os%&lang=en-US
      COMPUTE_HASHES: True

  - Processor: EndOfCheckPhase

  - Processor: com.github.jgstew.SharedProcessors/TextSearcher
    Arguments:
      input_string: "%download_url%"
      re_pattern: 'releases/(?P<version>\d+(\.\d+)+)/'
```

Should run this and make sure we get the same output as before.

Now we can create a windows download recipe based upon this one:

```
---
Description: Download Firefox for Win
Identifier: com.github.macadmins.Firefox-Win
Input:
  NAME: Firefox-Win
  os: win64
  filename: FirefoxSetup.exe
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.Firefox-Mac
```

Run this and see the different output.

Then we can do the same, but for Linux:

```
---
Description: download Firefox for Linux
Identifier: com.github.macadmins.Firefox-Linux
Input:
  NAME: Firefox-Linux
  os: linux64
  filename: firefox.tar.xz
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.Firefox-Mac
```
