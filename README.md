# rt-movie-files
Renames all movie files in a folder to include rotten tomatoes scores

To use it just drop the .py file into the base directory where you keep your movies.

1. The program will find all movie files within the main directory and sub directories.
2. Check for each on RottenTomatoes.com
3. If a match is found it will rename the file to the format 'Movie Title (year) C-00% A-00%.ext'
4. Then there is an option to move all movie files to the base directory and delete their old subdirectories.

# Config Options

```
MOVE_FILES = True   # True/False Move files to base directory & delete old sub directories.
TEST_MODE = True   # True/False Test mode will print old/new filenames instead of renaming and moving the files.
```
There are two config options at top of the program

**MOVE_FILES** lets you decide if you want to move the movie files to the base directiory and delete the old sub directories or leave the movie files where they are

**TEST_MODE**, This is enabled by default and I highly recomend runnigng it this way first.  It will print out the old and new paths without moving any files, so you can check to make sure it works correctly.
