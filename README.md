# GREP on cloud

A GNU grep-like tool that works on Amazon AWS. It is called "fdsm", which stands for **f**ile **d**irectory **s**earch and **m**anipulation.

### Program Execution
  fdsm [-b] [-f] [-s <path/to/statementsfile>] [-i \<instance\>] [\<directory/to/instance\>]
  
The program options are as follows:

  -b: Traverse the directory in BFS manner. (default: DFS)\
  -f: Use full path name. (default: run on current path)\
  -s: Get statements from a file (given path/to/statementsfile). (default: get statements from stdin)\
  -i: Run on Amazon Cloud machine with given instance id. (default: on host machine)\
  directory: Choose in which directory the code will run on the cloud
### Syntax

Statements file has the following syntax:

    <fdsm expression> => <Unix/Python commands separated by comma>;
    ...
    
For example:

    start => {count = 0} ;
    /^A/ && file && d/01-04-2002/b => echo $MATCHED ; rm $MATCHED ;
    (/^core$/ || /.+\.o$/ ) && file => rm $MATCHED ;
    /^.*\.py$/ && file => {count = count+1\nprint $MATCHED} ;
    /junk/ && directory => rm $MATCHED ;
    finish => {print count} ;
    
The statements on the right can be either python or unix statements. Python statements are in curly brackets ({}). 

The statements on the left are in fdsm syntax which are patterns that will match file properties. The patterns are as follows:
    
syntax | meaning 
---|---
start, finish | beginning and the end of the code block
file, directory | if a path is a directory or a file
/\<regex-statement\>/ | item name matches
c/\<regex-statement\>/ | there is a match in file content
o/\<regex-statement\>/ | owner of the item matches
p/\<regex-statement\>/ | permission type of the item matches
d/\<regex-statement\>/[b/a] | date of the item matches (options: before/after)
s/\<regex-statement\>/[l] | size of the item matches (options: larger)
readable, writeable, executable | checks these permissions on the item

    
    
    
