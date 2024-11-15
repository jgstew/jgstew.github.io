
### Objectives: 
1. Edit and Use a JQuery DataTables Dashboard
    * Steps 1 through 7
    * Optionally Steps 8 & 9
1. View the Dashboard as a Custom Web Report
    * Step 10

### Prerequisites:

1. [Open BigFix Console Presentation Debugger](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md)
1. [Debug a Dashboard In the BigFix Console](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Debug-Dashboard-In-BigFix-Console.md)
1. (recommended) Have the "Patches for Windows (English)" site enabled, gathered, and computers subscribed.

### Steps:
1. Put Dashboard Files in Folder
    * Example: [GenericDataTables.ojo](https://raw.githubusercontent.com/jgstew/bigfix-content/master/dashboards/GenericDataTables.ojo)
    * ![Put Dashboard Files in Folder](/images/BigFix/Dashboards/PutDashboardFilesInFolderDT.png)
1. Open the Debug Menu
    * ![Open Debug Menu](/images/BigFix/Console/OpenDebugMenu.png)
    * If missing, See here on how to enable the Debug Menu: [Open The BigFix Console Presentation Debugger](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-10-29-Open-BigFix-Console-Presentation-Debugger.md)
1. Select "Load Wizard..."
    * Note: Wizards and Dashboards are [basically the same](https://github.com/jgstew/bigfix-content/blob/master/dashboards/README.md)
    * ![Select Load Wizard](/images/BigFix/Dashboards/SelectLoadWizard.png)
1. Load Dashboard into Console
    * Navigate into temp folder ( `_tmp_Dashboard` )
    * Select the OJO file
    * Click Open
    * ![Load Dashboard](/images/BigFix/Dashboards/LoadDashboardInConsoleDT.png)
1. View the Dashboard:
    * ![View Dashboard](/images/BigFix/Dashboards/ViewDashboardDT.png)
    * Should load automatically
    * If not, check under [Dashboards -> All Dashboards](/images/BigFix/Dashboards/DashboardLocationCustom.png)
1. Try Searches in the Dashboard
    * Example: `block ie x64 2008 r2 sp1`
    * ![Search Dashboard](/images/BigFix/Dashboards/DashboardSearchDT.png)
1. Edit the `GenericDataTables.ojo` file
    * Open `GenericDataTables.ojo` in [Visual Studio Code](https://code.visualstudio.com/) or similar editor
    * Edit [Line 30](https://github.com/jgstew/bigfix-content/blob/master/dashboards/GenericDataTables.ojo#L30) changing `bes tasks` to `bes computers`
        * `'( html concatenations of tds of (name of it; id of it as string) ) of bes computers'`
    * Save the file ( Ctrl + S )
    * Reload the Dashboard to see the changes
    * ![Reload Dashboard](/images/BigFix/Dashboards/ReloadDashboardDT.png)
1. Edit the `GenericDataTables.ojo` file further
    * Edit [Line 30](https://github.com/jgstew/bigfix-content/blob/master/dashboards/GenericDataTables.ojo#L30) to add `operating systems`
         * `'( html concatenations of tds of (name of it; id of it as string; operating systems of it) ) of bes computers'`
    * Save the file ( Ctrl + S )
    * Reload the Dashboard to see the changes
1. Experiment with other changes
    * [cpus of bes computers](https://developer.bigfix.com/relevance/reference/bes-computer.html#cpu-of-bes-computer-string)
    * [device types of bes computers](https://developer.bigfix.com/relevance/reference/bes-computer.html#device-type-of-bes-computer-string)
    * ![Experiment Dashboard](/images/BigFix/Dashboards/ViewExperimentDashboardDT.png)
1. Copy the Dashboard `<HTML>` into a Web Report
    * Copy [Lines 18 through 67](https://github.com/jgstew/bigfix-content/blob/master/webreports/GenericDataTables.besrpt#L18) from the `GenericDataTables.ojo`
    * Open Web Reports
        * [https://localhost:8083/webreports?page=CustomReport](https://localhost:8083/webreports?page=CustomReport)
            * `localhost` will need to be set to the FQDN or IP of your web reports server
            * `8083` will need to be set to the port of your web reports server
    * Paste [Lines 18 through 67](https://github.com/jgstew/bigfix-content/blob/master/webreports/GenericDataTables.besrpt#L18) into the Custom Web Report
    * ![Paste Source](/images/BigFix/Dashboards/PasteDashboardIntoWebReport.png)
    * Scroll Down and Click the `Preview` button on the far right
    * ![Web Reports Preview Button](/images/BigFix/Dashboards/WebReportsCustomPreviewButton.png)
    * Scroll Up and Click the `Hide Source` link on the top left
        * This will show what the Custom Web Report will look like normally
    * View the Web Report
        * Experiment and Compare the Functionality to the Dashboard
    * ![View Web Report](/images/BigFix/Dashboards/WebReportsCustomView.png)


### Next:

* [Debug BigFix Dashboard In Visual Studio](https://github.com/jgstew/jgstew.github.io/blob/master/_posts/2018-11-27-Debug-BigFix-Dashboard-In-Visual-Studio.md)


### Related:

* [Intro to BigFix Dashboards Presentation](https://docs.google.com/presentation/d/1pg_j-9MM9-7rnF_l_8uhMG4ZiJxPW37cB8TVpd7Qmdk/edit?usp=sharing)
* https://github.com/jgstew/bigfix-content/blob/master/dashboards/Computer_Filter_Search.ojo
