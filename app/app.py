'''
The main CSSP-Brazil flask app

'''
__author__ = 'D.Ellis'
__organisation__= 'CEMAC'
__contact__='d.ellis-A-T-leeds.ac.uk'



''' 
imports
'''
import sys,os,re,glob

## file processing (uploads)
from pathlib import Path
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1] # 1 level up
sys.path.append(str(root))
# import each_h5 as processing
from params import indicators

import pandas as pd
import simplejson as json
from flask import Flask, flash, request, redirect, render_template,url_for,Response,send_from_directory
# from flask_login import (LoginManager, login_required, login_user, 
#                          current_user, logout_user, UserMixin)
# from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash
# print generate_password_hash("P1ain-text-user-passw@rd", "sha256")
#print check_password_hash("sha256$lTsEjTVv$c794661e2c734903267fbc39205e53eca607f9ca2f85812c95020fe8afb3bc62", "P1ain-text-user-passw@rd")



from serverscripts.get_individual import m_new
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
ini_br  = parsetext.about(ini_page_text_pt_br)
ini_en  = parsetext.about(ini_page_text_en_uk)


from flask_sqlalchemy import SQLAlchemy
from flask_statistics import Statistics
from flask_socketio import SocketIO


app=Flask('AGROCLIM_SERVER', 
            static_url_path='', # removes path prefix requirement 
            static_folder=os.path.abspath('templates/static/'),# static file location
            template_folder='templates' # template file location
            )
            
            
app.secret_key = app_key




app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///statslog.sqlite3'

app.config['DATA_LOCATION'] = PROCESSED
app.config['MAX_CONTENT_LENGTH'] = file_mb_max* 1024 * 1024

sqlc = Database(db_loc,app_key)



db = SQLAlchemy(app)
socketio = SocketIO(app)


class Request(db.Model):
    __tablename__ = "request"

    index = db.Column(db.Integer, primary_key=True, autoincrement=True)
    response_time = db.Column(db.Float)
    date = db.Column(db.DateTime)
    method = db.Column(db.String)
    size = db.Column(db.Integer)
    status_code = db.Column(db.Integer)
    path = db.Column(db.String)
    user_agent = db.Column(db.String)
    remote_address = db.Column(db.String)
    exception = db.Column(db.String)
    referrer = db.Column(db.String)
    browser = db.Column(db.String)
    platform = db.Column(db.String)
    mimetype = db.Column(db.String)

db.create_all()
statistics = Statistics(app, db, Request)





# # Check that the upload folder exists
def makedir (dest,upload=True):
    if upload:
            global STAGING
            fullpath = '%s%s'%(STAGING,dest)
    else:
            fullpath = dest
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)
# 
makedir('')# make uploads folder

# create uploads folders if they dont exist
# for i in indicators:
#             makedir(STORAGE+i,False)




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
    if lang == 'status':
            return 'Live'
    if lang == 'staticpages':
        return None
    if lang == 'upload':
        return redirect('/upload')
    if lang == 'br': atext = ini_br
    else: atext = ini_en
    return render_template('about.html', atext=atext, title='Welcome!')


@app.route('/<lang>/about')
def about(lang):
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


@app.errorhandler(404)
def not_found(e):
  return render_template("404.html", number= 404)


@app.errorhandler(500)
def not_found500(e):
  return render_template("404.html", number = 500)

@app.route('/error/<number>/<message>/')
def not_foundcustom(number,message):
  return render_template("404.html", number = number, message=message)





'''
Fetch Functions
'''

@app.route('/staticpages/<page>/')
def getstat(page):
    return render_template(page+'.html')

@app.route('/bundles/<page>/')
def getbundle(page):
    return render_template('bundles/'+page+'/dist/bundle.js')

@app.route('/allfiles/')
def getallfiles():
    print(PROCESSED)
    return send_from_directory('%s/'%(PROCESSED), 'allfiles.json', as_attachment=True)


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
Data Browser
'''
# @app.route('/<lang>/dataview/')
# def nobd(lang):
#     return redirect('/%s/dataview'%lang)

@app.route('/<lang>/databrowser')
def getdatamap(lang):
    if lang =='br':
        ov = data_brows_text_pt_br
        #page = 'overview_br.html'
    else: 
        ov = data_brows_text_en_uk
    
    page = 'databrowser.html'
    return render_template(page, title=ov.data_brows_title,textbox1=f(ov.data_brows_textbox1))


''' 
Individual
'''
# @app.route('/<lang>/dataview/')
# def nobd(lang):
#     return redirect('/%s/dataview'%lang)

@app.route('/<lang>/individual/<geoid>/')
def getindi(lang,geoid):
    if lang =='br':
        ov = data_brows_text_pt_br
        #page = 'overview_br.html'
    else: 
        ov = data_brows_text_en_uk
    
    page = 'individual.html'
    return render_template(page, title=ov.data_brows_title,hash=geoid)


@app.route('/idata/<item>/')
def getidata(item):
    folder = 'muncipalities'
    fitem = 'file_%s.json'%item
    jsn = '%s%s/%s'%(PROCESSED,folder,fitem)
    updated = max([os.path.getmtime(i) for i in h5locs])
    
    try:
        if (os.path.getmtime(jsn) < updated):
            print('NEW DATA AVAILABLE')
            assert False
    except FileNotFoundError:
        m_new(item)
    
    print('%s%s/'%(PROCESSED,folder),'\n\n\n')

    return send_from_directory('%s%s/'%(PROCESSED,folder), fitem, as_attachment=True)






'''
UPLOAD
'''

## on upload end
@socketio.on('upload_disconnect')
def process(data):
    global filelist 
    print(data,'\n\nUPLOAD END\n\n')
    print(filelist)

## on page load display the upload file
@app.route('/upload')
def upload_form():
    # flash('Drag files to upload here.')
    return render_template('upload.html',uploads = 'This populates on sucessful submission...')


filelist = []

## on a POST request of data 
@app.route('/upload', methods=['POST'])
def upload_file():
    global filelist
    if request.method == 'POST':
                        
        

        psw = str(request.form['psw'])
        
        #         print(psw,'aaaasdkjlkj')
        
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
                    makedir(check,False)
                    saveloc = os.path.join(STAGING,check, filename)
                    file.save(saveloc)
                    
                    filesplit = filename.upper().split('_')
                    dest = filesplit[0]
                    makedir(STORAGE+dest,False)
                    if dest == 'SPI':
                          dest += '/%s%02d'%(dest,int(filesplit[1]))
                          makedir(STORAGE+dest,False)

                    fl = STORAGE+dest+'/'+filename.replace('.tiff','.tif')
            
                    os.system('cp %s %s'%(saveloc,fl))
                   
            
            
            
#                     os.system('/bin/gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857 -r cubicpline %s %s'%(saveloc,fl))
                    filelist.append(fl)

                    print('-----------------',saveloc,fl)


                        
                else:
                    print( 'Wrong Credentials! ')
                    flash('Wrong Credentials!') 
                    return redirect('/upload')
            else:
                print('Not allowed', file)
                
        
        
        
#         try:fdata = json.load(open(FNEW))
#         except FileNotFoundError: fdata=[]

#         a_file = open(FNEW, "w")
#         fdata.extend(filelist)
#         json.dump(fdata, a_file)
#         a_file.close()    

        flash('File(s) uploaded')
        
#         last = pd.DataFrame([[i.replace(STAGING,''),os.path.getmtime(i)] for i in glob.glob(STAGING+check+'/*')], columns=['filename','created']).to_markdown(tablefmt="grid")
        
        print('*(^&*(&*(&*&', fdata)
        
#         flash('kljlkj')
        
        return redirect('/processing')
        #render_template('upload.html', uploads = f(last))



## what have I updated? Return a list of updated files
@app.route('/uploaded/<upload_id>', methods=['GET','POST'])
def data_get(upload_id):
    
    if request.method == 'POST': # POST request
        print(request.get_text())  # parse as text
        
        
        return 'OK', 200
    
    else: # GET request
        print('%s/%s/*'%(STAGING,sqlc.writefile(upload_id)))
        files = glob.glob('%s/%s/*'%(STAGING,sqlc.writefile(upload_id)) ) 
        print ('------',upload_id,files)
        
        return ','.join([i.rsplit('/',1)[1] for i in files])




if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:57263/upload')
    # lets run this on localhost port 4000
    socketio.run(app,host='129.11.78.152',port=57263,debug=True)#,threaded=True)
