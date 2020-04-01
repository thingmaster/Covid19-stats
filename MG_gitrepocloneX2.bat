:getdate
rem Extract yyyy mm dd from date
set cdate=%DATE%
rem echo cdate=%DATE%
set cyear=%cdate:~10,4%
set cmonth=%cdate:~4,2%
set cday=%cdate:~7,2%
rem Extract hh from current time
set ctime=%TIME%
set ch1=%ctime:~0,1%
set ch2=%ctime:~1,1%
set cm1=%ctime:~3,1%
rem echo "%ch1%%cm1%" > %dropbox%\Cameras\%cameraname%\time.txt
if "%ch1%"=="1" goto :pastdate
if "%ch1%"=="2" goto :pastdate
set ch1=0
:pastdate
echo FILE:%cyear%.%cmonth%.%cday%.%ch1%%ch2%.%cm1%0-%2.jpg 
git clone https://github.com/CSSEGISandData/COVID-19
mkdir .\%cmonth%-%cday%
mkdir .\%cmonth%-%cday%\%ch1%%ch2%-%cm1%
git clone https://github.com/CSSEGISandData/COVID-19 --branch web-data --single-branch  webdata
copy COVID-19\archived_data\archived_time_series .\%cmonth%-%cday%
copy COVID-19\archived_data\archived_time_series .\%cmonth%-%cday%\%ch1%%ch2%-%cm1%
copy .\webdata\data .\%cmonth%-%cday%
copy .\webdata\data .\%cmonth%-%cday%\%ch1%%ch2%-%cm1%
rem copy .\COVID-19\archived_data\archived_time_series\
rem 
copy .\COVID-19\csse_covid_19_data\csse_covid_19_time_series\time_series_covid19_confirmed_global.csv .
rem COVID-19/csse_covid_19_data/csse_covid_19_time_series/
copy .\webdata\data\cases_state.csv .\cases_state-%cmonth%-%cday%.csv
del /F /S /Q .\webdata
del /F /S /Q .\COVID-19
rmdir webdata /S /Q
rmdir COVID-19 /S /Q
REM git clone https://github.com/CSSEGISandData/COVID-19/tree/web-data BRANCH FAILS WITHOUT --branch opt