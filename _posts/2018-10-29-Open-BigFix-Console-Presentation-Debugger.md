
### Objective: 

* Open the Presentation Debugger from the BigFix Console Debug Menu
* Evaulate a Session Relevance Query in the BigFix Console Presentation Debugger

### Steps:

1. Open the BigFix Console
1. Login to the BigFix Console
1. Open the Debug Dialog 
    * Press Ctrl+Shift+Alt+D 
    * ![Debug Dialog](/images/BigFix/Console/DebugDialog.png)
1. Check the "Show Debug Menu" Checkbox
    * ![Show Debug Menu](/images/BigFix/Console/ShowDebugMenuCheckbox.png)
1. Close Debug Dialog
    * ![Close Debug Dialog](/images/BigFix/Console/ShowDebugMenuCheckedClose.png)
1. Open the Debug Menu
    * ![Open Debug Menu](/images/BigFix/Console/OpenDebugMenu.png)
1. Open the Presentation Debugger
    * ![Open Presentation Debugger](/images/BigFix/Console/OpenPresentationDebugger.png)
1. Evaulate a Session Relevance Query
    * `number of bes tasks`
    * `ps of concatenations of ("There are ";it as string;" registered computers right now [ "; now as string; " ]") of number of bes computers`
    * ![Open Presentation Debugger](/images/BigFix/Console/PresentationDebuggerEvaluate.png)

### BONUS: REST API Session Relevance Example:

1. Use the same query as above in the BigFix REST API as a URL Encoded string
    * <img src="/images/posts/BigFix-Debugging-REST-API-Example.PNG" alt="REST API Session Relevance Example" style="max-width:350px;"/>

### Next: 

* [Debug A Dashboard In The BigFix Console](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Debug-Dashboard-In-BigFix-Console.md)

### Related:

- https://developer.bigfix.com/tools/presentation_debugger.html
- https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md
- http://www.jgstew.com/bigfix/2018/10/29/Open-BigFix-Console-Presentation-Debugger.html
- https://forum.bigfix.com/t/open-the-bigfix-console-presentation-debugger/27768
