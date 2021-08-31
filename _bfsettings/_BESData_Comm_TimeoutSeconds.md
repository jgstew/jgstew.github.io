
Default: 10 seconds (10)

Recommendation: 60 seconds (60) or more

Applicability: Root Server Only (exists main gather service)

The default timeout for communication with the BigFix Console and root server is too low which can cause the console to retry over and over again, never actually completing successfully. 

If this is causing issues, then you should see HTTP 28 errors in the Console. Also check BESRelay.log for HTTP 28 errors.

Often times there will be a single time where a large query needs to complete, but then after that each subsequent query is smaller. The one time larger query can become longer over time with more endpoints, patches, etc...

- http://www-01.ibm.com/support/docview.wss?uid=swg21645679
- https://bigfix.me/fixlet/details/3959
- https://forum.bigfix.com/t/console-not-accepting-actions/22220/6
