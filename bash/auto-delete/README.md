Delete files before `n` days

### Example:

```
bash/time_files » ./mkfiles.sh 
total 0
-rw-rw-r-- 1 alexandre alexandre 0 May 24 00:00 00_first
-rw-rw-r-- 1 alexandre alexandre 0 May 23 11:18 01_day
-rw-rw-r-- 1 alexandre alexandre 0 May 23 00:00 01_first
-rw-rw-r-- 1 alexandre alexandre 0 May 23 23:59 01_last
-rw-rw-r-- 1 alexandre alexandre 0 May 22 00:00 02_first
-rw-rw-r-- 1 alexandre alexandre 0 May 22 23:59 02_last
-rw-rw-r-- 1 alexandre alexandre 0 May 21 23:59 03_last
bash/time_files » ./auto-delete.sh ./files 2
Path:   './files'
Before: '2019-05-23 00:00:00'  (Today: 2019-05-24 11:18:52)
        Confirm? (y/other)
y
./files/03_last
./files/02_first
./files/02_last
bash/time_files » ls -lh ./files 
total 0
-rw-rw-r-- 1 alexandre alexandre 0 May 24 00:00 00_first
-rw-rw-r-- 1 alexandre alexandre 0 May 23 11:18 01_day
-rw-rw-r-- 1 alexandre alexandre 0 May 23 00:00 01_first
-rw-rw-r-- 1 alexandre alexandre 0 May 23 23:59 01_last
```
