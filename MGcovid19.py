import numpy as np
from statsmodels.formula.api import ols
import pandas
from MGcsvutils import MGcsvutils

x = np.linspace(-5, 5, 20)

np.random.seed(1)

# normal distributed noise

y = -5 + 3*x + 4 * np.random.normal(size=x.shape)

# Create a data frame containing all the relevant variables

data = pandas.DataFrame({'x': x, 'y': y})

#“formulas” for statistics in Python

#See the statsmodels documentation

#Then we specify an OLS model and fit it:


model = ols("y ~ x", data).fit()

print(model)

covidfile = "C:\\Users\\PG Dev\\Downloads\\COVID-19-master-23\\COVID-19-master\\csse_covid_19_data\\csse_covid_19_time_series\\time_series_19-covid-Confirmed.csv"

csvinstance = MGcsvutils()
csvinstance.MGC_opencsv(covidfile) #open another file

#while csvinstance.MGC_getcsvline() :
#    pass

recordlist = csvinstance.MGC_loadcsvdata(True)
datadict = dict()
for i in recordlist:
    tag0 = i[1]
    if not i[0] =='': 
        tag0 += '-'+i[0]
    datadict[tag0] = i[4:]

interestedlist = ['US-California', 'US-New York','US-Washington','US-New Jersey','Italy','China-Henan','China-Beijing']
#for i in interestedlist:
dailyratethreshold = 200
totalthreshold=1700
for i in datadict:
    if i== 'Country/Region-Province/State':
        daystrs = str(datadict[i])
        daystrs = daystrs.strip('[]')
        print("\"Region\",", "\"Days below 100/day\",",  "\"Days exceeded 100\",", "\"Total cases\",", "\"7day growth %\",","\"7day avg/day\",","\" x \",","\"7day daily\",", daystrs )
        continue
    results = list(map(int, datadict[i]))
    if   results[-1] < totalthreshold and not i in interestedlist :
        continue
    resultsdiffs =  [results[n]-results[n-1] for n in range(1,len(results))]
    avg7days = sum(resultsdiffs[-7:])/len(results[-7:])
    bhund = True
    firsthund = -1
    last3digits = -1
    for ix in range(0,len(resultsdiffs)):        
        if resultsdiffs[ix] >= 100: 
            if bhund:
                firsthund = ix
                last3digits = ix
                bhund = False
            else:
                last3digits = ix
    if firsthund == -1:
        continue
    #last3digits = len(results)
    dayspost100 = len(results) - last3digits - 2
    daysover100 = last3digits - firsthund + 1
    resultstr = str(results)
    resultstr = resultstr.strip('[]')
    resultsdiffstr = str(resultsdiffs)
    resultsdiffstr = resultsdiffstr.strip('[]')
    print("\"%s\","%i, dayspost100,",", daysover100, ",","%d,"%results[-1],"%3.1f%%,"%(results[-1]/results[-7]*100.0),"%6.2f,"%avg7days, ",\"",resultsdiffs[-7:],"\",",resultstr,",", resultsdiffstr)

exit(0)


data = pandas.read_csv(covidfile, sep=',', na_values=".")
print (data.shape)
nrows, ncols = data.shape
print (data.columns)
#for j in data.columns: 
#    for k in data[j]:
#        print(j, k )
#for j in data.values:
#    print(len(j),j[10],j)

for i in range(0,nrows):
    print(data.columns[i])
    for j in range(0,ncols):
        print(data[i,j])

for j in data.columns:
    print(j,data[j])
    for k in data[j] :
        i = 0
        try: 
            i = k
        except:
            pass
        if  i==k:
            print('---->',k)

#numpy
import numpy as np

t = np.linspace(-6, 6, 20)

sin_t = np.sin(t)

cos_t = np.cos(t)
pandas.DataFrame({'t': t, 'sin': sin_t, 'cos': cos_t})  
#print(data.rows)
for i in data:
    print(i) #data )