---
published: false
---

Google Chrome settings can be managed by Local GPO on Windows or similar mechanisms on Mac & Linux.

## Example:

### JSON:

Registry(LocalGPO): `HKEY_LOCAL_MACHINE\SOFTWARE\Policies\Google\Chrome\ManagedBookmarks`

    [{"toplevel_name": "BigFix!"}, {"url": "https://github.com/bigfix", "name": "BigFix GitHub"}, {"url": "https://bigfix.me", "name": "BigFix Me"}, {"url": "https://forum.bigfix.com", "name": "BigFix Forums"}, {"url": "https://developer.bigfix.com/", "name": "BigFix Developer"}, {"url": "https://macadmins.psu.edu/", "name": "PSU MacAdmins Conference"}, {"url": "macadmins.org", "name": "MacAdmins Slack"}]
    
### Plist:

File: `/Library/Managed Preferences/com.google.chrome.plist`


    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>
    <key>ManagedBookmarks</key>
    <array>
      <dict>
        <key>toplevel_name</key>
        <string>BigFix!</string>
      </dict>
      <dict>
        <key>name</key>
        <string>Google</string>
        <key>url</key>
        <string>google.com</string>
      </dict>
      <dict>
        <key>name</key>
        <string>Youtube</string>
        <key>url</key>
        <string>youtube.com</string>
      </dict>
      <dict>
        <key>children</key>
        <array>
          <dict>
            <key>name</key>
            <string>Chromium</string>
            <key>url</key>
            <string>chromium.org</string>
          </dict>
          <dict>
            <key>name</key>
            <string>Chromium Developers</string>
            <key>url</key>
            <string>dev.chromium.org</string>
          </dict>
        </array>
        <key>name</key>
        <string>Chrome links</string>
      </dict>
    </array>
    </dict>
    </plist>
    
### Related:

- chrome://policy/
- https://www.chromium.org/administrators/policy-templates
- https://www.chromium.org/administrators/policy-list-3#ManagedBookmarks
- https://www.jamf.com/jamf-nation/discussions/13947/configuring-google-chrome

