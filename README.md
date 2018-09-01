# sql-rest-blueprint
A blueprint generator for REST services linking to SQL databases.

The general idea of this program arose when I began writing REST APIs for various SQL databases. In the interest of debug/testability, many of my files were broken down into small, logical units that, from table to table, looked almost identical. 

This framework parses a SQL file for names, general structure and data types, and then uses those values to fill a template for an application, with the varying values substituted in for the tags that look something like `{{$this}}`.

This does not substitute the initial work of assembling a functional application to begin with, but once an application has been written once, the table/application specific values can be substituted in with tags for further generation. 

This is mostly a fancy copy/paste machine, but it takes the meticulous work out of building multi-table APIs.

There are no dependencies

to run, `cd` into the directory where your `.sql` file is. (server connection to be implemented)
then run `python /path/to/blueprint.py` with the appropriate flags.

# Flags

## `-l mylang`, `--lang mylang`, or `--language mylang`
### (REQUIRED)
The language/structure to use.

## `-s rel/path/to/src.sql` or `--source rel/path/to/src.sql` 
### (OPTIONAL, default: `init.sql` or first `*.sql` found alphabetically in the dir)
The relative path to the source file. (this would be a database create script)

## `-d rel/path/to/proj` or `--dest rel/path/to/proj` 
### (OPTIONAL, default : `./[database name]` is used if not specified)
The relative path to the destination folder.
This will be the root of your generated project

## `-n` or `--name` 
### (OPTIONAL, default: database name from sql file)
This will be the name used to give a name to the folder and stuff.

## `-v` or `--verbose` 
### (OPTIONAL)
I need to implement this, but nominally, it'll print stuff when I say verbose, and it'll print less without it.


## (TODO) `-q` or `--quiet`
### (OPTIONAL)
Will only print `SUCCESS` after complete copy. You'll see the stack trace if it fails.




Written in Python 3.6.2. compatibility tests coming whenever I have the time.



