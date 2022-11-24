# Directory Reporting and Clean up Utility

## Description

Create a command line program, `stale_file.py` that accepts three parameters:

1. a root directory
2. a best before dat in teh form YYYY-MM-DD
3. action which is one of "Print"/"P" or "Report"/"R"

Based on these inputs `stale_file.py` generates a list all of the files that haven't been modified since the best before date and either outputs them to the console or writes them to a report file.

### Print

If the third parameter is "Print" the n the program prints the list of files.

The output includes:

1. A header showing the root directory and the best before date
2. A line for each file that includes:
   1. The relative path of each file from the root directory
   2. The modification date of the file
   3. The file size in MB

### Report

If the third parameter is "Report" then the program generates a report file called `YYYY_MM_DD_stale_files_.txt` in the same directory as the `stale_file.py script file

The first line of hte file is the full path of the root directory.

This the remaining lines of the file contain the following columns separated by commas:

* The Full path of each file
* The modification date of the file in the form YYYY-MM-DD
* The file size in bytes

### Extra: Deletion Utility (Unmarked)

This program `dir_cleanup.py` accepts a single parameter, a report file.

It reads the report csv file, outputs the list of files to be deleted, prompts the user for confirmation to delete the files, and if given deletes the files listed in the report.

If a subdirectory is empty after the files are deleted then the subdirectory is also deleted.

### Additional Requirements

The program should gracefully handle the following situations:
* The root directory doesn't exists
* The best before date is not valid
* The action is not one of "Print" or "Report"

### Example Directory Hierarchy

A test file hierarchy can be created by calling the make_file_hierachy.py script which
creates a hierarchy specified in the file_hierarchy.csvfile. These files need to be in the same directory.

When run: python make_file_hierachy.py the script creates a directory called test_root in the same directory as the script file. The test_root directory contains a hierarchy of files and directories.

The outputs below are based on this directory hierarchy.

### Invocation: Print

```plaintext
python stale_file.py test_root 2021-05-09 Print 

Root Directory: C:\Users\thomas_lane\OneDrive - BCIT\course_content\acit_1515_202130\instructor\projects\clean_up_project\test_root
Best Before Date: 2021-05-09

Files to delete:
subdir1                                                                          2021-05-08      0  B
subdir1\file11.txt                                                               2020-12-14    145  B
subdir1\file12.txt                                                               2021-05-08    145  B
subdir2\file21.txt                                                               2021-05-08    145  B
```

### Invocation: Report

`python stale_file.py test_root 2021-05-09 Report`

The above command generates the following report file: 2021_05_09_stale_files.txt with the following contents:

```plaintext
C:\Users\thomas_lane\clean_up_project\test_root
C:\Users\thomas_lane\clean_up_project\test_root\subdir1,2021-05-08,0
C:\Users\thomas_lane\clean_up_project\test_root\subdir1\file11.txt,2020-12-14,145
C:\Users\thomas_lane\clean_up_project\test_root\subdir1\file12.txt,2021-05-08,145
C:\Users\thomas_lane\clean_up_project\test_root\subdir2\file21.txt,2021-05-08,145
```

## References

### Pathlib

1. https://realpython.com/python-pathlib/
2. https://zetcode.com/python/pathlib/
3. https://docs.python.org/3/library/pathlib.html

### Datetime

1. https://realpython.com/python-datetime/
2. https://docs.python.org/3/library/datetime.html

### Python os module (required to set file timestamps):

1. https://nitratine.net/blog/post/change-file-modification-time-in-python/
2. https://docs.python.org/3/library/os.html

### Globs and Paths

1. [What is a Glob in computing terms](https://en.wikipedia.org/wiki/Glob_(programming))
2. [How to use Pathlib 1](https://pymotw.com/3/pathlib/index.html)
3. [How to use Pathlib 2](https://realpython.com/python-pathlib/)
4. [Official Pathlib documentation](https://docs.python.org/3/library/pathlib.)
