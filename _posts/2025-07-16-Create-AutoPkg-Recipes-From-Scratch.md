---
published: false
category: Other
---

## Example: Firefox Download Recipes

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

Now we can create a windows download recipe based upon this one: Firefox-Win.download.recipe.yaml

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

`ParentRecipe: com.github.macadmins.Firefox-Mac` means that this recipe will run first, but using the items in the `Input` area of our `com.github.macadmins.Firefox-Win` recipe.

Then we can do the same, but for Linux: Firefox-Linux.download.recipe.yaml

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


## Example: Firefox MacOS Homebrew Recipe

Now that we have a working download recipe for FireFox for MacOS, we need to create a recipe to "package" it for a distribution tool.

For this example, we are going to make a homebrew cask.

We are going to start with a working example then turn it into a template so that we can automate the creation of it using AutoPkg.

Here is a working example that installs an outdated version of FireFox: firefox.example.rb

```
# https://github.com/Homebrew/homebrew-cask/blob/master/Casks/f/firefox.rb
cask "firefox" do
    version "127.0.2"

    language "en", default: true do
      sha256 "af516f0222361a311e83de8ca9a27a99653b2c0a00a6653e25ab59046a44d128"
      "en-US"
    end

    url "https://download-installer.cdn.mozilla.net/pub/firefox/releases/#{version}/mac/#{language}/Firefox%20#{version}.dmg",
        verified: "download-installer.cdn.mozilla.net/pub/firefox/releases/"
    name "Mozilla Firefox"
    desc "Web browser"
    homepage "https://www.mozilla.org/firefox/"

    livecheck do
      url "https://download.mozilla.org/?product=firefox-latest-ssl&os=osx"
      strategy :header_match
    end

    auto_updates true
    conflicts_with cask: [
      "firefox@beta",
      "firefox@cn",
      "firefox@esr",
    ]
    depends_on macos: ">= :catalina"

    app "Firefox.app"
    # shim script (https://github.com/Homebrew/homebrew-cask/issues/18809)
    shimscript = "#{staged_path}/firefox.wrapper.sh"
    binary shimscript, target: "firefox"

    preflight do
      File.write shimscript, <<~EOS
        #!/bin/bash
        exec '#{appdir}/Firefox.app/Contents/MacOS/firefox' "$@"
      EOS
    end

    uninstall quit: "org.mozilla.firefox"

    zap trash: [
          "/Library/Logs/DiagnosticReports/firefox_*",
          "~/Library/Application Support/com.apple.sharedfilelist/com.apple.LSSharedFileList.ApplicationRecentDocuments/org.mozilla.firefox.sfl*",
          "~/Library/Application Support/CrashReporter/firefox_*",
          "~/Library/Application Support/Firefox",
          "~/Library/Caches/Firefox",
          "~/Library/Caches/Mozilla/updates/Applications/Firefox",
          "~/Library/Caches/org.mozilla.crashreporter",
          "~/Library/Caches/org.mozilla.firefox",
          "~/Library/Preferences/org.mozilla.crashreporter.plist",
          "~/Library/Preferences/org.mozilla.firefox.plist",
          "~/Library/Saved Application State/org.mozilla.firefox.savedState",
          "~/Library/WebKit/org.mozilla.firefox",
        ],
        rmdir: [
          "~/Library/Application Support/Mozilla", #  May also contain non-Firefox data
          "~/Library/Caches/Mozilla",
          "~/Library/Caches/Mozilla/updates",
          "~/Library/Caches/Mozilla/updates/Applications",
        ]
  end
```

We can test this existing example to make sure it works using:

`brew install --cask --verbose firefox.example.rb`
