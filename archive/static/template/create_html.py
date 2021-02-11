import jinja2,glob,os,json

def arrange(x):
    x= list(set(x))
    x.sort()
    return x


# os.system('')




title = 'Drought Compare'
description = 'We use a bivariate colour bar to indicate regions of drought using the VHI and SPI indicators. See key for more information.'
outputfile = '../droughtcompare.html'

files = list(json.load(open('../plotdata/biindicate.json')).keys())  
files.sort()

year = []
month = []
for date in files:
    syear = date[:4]
    smonth = date[4:]
    year.append(syear)
    month.append(smonth)

subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader('./')      
              ).get_template('drought_template.html').render(title=title,description=description,year = arrange(year), month=arrange(month) ) 
# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)












'''
'''



## SPI 03

title = 'SPI 3 Month avarage'
description = 'Some text on what this is.'
outputfile = '../spi3.html'
ext = '_spi_03.png'
files = glob.glob('../plotdata/??????'+ext)
files.sort()
#[[-76.125,-34.125].reverse(), [-31.875,6.125].reverse()]
bounds = [[-34.125,-76.125],[6.125,-31.875]]


year = []
month = []
for i in files:
    date = i.split('/')[-1].split('_')[0]
    syear = date[:4]
    smonth = date[4:]
    year.append(syear)
    month.append(smonth)
    
    
    
subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader('./')      
              ).get_template('image_template.html').render(title=title,description=description,files=files,year = arrange(year), month=arrange(month),ext=ext,smonth = smonth, syear=syear ,bounds = bounds) 
# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)


'''
'''

## SPI 06

title = 'SPI 6 Month avarage'
description = 'Some text on what this is.'
outputfile = '../spi6.html'
ext = '_spi_06.png'
files = glob.glob('../plotdata/??????'+ext)
files.sort()
bounds = [[-34.125,-76.125],[6.125,-31.875]]

year = []
month = []
for i in files:
    date = i.split('/')[-1].split('_')[0]
    syear = date[:4]
    smonth = date[4:]
    year.append(syear)
    month.append(smonth)
    
    
    
subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader('./')      
              ).get_template('image_template.html').render(title=title,description=description,files=files,year = arrange(year), month=arrange(month),ext=ext,smonth = smonth, syear=syear, bounds = bounds ) 
# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)



'''
'''



## VHI

title = 'VHI'
description = 'Some text on what this is.'
outputfile = '../vhi.html'
ext = '_VHI.png'
files = glob.glob('../plotdata/??????'+ext)
files.sort()

bounds = [[-33.75086,-73.99095],[5.27313,-34.78695]]
# bounds = left=-73.9909560699855, bottom=-33.750867566597, right=-34.78695775763141, top=5.27313075350569

year = []
month = []
for i in files:
    date = i.split('/')[-1].split('_')[0]
    syear = date[:4]
    smonth = date[4:]
    year.append(syear)
    month.append(smonth)
    
    
    
subs = jinja2.Environment( 
              loader=jinja2.FileSystemLoader('./')      
              ).get_template('image_template.html').render(title=title,description=description,files=files,year = arrange(year), month=arrange(month),ext=ext,smonth = smonth, syear=syear ,bounds = bounds) 
# lets write the substitution to a file
with open(outputfile,'w') as f: f.write(subs)
