'''
The main CSSP-Brazil flask app

'''
__author__ = 'D.Ellis'
__organisation__ = 'CEMAC'
__contact__ = ''


'''
imports
'''

# file processing (uploads)
from flask import Flask, flash, request, redirect, render_template, url_for, Response, send_from_directory
from flask_socketio import SocketIO
from flask_statistics import Statistics
from flask_sqlalchemy import SQLAlchemy
import serverscripts.importdir as importdir
from serverscripts.config import *
from serverscripts.secure_db import *
from serverscripts.get_individual import m_new
from werkzeug.utils import secure_filename
import simplejson as json
import pandas as pd
from params import indicators
from pathlib import Path
import sys, os, re, glob
file = Path(__file__).resolve()
parent, root = file.parent, file.parents[1]  # 1 level up
sys.path.append(str(root))

# import the about scripts
importdir.do(str(parent) + '/about', globals())
f = parsetext.f
about_br = parsetext.about(about_us_text_pt_br)
about_uk = parsetext.about(about_us_text_en_uk)
tool_br = parsetext.about(about_tool_text_pt_br)
tool_uk = parsetext.about(about_tool_text_en_uk)
disc_br = parsetext.about(discl_liab_text_pt_br)
disc_uk = parsetext.about(discl_liab_text_en_uk)
ini_br = parsetext.about(ini_page_text_pt_br)
ini_en = parsetext.about(ini_page_text_en_uk)


rootdir = '/var/www/AgroClimatic-Monitor/app/'
app = Flask('AGROCLIM_SERVER',
            static_url_path='',  # removes path prefix requirement
            static_folder=os.path.abspath(
                rootdir + 'templates/static/'),  # static file location
            template_folder=rootdir + 'templates'  # template file location
            )


app.secret_key = app_key


app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///var/www/AgroClimatic-Monitor/statslog.sqlite3'
app.config['DATA_LOCATION'] = PROCESSED
app.config['MAX_CONTENT_LENGTH'] = file_mb_max * 1024 * 1024

sqlc = Database(db_loc, app_key)


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
def makedir(dest, upload=True):
    if upload:
        global STAGING
        fullpath = '%s%s' % (STAGING, dest)
    else:
        fullpath = dest
    print('read full: ', fullpath)
    if not os.path.isdir(fullpath):
        os.mkdir(fullpath)


#
try:
    makedir('')  # make uploads folder
except (PermissionError, FileNotFoundError) as e:
    print('ERROR: STORAGE Not Readable by Apache')
    print(
        'PermissionError: [Errno 13] Permission denied: /var/www/AgroClimatic-Monitor/uolstorage/Data/upload')


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
    if lang == 'br':
        atext = ini_br
        Title='Bem vindo!'
    else:
        atext = ini_en
        Title='Welcome!'

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template('about.html', layout=layout, atext=atext, title=Title)


@app.route('/<lang>/about')
def about(lang):

    if lang == 'staticpages':
        return None
    if lang == 'br':
        atext = about_br
        title = 'Sobre Nós'
    else:
        atext = about_uk
        title = 'About Us'

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template('about.html', layout=layout, atext=atext, title=title)


@app.route('/<lang>/tool')
def tool(lang):
    if lang == 'staticpages':
        return None
    if lang == 'br':
        atext = tool_br
        Title = "Usando a ferramenta"
    else:
        atext = tool_uk
        Title = 'Using the Tool'

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template('about.html', layout=layout, atext=atext, title=Title)


@app.route('/<lang>/disclaimer')
def disc(lang):
    if lang == 'staticpages':
        return None
    if lang == 'br':
        atext = disc_br
        Title = "Informação Legal"
    else:
        atext = disc_uk
        Title = "Disclaimer"

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template('about.html', layout=layout,  atext=atext, title=Title)


@app.errorhandler(404)
def not_found(e):
    return render_template("404.html", number=404)


@app.errorhandler(500)
def not_found500(e):
    return render_template("500.html", number=500)


@app.route('/error/<number>/<message>/')
def not_foundcustom(number, message):
    return render_template("404.html", number=number, message=message)


'''
Fetch Functions
'''


@app.route('/staticpages/<page>/')
def getstat(page):
    return render_template(page + '.html')


@app.route('/bundles/<page>/')
def getbundle(page):
    return render_template('bundles/' + page + '/dist/bundle.js')


@app.route('/allfiles/')
def getallfiles():
    print(PROCESSED)
    return send_from_directory('%s/' % (PROCESSED), 'allfiles.json', as_attachment=True)


@app.route('/data/<folder>/<item>/')
def getdata(folder, item):

    print('%s%s/' % (PROCESSED, folder), folder, item, '\n\n\n')

    return send_from_directory('%s%s/' % (PROCESSED, folder), item, as_attachment=True)


'''
overview
'''


@app.route('/<lang>/overview/')
def noover(lang):
    return redirect('/%s/overview/RZSM' % lang)


@app.route('/<lang>/overview/<what>')
def getover(lang, what):
    if lang == 'br':
        ov = index_anim_text_pt_br
        table = f(about_tool_text_pt_br.about_tool_textbox6_text)
        #page = 'overview_br.html'
    else:
        ov = index_anim_text_en_uk
        table = f(about_tool_text_en_uk.about_tool_textbox6_text)

    page = 'overview.html'

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template(page, layout=layout, title=ov.index_anim_title,
                           table=table, textbox1=f(ov.index_anim_textbox1),
                           indicator=what)


'''
Data Browser
'''
# @app.route('/<lang>/dataview/')
# def nobd(lang):
#     return redirect('/%s/dataview'%lang)


@app.route('/<lang>/databrowser')
def getdatamap(lang):
    if lang == 'br':
        ov = data_brows_text_pt_br
        table = f(about_tool_text_pt_br.about_tool_textbox6_text)
        button="Baixe a imagem atual"
        subtitle1="Instruções"
        subtitle2="Gráfico resumido"
        subtitle3="Mapa"
        subtitle4="Classificação"
        #page = 'overview_br.html'
    else:
        ov = data_brows_text_en_uk
        table = f(about_tool_text_en_uk.about_tool_textbox6_text)
        button="Download Current Image"
        subtitle1="Instructions"
        subtitle2="Summary Plot"
        subtitle3="Map"
        subtitle4="Classification"

    page = 'databrowser.html'

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'

    return render_template(page, layout=layout, title=ov.data_brows_title,
                           textbox1=f(ov.data_brows_textbox1), table=table,
                           button=button, subtitle1=subtitle1,
                           subtitle2=subtitle2, subtitle3=subtitle3,
                           subtitle4=subtitle4)


'''
Individual
'''
# @app.route('/<lang>/dataview/')
# def nobd(lang):
#     return redirect('/%s/dataview'%lang)


@app.route('/<lang>/individual/<geoid>/')
def getindi(lang, geoid):
    if lang == 'br':
        ov = data_brows_text_pt_br
        #page = 'overview_br.html'
    else:
        ov = data_brows_text_en_uk

    layout = 'layout.html'
    if lang == 'br':
        layout = 'layout_br.html'
        page = 'individual_br.html'
    else:
        page = 'individual.html'
    return render_template(page, layout=layout,  title=ov.data_brows_title, hash=geoid)


@app.route('/idata/<item>/')
def getidata(item):
    folder = 'muncipalities'
    fitem = 'file_%s.json' % item
    jsn = '%s%s/%s' % (PROCESSED, folder, fitem)
    updated = max([os.path.getmtime(i) for i in h5locs])
    try:
        # for some reasone try except was failing
        test=os.path.getmtime(jsn)
        if (os.path.getmtime(jsn) < updated):
            print('NEW DATA AVAILABLE')
            m_new(item)
            # Not sure what the assert false was about
            #assert False
    except FileNotFoundError:
        print('no json file found. Generating...')
        m_new(item)
        
    print('getidata')
    print(fitem)
    print('%s%s/' % (PROCESSED, folder), '\n\n\n')

    return send_from_directory('%s%s/' % (PROCESSED, folder), fitem, as_attachment=True)


'''
UPLOAD
'''

# on upload end
@socketio.on('upload_disconnect')
def process(data):
    global filelist
    print(data, '\n\nUPLOAD END\n\n')
    print(filelist)

# on page load display the upload file
@app.route('/upload')
def upload_form():
    layout = 'layout.html'
    # flash('Drag files to upload here.')
    return render_template('upload.html', layout=layout, uploads='This populates on sucessful submission...')


filelist = []

# on a POST request of data
@app.route('/upload', methods=['POST'])
def upload_file():
    global filelist
    if request.method == 'POST':

        psw = str(request.form['psw'])

        #         print(psw,'aaaasdkjlkj')

        # str(request.args.get('psw'))
        allfiles = request.files

        if 'files[]' not in allfiles:
            flash('No files found, try again.')
            return redirect(request.url)

        files = allfiles.getlist('files[]')

        for file in files:
            print(file)
            if file.mimetype in extensions:
                filename = secure_filename(file.filename)

                check = sqlc.writefile(psw, filename)
                if (check):
                    makedir(os.path.join(STAGING, check), False)
                    saveloc = os.path.join(STAGING, check, filename)
                    file.save(saveloc)

                    filesplit = filename.upper().split('_')
                    dest = filesplit[0]
                    makedir(STORAGE + dest, False)
                    if dest == 'SPI':
                        dest += '/%s%02d' % (dest, int(filesplit[1]))
                        makedir(STORAGE + dest, False)

                    fl = STORAGE + dest + '/' + \
                        filename.replace('.tiff', '.tif')

                    os.system('cp %s %s' % (saveloc, fl))


#                     os.system('/bin/gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3857 -r cubicpline %s %s'%(saveloc,fl))
                    filelist.append(fl)

                    print('-----------------', saveloc, fl)

                else:
                    print('Wrong Credentials! ')
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


# what have I updated? Return a list of updated files
@app.route('/uploaded/<upload_id>', methods=['GET', 'POST'])
def data_get(upload_id):

    if request.method == 'POST':  # POST request
        print(request.get_text())  # parse as text

        return 'OK', 200

    else:  # GET request
        print('%s/%s/*' % (STAGING, sqlc.writefile(upload_id)))
        files = glob.glob('%s/%s/*' % (STAGING, sqlc.writefile(upload_id)))
        print('------', upload_id, files)

        return ','.join([i.rsplit('/', 1)[1] for i in files])

if __name__ == "__main__":
    print('to upload files navigate to http://127.0.0.1:57263/upload')
    # lets run this on localhost port 4000
    # socketio.run(app,host='129.11.78.152',port=57263,debug=True)#,threaded=True)
    app.run()
