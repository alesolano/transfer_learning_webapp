import os
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
from config import *
from flask import render_template
import time

app = Flask(__name__)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def create_folder_save_files(file, class_name):

    #print('file', file)
    #print('file.filename', file.filename)
    if file.filename == '':
        print('No selected file')
        return redirect(request.url)

    # if user does not select file, browser also submit a empty part without filename
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        #print('class_name, filename', class_name, filename)
        #print('app.config[UPLOAD_FOLDER] + / + class_name', app.config['UPLOAD_FOLDER'] + '/' + class_name)
        #print('--------------------------------')

        # Recreate folder if not exists
        if not os.path.exists(app.config['UPLOAD_FOLDER'] + '/' + class_name):
            os.makedirs(app.config['UPLOAD_FOLDER'] + '/' + class_name)

        # Save each file in folder
        file.save(os.path.join(app.config['UPLOAD_FOLDER'] + '/' + class_name, filename))
        #print('file saved')


def log_form_info():
    print('--------------------------------')
    print('request',request)
    #print('request.form',request.form)
    print('dict(request.form)',dict(request.form))
    #print('request.files',request.files)
    #print('dict(request.files)',dict(request.files))
    #print('list_request.files.keys()',list(request.files.keys()))

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        log_form_info()
        #1. Get general form elements
        if 'ml_models' not in request.form:
            print('No model selected')
            return redirect(request.url)

        model_name = request.form['ml_models']
        retrained_model_name = request.form['retrained_model_name']


        #2. Get table form elements
        classes_list = []
        table_row_ids = list(request.files.keys())#List of all rows in table
        for table_row_id in table_row_ids:
            # Variables for request parameters:
            class_name = request.form[table_row_id]
            print('class_name', class_name)
            classes_list.append(class_name)
            files = request.files.getlist(table_row_id)
            for file in files:
                create_folder_save_files(file, class_name)
            print("Saved {} files for class {}".format(len(files), class_name))

        print('classes_list',classes_list)


        return redirect(url_for('training', model_name=model_name, classes_list=classes_list, retrained_model_name=retrained_model_name))
    return render_template("index.html")


@app.route('/training', methods=['GET', 'POST'])
def training():
    if request.method == 'GET':
        import time
        time.sleep(3)
        retrained_model_name = request.args.get('retrained_model_name')
        model_name = request.args.get('model_name')
        classes_list = request.args.getlist('classes_list')
        print('retrained_model_name',retrained_model_name)

        from extracting_features import extract_features
        #extract_features(retrained_model_name, model_name, classes_list)

        from retraining import retrain
        #retrain(retrained_model_name, model_name)

        #print('classes_list_training',classes_list)
        model_short_name = model_name
        model_long_name = models_names_dict[model_short_name]

        available_retrained_models = get_immediate_subdirectories('./retrained_models/' + retrained_model_name + '/')
        return render_template("training.html",
                               model_short_name=model_short_name,
                               model_long_name=model_long_name,
                               classes_list=classes_list,
                               retrained_model_name=retrained_model_name,
                               available_retrained_models = available_retrained_models)

    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            print('No file part')
            return redirect(request.url)

        if 'import_options' not in request.form:
            print('No import option selected')
            return redirect(request.url)

        if 'ml_models' not in request.form:
            print('No model selected')
            return redirect(request.url)

        #Variables for request parameters:
        file = request.files['file']
        import_option = request.form['import_options']
        model_name = request.form['ml_models']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #return redirect('/uploaded')
            print('return successful')
            return redirect(url_for('uploaded', filename=filename, import_option=import_option, model_name=model_name))

@app.route('/uploaded')
def uploaded():
    filename = request.args.get('filename')
    model_name = request.args.get('model_name')
    print("Selected model:", model_name)
    print("Filename:", filename)

    begin = time.time()
    pred_class, pred_score = predictor.evaluate(
        filename=request.args.get('filename'),
        model_name=model_name)
    end = time.time()
    
    return render_template("uploaded.html",
        filename=filename,
        pred_class_0=str(pred_class[0]),
        pred_class_1=str(pred_class[1]),
        pred_class_2=str(pred_class[2]),
        pred_class_3=str(pred_class[3]),
        pred_class_4=str(pred_class[4]),
        pred_score_0=str(pred_score[0]),
        pred_score_1=str(pred_score[1]),
        pred_score_2=str(pred_score[2]),
        pred_score_3=str(pred_score[3]),
        pred_score_4=str(pred_score[4]),
        elapsed_time=format(end-begin, '.5f'))


@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/contact')
def contact():
    return render_template("contact.html")


if __name__ == '__main__':
    app.run(port=5000, debug=True)