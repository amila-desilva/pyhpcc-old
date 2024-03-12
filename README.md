# PyHPCC

## Overview
This repository houses a Python package, PyHPCC, to interact with HPCC Systems using the web services exposed by the HPCC platform.


## Pre-Requisites
1. Python preferably version 3.x. 
   <br>**NOTE**: On a Windows machine, ensure the path to Python is added to the System Environment Variables. Follow [this YouTube video](https://www.youtube.com/watch?v=Y2q_b4ugPWk) for instructions on how to add Python to Environment Variables.
2. Install ECL Client Tools


## Installation
Before installing PyHPCC, ensure you have ECL client tools installed on your machine. The method for installing client tools varies on Windows and Linux systems.


### Windows
#### <span style="color:aqua">ADDING ECL CLIENT TOOLS TO SYSTEM ENVIRONMENT VARIABLES</span>
Installing ECL IDE on a Windows machine installs ECL Client Tools by default--it need not be installed separately. The path to the Client Tools need to be added to the Windows Environment Variables:
  1. On the Windows search bar, type <em>environment variables</em> and select <em>Edit the system environment variables</em>.
  2. In the resulting window, click the <em>Environment Variables...</em> button at the bottom.
  3. Under the <em>System variables</em> block, double-click on the <em>Path</em> variable.
  4. Add the Client Tools path to the list under the Path variable. The path looks something like this: `C:\Program Files\HPCCSystems\8.4.10\clienttools\bin` . 
  5. Open a Command Prompt window, and type `ecl --version` to test if ECL Client Tools are accessible thru command line.
   <br>**NOTE**: if you had a Command Prompt or VS Code window open while editting the Environment Variables, you will have to re-open the window to allow the new changes to be picked up.

#### <span style="color:aqua">PyHPCC INSTALLATION</span>
1. The easiest way to install the latest version is by downloading the latest PyHPCC <em>.tar.gz</em> package from the <em>package</em> folder on this Git repository onto your machine. 
2. Open a Command Prompt window, and navigate to the folder containing the PyHPCC <em>.tar.gz</em> package. Then, run `pip install pyhpcc-<downloaded-version>.tar.gz` command on your Command Prompt.


### Linux
#### <span style="color:aqua">ADDING ECL CLIENT TOOLS TO SYSTEM ENVIRONMENT VARIABLES</span>
The ECL Client Tools needs to be installed separately on Linux machines from the [HPCC System's Download webpage](https://hpccsystems.com/download/archive). Select a version of your choice. 
<br>
**NOTE**: Version 7.4.32 has been tested and used on Ubuntu. Version 6.4.12 has been tested and used on CentOS systems.


#### <span style="color:aqua; font-style:italic">Client Tools Installation on Ubuntu</span>
Download ECL Client Tools 7.4.32 onto the Ubuntu machine. Then, run the following commands on a shell or bash window:

    apt-get update -y
    apt-get -f install


#### <span style="color:aqua; font-style:italic">Client Tools Installation on CentOS</span>
Download ECL Client Tools 6.4.12 onto the CentOS machine. Then, run the following commands on a shell or bash window:

    yum clean all
    rm -rf /var/cache/yum
    yum -y install hpcc_clienttools_6.4.12_centos.rpm


#### <span style="color:aqua">PyHPCC INSTALLATION</span>
1. Download and place the latest PyHPCC <em>.tar.gz</em> package from the <em>package</em> folder on this Git repository onto your Linux machine. 
2. Use a bash or shell window to navigate to the folder containing the PyHPCC <em>.tar.gz</em> package. Then, run `pip install pyhpcc-<downloaded-version>.tar.gz` command.


## Functionality
<span style="color:orange">In Transit</span>


## How to Contribute
<span style="color:orange">In Transit</span>