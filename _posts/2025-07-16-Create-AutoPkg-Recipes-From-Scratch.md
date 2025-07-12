---
published: false
category: Other
---

## Setup:

Use a Mac, Windows, or Linux system. (Ubuntu specifically is well tested, but other distros should work)

Install AutoPkg or clone repo and run it using python directly.

Run: `autopkg repo-add https://github.com/jgstew/jgstew-recipes.git`

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
Identifier: com.github.macadmins.download.Firefox-Mac
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
Identifier: com.github.macadmins.download.Firefox-Mac
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
Identifier: com.github.macadmins.download.Firefox-Win
Input:
  NAME: Firefox-Win
  os: win64
  filename: FirefoxSetup.exe
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.download.Firefox-Mac
```

Run this and see the different output.

`ParentRecipe: com.github.macadmins.Firefox-Mac` means that this recipe will run first, but using the items in the `Input` area of our `com.github.macadmins.Firefox-Win` recipe.

Then we can do the same, but for Linux: Firefox-Linux.download.recipe.yaml

```
---
Description: download Firefox for Linux
Identifier: com.github.macadmins.download.Firefox-Linux
Input:
  NAME: Firefox-Linux
  os: linux64
  filename: firefox.tar.xz
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=osx&lang=en-US
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=win64&lang=en-US
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.download.Firefox-Mac
```


## Example: Firefox MacOS Homebrew Recipe

Now that we have a working download recipe for FireFox for MacOS, we need to create a recipe to "package" it for a distribution tool.

For this example, we are going to make a homebrew cask, which is just a ruby file with a specific format.

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

`brew install --cask --verbose firefox.rb`

We can turn this into a template by making a copy, renaming it to `firefox.template.rb` and changing the following:

`version "127.0.2"` to `version "{{version}}"`

`sha256 "af516f0222361a311e83de8ca9a27a99653b2c0a00a6653e25ab59046a44d128"` to `sha256 "{{file_sha256}}"`

Now make a cask recipe that will use this template: `Firefox-Mac.cask.recipe.yaml`

```
---
Description: Creates an homebrew cask for the latest version of Firefox
Identifier: com.github.macadmins.cask.Firefox-Mac
Input:
  NAME: "Firefox"
  OS: osx
  filename: Firefox.dmg
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.download.Firefox-Mac
Process:
  # this is not actually BigFix specific, just sets up some defaults in the template dictionary:
  - Processor: com.github.jgstew.SharedProcessors/BigFixSetupTemplateDictionary

  # this generates the homebrew cask from the template
  - Processor: com.github.jgstew.SharedProcessors/ContentFromTemplate
    Arguments:
      template_file_path: "%RECIPE_DIR%/firefox.template.rb"
      content_file_pathname: "%RECIPE_CACHE_DIR%/firefox.rb"
```

Run this recipe, and it will generate the firefox homebrew cask.

`autopkg run -vv Firefox/Firefox-Mac.cask.recipe.yaml`

The generated item should be in a location like: (varies by OS)

`/Users/_USER_/Library/AutoPkg/Cache/com.github.macadmins.cask.Firefox-Mac/firefox.rb`

Can test this generated cask on a MacOS test machine:

`brew install --cask /Users/_USER_/Library/AutoPkg/Cache/com.github.macadmins.cask.Firefox-Mac/firefox.rb`

From here, AutoPkg can import this into your preferred management tool, you can test it, and run on a target systems.

## Example: Firefox Linux Script Recipe

Now a similar example for Linux, but this time using a bash script to install firefox.

Create a bash script to install FireFox on Linux, based upon the Mozilla documentation: `firefox-install-linux.example.sh`

```
#!/bin/bash
# URL of the file to download
url="https://download-installer.cdn.mozilla.net/pub/firefox/releases/137.0/linux-x86_64/en-US/firefox-137.0.tar.xz"

# Expected SHA-256 hash of the file
expected_sha256="4d2d0a64a11f8aab7a1be583e1e4cddfaf2671967212b369a87489f3c11c3ac9"

# Temporary file to store downloaded content
download_file_path=/tmp/firefox.tar.xz

# install prereqs if missing (docker)
if command -v apt &> /dev/null; then
    apt install -y curl bzip2 xz-utils
fi

# Download the file using curl
curl -sSL "$url" -o "$download_file_path"

# Calculate the SHA-256 hash of the downloaded file
actual_sha256=$(sha256sum "$download_file_path" | awk '{print $1}')

# Compare the calculated hash with the expected hash
if [ "$actual_sha256" == "$expected_sha256" ]; then
    echo "File downloaded successfully and hash matched: $actual_sha256"
    echo "Installing"
    # https://support.mozilla.org/en-US/kb/install-firefox-linux
    cd /tmp
    # tweak to handle .tar.xz files
    tar xJf $download_file_path
    rm -rf /opt/firefox
    mv firefox /opt
    rm -f /usr/local/bin/firefox
    ln -s /opt/firefox/firefox /usr/local/bin/firefox
    mkdir -p /usr/local/share/applications
    cat <<ENDOFTOKEN > /usr/local/share/applications/firefox.desktop
[Desktop Entry]
Version=1.0
Name=Firefox Web Browser
Comment=Browse the World Wide Web
GenericName=Web Browser
Keywords=Internet;WWW;Browser;Web;Explorer
Exec=firefox %u
Terminal=false
X-MultipleArgs=false
Type=Application
Icon=/opt/firefox/browser/chrome/icons/default/default128.png
Categories=GNOME;GTK;Network;WebBrowser;
MimeType=text/html;text/xml;application/xhtml+xml;application/xml;application/rss+xml;application/rdf+xml;image/gif;image/jpeg;image/png;x-scheme-handler/http;x-scheme-handler/https;x-scheme-handler/ftp;x-scheme-handler/chrome;video/webm;application/x-xpinstall;
StartupNotify=true
ENDOFTOKEN
    echo "FireFox installed!"
else
    echo "Hash verification failed! Expected: $expected_sha256, Actual: $actual_sha256"
fi
```

We can turn this into a template by making a copy, renaming it to `firefox-install-linux.template.sh` and changing the following:

`url="https://download-installer.cdn.mozilla.net/pub/firefox/releases/137.0/linux-x86_64/en-US/firefox-137.0.tar.xz"` to `url="{{download_url}}"`

`expected_sha256="4d2d0a64a11f8aab7a1be583e1e4cddfaf2671967212b369a87489f3c11c3ac9"` to `expected_sha256="{{file_sha256}}"`

Now make an installscript recipe that will use this template: 

### Firefox-Linux.installscript.recipe.yaml

```
---
Description: Creates an install script for the latest version of Firefox
Identifier: com.github.macadmins.installscript.Firefox-Linux
Input:
  NAME: Firefox-Linux
  OS: linux64
  filename: firefox.tar.xz
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.download.Firefox-Linux
Process:
  # this is not actually BigFix specific, just sets up some defaults in the template dictionary:
  - Processor: com.github.jgstew.SharedProcessors/BigFixSetupTemplateDictionary

  # this generates the install script from the template
  - Processor: com.github.jgstew.SharedProcessors/ContentFromTemplate
    Arguments:
      template_file_path: "%RECIPE_DIR%/firefox-install-linux.template.sh"
      content_file_pathname: "%RECIPE_CACHE_DIR%/install-firefox-linux.sh"
```

Run this recipe, and it will generate the firefox install script.

`autopkg run -vv Firefox/Firefox-Linux.installscript.recipe.yaml`

The generated item should be in a location like: (varies by OS)

`/Users/_USER_/Library/AutoPkg/Cache/com.github.macadmins.installscript.Firefox-Linux/install-firefox-linux.sh`

Can then test this script on a linux test machine: (or docker container)

`bash install-firefox-linux.sh`

From here, AutoPkg can import this into your preferred management tool, you can test it, and run on a target systems.


## Example: Firefox Windows Chocolatey Recipe

Now that we have a working download recipe for FireFox for Windows, we need to create a recipe to "package" it for a distribution tool.

For this example, we are going to make a chocolatey package, which is really just a zip file with specific files in it.

We are going to start with a working example then turn it into a template so that we can automate the creation of it using AutoPkg.

In this case we are going to bundle the Firefox download into the chocolatey package itself, so then this can be deployed to systems that do not have an internet connection.

Here is a working example that installs an outdated version of FireFox:

### chocolateyInstall.ps1

```
$ErrorActionPreference = 'Stop'
$toolsDir = "$(Split-Path -Parent $MyInvocation.MyCommand.Definition)"
$file = Join-Path $toolsDir 'FirefoxSetup.exe'
$packageArgs = @{
  packageName = 'Firefox'
  fileType = 'exe'
  silentArgs = '/S'
  file = $file
}

Install-ChocolateyInstallPackage @packageArgs
```

Turn this into a template by changing `'FirefoxSetup.exe'` into `'{{file_name}}'`

Rename it to `Firefox-Win.ChocolateyTemplate.chocolateyInstall.ps1`


### Firefox.nuspec

```
<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://schemas.microsoft.com/packaging/2010/07/nuspec.xsd">
  <metadata>
    <id>Firefox</id>
    <version>127.0.2</version>
    <title>Firefox</title>
    <authors>Mozilla</authors>
    <requireLicenseAcceptance>false</requireLicenseAcceptance>
    <description>Firefox web browser.</description>
  </metadata>
</package>
```

Turn this into a template by changing `<version>127.0.2</version>` into `<version>{{version}}</version>`

Rename it to `Firefox-Win.ChocolateyTemplate.Firefox.nuspec`

Create a recipe to create the chocolatey package from the templates:

### Firefox-Win.ChocolateyTemplate.recipe.yaml

```
---
Description: Creates an choco package for the latest version of Firefox
Identifier: com.github.macadmins.ChocolateyTemplate.Firefox-Win64
Input:
  NAME: "Firefox"
  OS: win64
  filename: FirefoxSetup.exe
  # https://download.mozilla.org/?product=firefox-latest-ssl&os=linux64&lang=en-US
  # https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US
MinimumVersion: "2.3"
ParentRecipe: com.github.macadmins.download.Firefox-Win
Process:
  # this is not actually BigFix specific, just sets up some defaults in the template dictionary:
  - Processor: com.github.jgstew.SharedProcessors/BigFixSetupTemplateDictionary

  # create missing folders:
  - Processor: com.github.jgstew.SharedProcessors/FileTouch
    Arguments:
      pathname: "%RECIPE_CACHE_DIR%/tmp/tools/chocolateyInstall.ps1"
      touch_create_folders: True

  # create Firefox.nuspec from template
  - Processor: com.github.jgstew.SharedProcessors/ContentFromTemplate
    Arguments:
      template_file_path: "%RECIPE_DIR%/Firefox-Win.ChocolateyTemplate.Firefox.nuspec"
      content_file_pathname: "%RECIPE_CACHE_DIR%/tmp/Firefox.nuspec"

  # create chocolateyInstall.ps1 from template
  # https://docs.chocolatey.org/en-us/create/create-packages/
  # https://docs.chocolatey.org/en-us/create/functions/install-chocolateypackage/
  - Processor: com.github.jgstew.SharedProcessors/ContentFromTemplate
    Arguments:
      template_file_path: "%RECIPE_DIR%/Firefox-Win.ChocolateyTemplate.chocolateyInstall.ps1"
      content_file_pathname: "%RECIPE_CACHE_DIR%/tmp/tools/chocolateyInstall.ps1"

  # copy FirefoxSetup.exe into tmp directory for creation of nupkg
  - Processor: com.github.jgstew.SharedProcessors/FileCopyNewest
    Arguments:
      file_path_first: "%RECIPE_CACHE_DIR%/downloads/FirefoxSetup.exe"
      file_path_second: "%RECIPE_CACHE_DIR%/tmp/tools/FirefoxSetup.exe"

  # create zip file Firefox.nupkg
  - Processor: com.github.jgstew.SharedProcessors/SevenZip
    Arguments:
      sevenzip_args: ["a", "-tzip", "../firefox.nupkg", "*"]
      # need to change the relative directory to NOT include the directory name
      relative_directory: tmp
```

Run this recipe, and it will generate the firefox chocolatey package.

`autopkg run -vv Firefox/Firefox-Win.ChocolateyTemplate.recipe.yaml`

The generated item should be in a location like: (varies by OS)

`/Users/_User_/Library/AutoPkg/Cache/com.github.macadmins.ChocolateyTemplate.Firefox-Win64/firefox.nupkg`

Can test this generated chocolatey package on a Windows test machine:

`choco install firefox -s "$env:USERPROFILE\Library\AutoPkg\Cache\com.github.macadmins.ChocolateyTemplate.Firefox-Win64\" --pre --no-progress --yes --force --verbose`

From here, AutoPkg can import this into your preferred management tool, you can test it, and run on a target systems.
