
### Objective:

* Edit and Debug a BigFix Console Dashboard
    * Steps 4 through 8

### Prerequisites:

1. [Open BigFix Console Presentation Debugger](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md)

### Steps:

1. Create Empty Temp Folder 
    * Example: `_tmp_Dashboard`
    * **NOTE:** The console will copy all of the files in the folder!
    * ![Create Empty Temp Folder](/images/BigFix/Dashboards/CreateEmptyFolder.png)
1. Put Dashboard Files in Folder
    * Example: [HelloWorld_template.ojo](https://raw.githubusercontent.com/jgstew/bigfix-content/master/dashboards/HelloWorld_template.ojo)
    * ![Put Dashboard Files in Folder](/images/BigFix/Dashboards/PutDashboardFilesInFolder.png)
1. Open the Debug Menu
    * ![Open Debug Menu](/images/BigFix/Console/OpenDebugMenu.png)
    * If missing, See here on how to enable the Debug Menu: 
        * [Open The BigFix Console Presentation Debugger](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md)
1. Select "Load Wizard..."
    * Note: Wizards and Dashboards are [basically the same](https://github.com/jgstew/bigfix-content/blob/master/dashboards/README.md)
    * ![Select Load Wizard](/images/BigFix/Dashboards/SelectLoadWizard.png)
1. Load Dashboard into Console
    * Navigate into temp folder ( `_tmp_Dashboard` )
    * Select the OJO file
    * Click Open
    * ![Load Dashboard](/images/BigFix/Dashboards/LoadDashboardInConsole.png)
1. View the Dashboard:
    * ![View Dashboard](/images/BigFix/Dashboards/ViewDashboardHW.png)
    * Should load automatically
    * If not, check under [Dashboards -> All Dashboards](/images/BigFix/Dashboards/DashboardLocationCustom.png)
1. Reload the Dashboard
    * Right Click
    * Select "Reload"
        * Alternatively press Ctrl+F5 keys
    * ![Reload Dashboard](/images/BigFix/Dashboards/ReloadDashboard.png)
    * Notice the time displayed updates
    * Reload again as needed (like when editing the OJO file)
1. Edit the OJO file
    * Open `\_tmp_Dashboard\HelloWorld_template.ojo` in [Visual Studio Code](https://code.visualstudio.com/) or similar editor
    * Make a minor change to the OJO file
        * Change [Line 17](https://github.com/jgstew/bigfix-content/blob/master/dashboards/HelloWorld_template.ojo#L17) to `<h2>Hello World!!!</h2>`
    * Save the file ( Ctrl + S )
    * Reload the Dashboard to see the changes
1. View Source from Console
    * Right Click
    * Select "View Source"
    * ![Select View Source](/images/BigFix/Dashboards/DashboardViewSource.png)
1. Compare the "Rendered" Source in Notepad to the OJO file
    * Notice that `<h2>Hello World!!!</h2>` is the same in both ( [Line 8](https://github.com/jgstew/bigfix-content/blob/master/dashboards/about_blank%5B1%5D.html#L8) vs [Line 17](https://github.com/jgstew/bigfix-content/blob/master/dashboards/HelloWorld_template.ojo#L17) )
    * Compare [Line 10](https://github.com/jgstew/bigfix-content/blob/master/dashboards/about_blank%5B1%5D.html#L10) in Notepad to [Line 19](https://github.com/jgstew/bigfix-content/blob/master/dashboards/HelloWorld_template.ojo#L19) in the OJO file
        * OJO file: `<?Relevance ps of concatenations of ("There are ";it as string;" registered computers right now [ "; now as string; " ]") of number of bes computers ?>`
        * Rendered HTML: `<p>There are 1 registered computers right now [ Sun, 28 Oct 2018 21:16:09 -0700 ]</p>`
        * Dashboard Text: `There are 1 registered computers right now [ Sun, 28 Oct 2018 21:16:09 -0700 ]`
    * ![Compare Rendered Source](/images/BigFix/Dashboards/CompareRenderedSourceNotepad.png)
1. Edit the `HelloWorld_template.ojo` file further
    * **Example:** Edit [Line 19](https://github.com/jgstew/bigfix-content/blob/master/dashboards/HelloWorld_template.ojo#L19) to [change the session relevance](https://gist.github.com/jgstew/89e024871105b60b225f53a4c3cb6a09/revisions#diff-b4bb108e538d0d33c410c803c12a7349) to the following:
        * `ps of concatenations of ("There are ";it as string;" tasks right now [ "; now as string; " ]") of number of bes tasks`
    * Try some other changes on your own.

### Next:

* [Debug BigFix Dashboard In Visual Studio](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-11-27-Debug-BigFix-Dashboard-In-Visual-Studio.md)
* [Edit DataTables Console Dashboard](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Edit-DataTables-Console-Dashboard.md)
