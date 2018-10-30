
### Objective: Edit and Use a JQuery DataTables Dashboard

1. Put Dashboard Files in Folder
    * Example: [GenericDataTables.ojo](https://raw.githubusercontent.com/jgstew/bigfix-content/master/dashboards/GenericDataTables.ojo)
    * ![Put Dashboard Files in Folder](/images/BigFix/Dashboards/PutDashboardFilesInFolderDT.png)
1. Open the Debug Menu
    * ![Open Debug Menu](/images/BigFix/Console/OpenDebugMenu.png)
    * If missing, See here on how to enable the Debug Menu: [Open The BigFix Console Presentation Debugger](2018-10-28-Open-BigFix-Console-Presentation-Debugger.md)
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
