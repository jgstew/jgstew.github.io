---
topicId: 15750
---

I'd like to document how to take a never booted OS image and have it applied to a system and have the BigFix agent installed all in one go, the idea being that BigFix would be the primary mechanism for software installation, configuration, and in some cases, drivers. This would be for Mac, Windows, and potentially linux.

I'd like to document the minimum effort to do this with the minimum amount of tools required.

## Requirements:
- Network
 - drivers (if applicable)
 - assume DHCP for simplicity at first
- An Admin User Account
 - need a way to login to troubleshoot
- BES Client
 - masthead / actionsite file
 - potentially a `clientsettings.cfg` or similar.
 - Client installer
 - a way to have the client be installed after the OS is installed
- Create installation media

## Windows
- [Windows ADK(AIK)](https://en.wikipedia.org/wiki/Windows_Assessment_and_Deployment_Kit) or [MDT](https://en.wikipedia.org/wiki/Microsoft_Deployment_Toolkit)
- **Network Drivers** (not required in all cases)
 - [Intel](https://downloadcenter.intel.com/download/25016/Network-Adapter-Driver-for-Windows-10)
 - [Realtek](http://www.realtek.com.tw/downloads/downloadsView.aspx?Langid=1&PNid=13&PFid=5&Level=5&Conn=4&DownTypeID=3&GetDown=false)
 - USB to Ethernet
    - [AX88178](http://www.asix.com.tw/products.php?op=pItemdetail&PItemID=134;71;100&PLine=71) & [AX88179](http://www.asix.com.tw/products.php?op=pItemdetail&PItemID=131;71;112&PLine=71)
    - [AX88772](http://www.asix.com.tw/products.php?op=pItemdetail&PItemID=86;71;101&PLine=71)
 - ???
- create bootable installation media
 - USB
 - ISO
    - `oscdimg -m -h -u2 -udfver102 -bC:\temp\WADK_Win10\boot\etfsboot.com C:\temp\WADK_Win10 C:\temp\win10bigfix.iso`
 - PXE

## Mac
- [AutoDMG](https://github.com/MagerValp/AutoDMG) ( Others? )
 - https://forum.bigfix.com/t/installing-the-bigfix-client-with-autodmg/15427

## Linux
- ???
 - target CentOS and Ubuntu initially
