stocktotal
==========

--------------------------------------------------------------------------------

Introduction
------------
* Main remote repo: [BitBucket](https://bitbucket.org/Menggen/stocktotal/)
* Mirror remote repo: [GitHub](https://github.com/Meng-Gen/stocktotal/)
* stocktotal project contains 3 modules:
    * Source: source Taiwan stock information
    * Report: generate pdf/png report
    * Portal: generate web portal report

    
Environment
-----------

First of all, we need PostgreSQL 9.1 (or higher).  Then prepare the following environment for each module.
Source module is required if your database is empty.  

### Source module

* [Python 3.2](http://www.python.org/) (or higher) environment

### Report module

* Java running environment
* [Apache Ant](http://ant.apache.org/) building environment

### Portal module

* Apache2 
* PHP 5.3 (or higher)


Prerequirement
--------------

### Source module

* [lxml](http://lxml.de/): process HTML.  In Windows, may use [unofficial binary package](http://www.lfd.uci.edu/~gohlke/pythonlibs/)
* [py-postgresql](http://pypi.python.org/pypi/py-postgresql): PostgreSQL driver and tools library
* [7-Zip](http://www.7-zip.org/): file archiver in Windows
* xlrd: extract data from Microsoft Excel.  To use xlrd in Python 3, may use [takluyver-xlrd](https://github.com/takluyver/xlrd/zipball/py3)
* [wget](http://users.ugent.be/~bpuype/wget/): in Windows

### Report module

For license issue, we need to prepare the following required jar files:

* KAIU font: use iReport 4.x to import Windows KAIU font into a jar file, say `font-kaiu.jar`

### Portal module

* PHP 5 pdo driver for PostgreSQL


Deployment
----------

### PostgreSQL

1.   Create a new role `stocktotal` with password `stocktotal`
2.   Create a new database `stocktotal` with owner `stocktotal`

### Source module

1.   Create home directory: `$HOME_DIR`
2.   Clone: `git clone https://bitbucket.org/Menggen/stocktotal.git`
3.   Put `7z.exe` and `7-zip.dll` in directory `$HOME_DIR/source/core/thirdparty/sevenzip/`
4.   Put `wget.exe` in directory `$HOME_DIR/source/core/thirdparty/wget`

### Report module

* Put `font-kaiu.jar` in directory `$HOME_DIR/report/core/lib/`

### Portal module

* Copy `$HOME_DIR/portal` to Apache2 `htdocs` directory


Executing
---------

1.   Database schema: `$HOME_DIR/db/postgres/pg_dump.sql`. 
2.   Source module: execute `$HOME_DIR/source/source_manager.py -h` for usage.  Note that running source module will consume a lot of time.
3.   Report module: we need to build first: `$HOME_DIR/report/builder_manager.py`.  To generate report, execute `$HOME_DIR/report/generator_manager.py -h` for usage.
4.   Portal module: open web browser and browse `http://localhost/portal/report.php`


Questions
---------

If you have any question/suggestion/advice, please mail to plover@gmail.com
