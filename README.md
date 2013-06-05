# Script to CRC check .rar files

Script performs following steps:

1) Check this folder for all .rar files: `/DMDS/9.Vuze/1.Share/*.rar`

2) Copies all files into a temporary file folder

3) CRC check all .rar files:

    unrar t %rar-filenname% > results.mvg

  Check each rar files results.mvg for word "All OK" if word is not found file is corrupted.

4) If file is corrupted .rar file gets deleted.

5) Each rar file has a two additional files that also gets deleted if file I corrupt.

Say filename is 2007-01-01-01-01.rar then these two files also exist:

2007-01-01-01-01.mvg
2007-01-01-01-01.id

These files should be deleted also.

So it's: %rar-filename%.rar
%rar-filename%.mvg
%rar-filename%.id


