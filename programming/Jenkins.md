# Jenkins

### Feature

* Building/testing software projects continuously
* Monitoring executions of externally-run jobs

### Install
[official website](http://jenkins-ci.org/)

1. Download windows installer and install as usual.
2. In the install directory, run `java -jar jenkins.war`, and view the manager page at localhost:8080
3. If the port of default 8080 is conflict with other application, jetty can not start normally. So run `java -jar jenkins.war --httpPort=8980` which using 8980 as bind port.

For windows installer, it will install a windows service called `Jenkins`，the service is start when computer is startup. We can modify the **jenkins.xml** in the intall directory to change the default config of the service. This service use the intalled path as the %JENKINS_HOME%.

There are some instructions about the service in **jenkins.xml**:
* `jenkins.exe stop` to stop the service
* `jenkins.exe uninstall` to uninstall the service.

It's more freely to run a bat file start the user defined service. Such as change the %JENKINS_HOME%. I dont't like run the service in the intaller path or my home directory. 
```
set JENKINS_HOME=E:\Jenkins
cd /d %JENKINS_HOME%
rem copy the jenkins.war to %JENKINS_HOME%
java -jar %JENKINS_HOME%\jenkins.war --httpPort=8980
```

### Add New Job

One porject continuous integration called a Job. The new jobs are lie in `%JENKINS_HOME%\job\`

* Set %WORKSPACE%:
Advanced Project Options -> Use custom workspace, Input the path for the root path of the Job.

* VC project bulid
Build->Execute Windows batch command:
```
"D:\Program Files (x86)\Microsoft Visual Studio 12.0\Common7\IDE\devenv.com" "%WORKSPACE%\proj.win32\PopClear.sln" /Build "Debug|Win32"
```

* Path the application after build  
Add another `Execute Windows batch command` and input the .bat file need to run.

```
del release\PopClear.exe

copy ..\Resources\*.png release\
copy Debug.win32\PopClear.exe release\

rem 7z a -tzip %date:~0,10%_%time:~0,2%%time:~3,2%%time:~6,2%_release.zip .\release\*

7z a -tzip %date:~0,10%_release.zip .\release\*
```
* Post-build Actions
Jenkins could archive the build after build.
Below the option Archive the arififacts, type \*.zip in the Files to archive field. So it will copy the \*.zip file to the build path, and show it in the job's home page.


### Plugin

There are two ways to install a plugin for Jenkins:

* **Manually offline**: Download plugin file *.hpi, put it into `%JENKINS_HOME%\plugins\` (Not in the install path)
* **Automatically online**: At the the manage page, select which plugin you want, in this way the system will install the dependence plugin automatically. Manage Jenkins->Manage Plugins


### CppCheck

* Download the installer and install on windows
* Add the cppcheck.exe to system %PATH%
* run gui or command to check .cpp files

`cppcheck --platform=win32W --enable=all --suppress=missingInclude ../Classes/. --xml 2> project_codeanalysis.xml`

win32W: windows 32 bit Unicode  
--enable=all: check level, which means check all the aspects.  
--suppress=missingInclude: disable the check with id `missingInclude`, otherwise it will check all the header files could be found  
../Classes/.: the directory which code are in  
--xml 2> project_codeanalysis.xml: output the result to version2 xml file named project_codeanalysis.xml   

