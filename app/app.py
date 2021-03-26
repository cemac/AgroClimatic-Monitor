'''
The main CSSP-Brazil flask app

'''
__author__ = 'D.Ellis'
__organisation__= 'CEMAC'
__contact__='d.ellis-A-T-leeds.ac.uk'


'''
CONSTS
'''

PROCESSED = '/Users/wolfiex/CCSP-Brazil/processed/'




''' 
imports
'''
import sys,os,re,glob
import simplejson as json
from flask import Flask, flash, request, redirect, render_template,url_for,Response,send_from_directory

from werkzeug.utils import secure_filename
from serverscripts.secure_db import *
from serverscripts.config import *
# import the about scripts
import serverscripts.importdir as importdir
importdir.do('about',globals())
f = parsetext.f
about_br = parsetext.about(about_us_text_pt_br)
about_uk = parsetext.about(about_us_text_en_uk)
tool_br = parsetext.about(about_tool_text_pt_br)
tool_uk = parsetext.about(about_tool_text_en_uk)
disc_br = parsetext.about(discl_liab_text_pt_br)
disc_uk = parsetext.about(discl_liab_text_en_uk)

# import getchoro as gc



app=Flask('CSSPBRZ', 
            static_url_path='', # removes path prefix requirement 
            static_folder=os.path.abspath('templates/static/'),# static file location
            template_folder='templates' # template file location
            )
            
            
app.secret_key = app_key
# app.config['SERVER_NAME']='CCSP.server'


app.config['DATA_LOCATION'] = PROCESSED
app.config['MAX_CONTENT_LENGTH'] = file_mb_max* 1024 * 1024
sqlc = Database(db_loc,app_key)

# # Check that the upload folder exists
# def makedir (dest):
#     fullpath = '%s/%s'%(upload_dest,dest)
#     if not os.path.isdir(fullpath):
#         os.mkdir(fullpath)
# 
# makedir('')# make uploads folder

'''
serve static
'''

#app.add_url_rule('/favicon.ico', redirect_to=flask.url_for('static', filename='favicon.ico'))
# @app.route('/counties.json')
# def favicon():
#     return redirect(url_for('static', filename='counties.json'))
# @app.route('/<path:filename>')
# def serve_static(filename):
#     root_dir = os.path.dirname(os.getcwd())
#     return send_from_directory(app.static_folder, filename)
# 


'''
Home
'''

@app.route('/')
def nolang():
    return redirect('/en/')


@app.route('/<lang>/')
def home(lang):
    if lang == 'staticpages':
        return None
    
    if lang == 'br': atext = about_br
    else: atext = about_uk
        
    return render_template('about.html', atext=atext, title='About Us')



@app.route('/<lang>/tool')
def tool(lang):
    if lang == 'staticpages':
        return None
    if lang == 'br': atext = tool_br
    else: atext = tool_uk
        
    return render_template('about.html', atext=atext, title='Using the Tool')



@app.route('/<lang>/disclaimer')
def disc(lang):
    if lang == 'staticpages':
        return None
    if lang == 'br': atext = disc_br
    else: atext = disc_uk
        
    return render_template('about.html', atext=atext, title='Disclaimer')











'''
Fetch Functions
'''

@app.route('/staticpages/<page>/')
def getstat(page):
    return render_template(page+'.html')

@app.route('/bundles/<page>/')
def getbundle(page):
    return render_template('bundles/'+page+'/dist/bundle.js')


@app.route('/data/<folder>/<item>/')
def getdata(folder,item):
    
    print('%s%s/'%(PROCESSED,folder),folder,item,'\n\n\n')

    return send_from_directory('%s%s/'%(PROCESSED,folder), item, as_attachment=True)
    


'''
overview
'''


@app.route('/<lang>/overview/')
def noover(lang):
    return redirect('/%s/overview/RZSM'%lang)

@app.route('/<lang>/overview/<what>')
def getover(lang,what):
    if lang =='br':
        ov = index_anim_text_pt_br
        #page = 'overview_br.html'
    else: 
        ov = index_anim_text_en_uk
    
    page = 'overview.html'
    return render_template(page, title=ov.index_anim_title,textbox1=f(ov.index_anim_textbox1),indicator=what)










'''
UPLOAD
'''
## on page load display the upload file
@app.route('/upload')
def upload_form():
    flash('Drag files to upload here.')
    return render_template('upload.html')


## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        psw = str(request.form['psw'])
        #str(request.args.get('psw'))
        allfiles = request.files

        if 'files[]' not in allfiles:
            flash('No files found, try again.')
            return redirect(request.url)

        files = allfiles.getlist('files[]')

        for file in files:
            print (file)
            if file.mimetype in extensions:
                filename = secure_filename(file.filename)
                
                check = sqlc.writefile(psw,filename)
                if (check):
                    makedir(check)
                    file.save(os.path.join(upload_dest,check, filename))
                else:
                    print( 'Wrong Credentials! ')
                    flash('Wrong Credentials!') 
                    return redirect('/upload')
            else:
                print('Not allowed', file)
                
        
        flash('File(s) uploaded')
        return redirect('/upload')



## what have I updated? Return a list of updated files
@app.route('/uploaded/<upload_id>', methods=['GET','POST'])
def data_get(upload_id):
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        return 'OK', 200
    
    else: # GET request
        print('%s/%s/*'%(upload_dest,sqlc.writefile(upload_id)))
        files = glob.glob('%s/%s/*'%(upload_dest,sqlc.writefile(upload_id)) ) 
        print ('------',upload_id,files)
        return ','.join([i.rsplit('/',1)[1] for i in files])




if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:4000/upload')
    # lets run this on localhost port 4000
    app.run(host='127.0.0.1',port=4000,debug=True,threaded=True)
