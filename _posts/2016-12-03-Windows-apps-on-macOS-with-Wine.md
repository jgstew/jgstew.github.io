### Example: FixletDebugger on OSX using WineBottler
- https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2015-03-17-FixletDebugger-on-OSX-using-WineBottler.md
- https://forum.bigfix.com/t/fixletdebugger-on-osx-using-winebottler/12778

# Work in progress

- https://www.winehq.org/wwn/384#Wine64%20on%20OS%20X
- http://portingteam.com/topic/10450-macwine-64bit-news/
- http://www.wine-reviews.net/2016/04/run-64bit-wine-197-on-your-mac-osx.html
- http://www.wine-reviews.net/2016/04/experimental-64-bit-wine-os-x-packages.html
- https://www.playonmac.com/en/
- http://wineskin.urgesoftware.com/tiki-index.php
- http://winebottler.kronenberg.org/
- https://www.codeweavers.com/support/wiki/64bit_Support
- https://mike.kronenberg.org/winebottler-1-5-30-now-with-codesigning-support/
- https://www.ibm.com/developerworks/community/wikis/home?lang=en#!/wiki/Tivoli%20Endpoint%20Manager/page/Utilities

--------------

Trying to run http://software.bigfix.com/download/bes/95/util/CLI9.5.4.38.zip in wine gave the error:
- unimplemented function KERNEL32.dll.GetCurrentConsoleFontEx
- seems to be fixed in 1.8.3 : https://www.winehq.org/announce/1.8.3
