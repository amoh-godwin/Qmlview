# Qmlview
An alternative to qmlscene

# Description
Qmlview is a command line utility. But sort of to replace the non-existent
qmlscene, which was used to preview qml source code before it is loaded
by any C++, Java, or python code.

# Why it came into being
It is supposed to be a somewhat replacement
for the default qmlscene that came with every PyQt installation.
But since PyQt5.10 it hasn't been included in the installation folder.
A way around it used to be to include a copy from the installation
of Qt's official software development bundle found on Qt's official
site Qt.com. But this also fails in PyQ5.11.
So, this is supposed to be a stand-alone qmlscene sort of replacement.

# Install

### Standalone
Standalones are available for download [here](https://github.com/amoh-godwin/Qmlview/releases)

### via PyPI
You can also download via pypi.org
If you have python installed you can do: ```pip install Qmlview```

# Usage
```qmlview path/to/file```
OR
```./qmlview path/to/file```

eg.
```qmlview C:/myproject/button.qml```
OR
```./qmlview C:/myproject/button.qml```

# Error reporting
No errors have been reported since the time of release. 
Therefore report every error at https://github.com/amoh-godwin/Qmlview/issues
Open a new issue and state the error.

# Contribute
Fork this repository and make commits to your fork.
Make a pull request to the development branch.
