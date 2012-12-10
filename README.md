stocktotal
==========

--------------------------------------------------------------------------------

Introduction
------------

stocktotal project contains two modules: source module and report module.
Source module is used to source Taiwan stock information.
Report module is used to generate analysis report.

Environment
-----------

The development platform is Windows.  The author had ported to Mac but didn't test yet.
 
1.   Database: PostgreSQL 9.2 (or higher).
2.   [Python 3.2](http://www.python.org/) (or higher) environment.  Do not use Python 2.x.
3.   Java running environment.
4.   [Apache Ant](http://ant.apache.org/) building environment.

Prerequirement
--------------

For source module:
1.   [lxml](http://lxml.de/): Processing HTML in the Python language.
2.   [py-postgresql](http://pypi.python.org/pypi/py-postgresql): PostgreSQL driver and tools library
3.   [7-Zip](http://www.7-zip.org/): file archiver in Windows
4.   xlrd: extract data from Microsoft Excel.  To use xlrd in Python 3, may use [takluyver-xlrd](https://github.com/takluyver/xlrd/zipball/py3)
5.   [wget](http://users.ugent.be/~bpuype/wget/): wget in Windows

For report module, need to prepare the following required jar files:
1.   [JasperReports library](http://community.jaspersoft.com/project/jasperreports-library): please check `$HOME_DIR/report/core/build.xml` for details
2.   KAIU Font: Use iReport 4.x to build into a jar file, say `font-kaiu.jar`
3.   [PostgreSQL driver](http://jdbc.postgresql.org/download.html): JDBC 3 
4.   [Apache commons configuration](http://commons.apache.org/configuration/)
5.   [Apache log4j](http://logging.apache.org/log4j/)

Deployment
----------

1.   Create a new role in PostgreSQL: `stocktotal`
2.   Goto your stocktotal project home directory: `$HOME_DIR`
3.   Clone remote stocktotal project: `git clone https://bitbucket.org/Menggen/stocktotal.git`
4.   Put `7z.exe` and `7-zip.dll` in directory `$HOME_DIR/source/core/thirdparty/sevenzip/`
5.   Put `wget.exe` in directory `$HOME_DIR/source/core/thirdparty/wget`
6.   Put all report module required jar files in directory `$HOME_DIR/report/core/lib/`

Executing
---------

1.   Database schema: `$HOME_DIR/db/postgres/pg_dump.sql`.  pgAdmin is your friend.
2.   Source module: execute `$HOME_DIR/source/source_manager.py -h` for usage.  Note that running source module will consume a lot of time.
3.   Report module: we need to build first: `$HOME_DIR/report/builder_manager.py`.  To generate report, execute `$HOME_DIR/report/generator_manager.py -h` for usage.

1.   Go to your project's directory.
2.   Clone this project into your `./vendor/` directory as a `DluBaseUrl` module:  
     `git clone https://bitbucket.org/dlu/dlubaseurl.git ./vendor/DluBaseUrl`
3.   Enable this module in your `./config/application.config.php`.
4.   Copy `dluBaseUrl.local.config.php.dist` config file to your application's `/config/autoload` directory
5.   Rename the config file to `dluBaseUrl.local.config.php`
6.   Edit the config file and enter the correct base URL according to your local deployment as the `baseUrl` parameter.
     E.g. if you are accessing your application like this `http://www.server.com/myapp`, set `baseUrl => '/myapp'`

Questions
---------

If you have any question/suggestion/advice, please mail to <plover at gmail dot com>.
