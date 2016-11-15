
**This is the final result:** https://bigfix.me/fixlet/details/22625

This post will walk through the steps I take to create a fixlet/task to install a new piece of software using BigFix. This will be with the specific case of Visual Studio Code for Windows.

### Step 1: Download

Visit the vendor site: https://code.visualstudio.com/

Click the `Download for Windows` button.

The software will start to download in the browser after a few seconds. In this case, the file is `VSCodeSetup-1.7.1.exe`

Go to the browser `downloads` section to find the actual download URL.

<img src="/uploads/default/original/2X/6/66a42e0e39f2c903238de5c3aee8660a19e24241.PNG" width="636" height="157">

In this case, the URL is `https://az764295.vo.msecnd.net/stable/02611b40b24c9df2726ad8b33f5ef5f67ac30b44/VSCodeSetup-1.7.1.exe`

Copy the URL into the clipboard

### Step 2: VirusTotal

Sign in to VirusTotal

Go to the home page, click the `URL` tab

Paste the Download URL into the `URL` tab where it says `Enter URL`

<img src="/uploads/default/original/2X/e/e4a8d15157496f97a919553cf4ee406ccdcc3131.PNG" width="547" height="197">

Click the `Scan it!` button

Go to the Analysis page: https://www.virustotal.com/en/url/ae6c705ae42d49dae10df490fab56d1ccb34835025c7d88f8db40247208f4466/analysis/

Click the `Go to downloaded file analysis` link. (this only works for files under a certain size)

In this case, you should end up here: https://www.virustotal.com/en/file/4f1a406321af2f90d16e5b753529d205e66d4f6eeaa5f925566c43b8f8e70638/analysis/1478216605/

### Step 3: Determine Installer Type

From the [VirusTotal analysis page](https://www.virustotal.com/en/file/4f1a406321af2f90d16e5b753529d205e66d4f6eeaa5f925566c43b8f8e70638/analysis/1478216605/), look for signs of the installer type, primarily under the `File detail` tab, but also the `Additional Information` tab.

Found "`This installation was built with Inno Setup.`" in the `File detail` tab, as well as "`INNO, maxorder, appended, packed`" which point to this being an `Inno Setup` installer type. The installer type is needed to determine what [command line switches](http://www.jrsoftware.org/ishelp/index.php?topic=setupcmdline) are needed to silently install the software.

### Step 4:

_(work in progress)_
