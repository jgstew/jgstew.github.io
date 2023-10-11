
There are a few different reasons why you might need to manually cache a file on a BigFix Root Server.

One of them is that the file being downloaded in a prefetch is not available on the public internet directly. The most common case is where a login is required in order to obtain the file. This is most common with certain versions of Oracle JAVA.

Another case is when only the latest version of the software is available from the vendor to download directly, but the version referenced in the prefetch is no longer available. This is most common with Google Chrome.

In any case where the download is not available, you can put the binary in the right place on the root server to solve this issue.

1. ensure the BigFix root server cache is set sufficiently large. (100GB or larger recommended)
1. ensure the BigFix root server has sufficient hard disk space on the volume that contains the wwwrootbes folder. (300GB or larger recommended)
1. rename the binary file to it's sha1 value, which must match the sha1 in the prefetch.
1. place the binary in the root server's wwwrootbes folder
  - On windows, the default location is: `C:\Program Files (x86)\BigFix Enterprise\BES Server\wwwrootbes\bfmirror\downloads\sha1`
  - On Linux, the default location is: `/var/opt/BESServer/wwwrootbes/bfmirror/downloads/sha1`
