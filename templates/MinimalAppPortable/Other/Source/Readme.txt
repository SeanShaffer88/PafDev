AppName Portable Launcher
=========================

This package's launcher is the PortableApps.com Launcher. It is released
under the GNU General Public License (GPL). The launcher, with full
source code and documentation, is available from:

    https://portableapps.com/development

The PortableApps.com Installer used to build this package is also
released under the GPL and is available from the same page.

The base application's source code (if applicable) is available from the
application's homepage, listed in help.html and in
App\AppInfo\appinfo.ini.


USER CONFIGURATION
==================

Some configuration in the PortableApps.com Launcher can be overridden by
the user in an INI file next to AppNamePortable.exe called
AppNamePortable.ini. If you are happy with the default options, this file
is not necessary. An example INI is included in this directory to get
you started. To use it, copy AppNamePortable.ini from this directory to
AppNamePortable.ini next to AppNamePortable.exe (the package root). The
options in the INI file are as follows:

    AdditionalParameters=
    DisableSplashScreen=false
    RunLocally=false

There may be other values also permitted in the user configuration file
by this portable application; refer to help.html for any details of them.
