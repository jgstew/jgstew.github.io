---
category: Other
---

It is possible to setup Visual Studio Code to use Google Chrome's remote debugging API using a plugin/module.

This really isn't specific to Angular, but that was my use case.

The main advantage to doing this is that it allows you to do the debugging directly in Visual Studio Code, while also capturing the Console output from the very start. It also allows setting breakpoints directly from source files if a sourcemap is used, though this never actually seems to work 100% of the time for some reason, but I had the most success with this method. Setting a breakpoint in the app.js directly might works slightly better sometimes... maybe.

### Steps:

- Install the [`vscode-chrome-debug`](https://github.com/Microsoft/vscode-chrome-debug) module in Visual Studio Code
- Launch Chrome with Remote Debugging enabled
  - `chrome --remote-debugging-port=9222`
  - BigFix Task: [Run Google Chrome with remote debugging enabled - Windows](https://github.com/jgstew/bigfix-content/blob/master/fixlet/Run%20Google%20Chrome%20with%20remote%20debugging%20enabled%20-%20Windows.bes)
- Configure `.vscode\launch.json` in project
  - This will not be exactly the same for every project


### My `.vscode\launch.json` Example

```
{
    "version": "0.2.0",
    "configurations": [
        {
            "type": "chrome",
            "request": "launch",
            "name": "Chrome against localhost",
            "url": "https://localhost:3000",
            "webRoot": "${workspaceRoot}/app/client/public",
            "port": 9222,
            "userDataDir": false,
            "sourceMaps": true
        }
    ]
}
```

### References:
- [https://github.com/Microsoft/vscode-chrome-debug](https://github.com/Microsoft/vscode-chrome-debug)
- [https://code.visualstudio.com/](https://code.visualstudio.com/)
