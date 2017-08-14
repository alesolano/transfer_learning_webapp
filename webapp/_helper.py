request.form ImmutableMultiDict([('Class2', '2'), ('Nclasses', ''), ('Class1', '1'), ('Class3', '')])
dict(request.form) {'Class2': ['2'], 'Nclasses': [''], 'Class1': ['1'], 'Class3': ['']}

request.files ImmutableMultiDict([('file2', <FileStorage: 'images (2).jpg' ('image/jpeg')>), ('file3', <FileStorage: '' ('application/octet-stream')>), ('file1', <FileStorage: 'images (1).jpg' ('image/jpeg')>)])
dict(request.files) {'file2': [<FileStorage: 'images (2).jpg' ('image/jpeg')>], 'file3': [<FileStorage: '' ('application/octet-stream')>], 'file1': [<FileStorage: 'images (1).jpg' ('image/jpeg')>]}

list_request.files.keys() ['file2', 'file3', 'file1']


file_keys = list(request.files.keys())

for file_key in file_keys:
    #print('request.files.getlist_' + file_key, request.files.getlist(file_key))
    file = request.files[file_key]
    class_name = request.form[file_key]
    filename = secure_filename(file.filename)
    print('------------')
    print(class_name,filename)
    print('------------')

    if not os.path.exists(app.config['UPLOAD_FOLDER']+'/'+class_name):
        os.makedirs(app.config['UPLOAD_FOLDER']+'/'+class_name)

    file.save(os.path.join(app.config['UPLOAD_FOLDER']+'/'+class_name, filename))

classes_list = []
for file_key in file_keys:
    classes_list.extend(request.form[file_key])


request <Request 'http://127.0.0.1:5000/' [POST]>

request.form ImmutableMultiDict([('import_options', 'checkpoints'), ('file2', '3'), ('file1', '2'), ('Nclasses', ''), ('file0', '1'), ('ml_models', 'inception_resnet_v2')])
dict(request.form) {'import_options': ['checkpoints'], 'file2': ['3'], 'file1': ['2'], 'Nclasses': [''], 'file0': ['1'], 'ml_models': ['inception_resnet_v2']}

request.files ImmutableMultiDict([('file2', <FileStorage: 'images (4).jpg' ('image/jpeg')>), ('file0', <FileStorage: '9k= (3).jpg' ('image/jpeg')>), ('file0', <FileStorage: '9k= (4).jpg' ('image/jpeg')>), ('file0', <FileStorage: 'images (1).jpg' ('image/jpeg')>), ('file1', <FileStorage: 'images (2).jpg' ('image/jpeg')>)])
dict(request.files) {'file2': [<FileStorage: 'images (4).jpg' ('image/jpeg')>], 'file0': [<FileStorage: '9k= (3).jpg' ('image/jpeg')>, <FileStorage: '9k= (4).jpg' ('image/jpeg')>, <FileStorage: 'images (1).jpg' ('image/jpeg')>], 'file1': [<FileStorage: 'images (2).jpg' ('image/jpeg')>]}


list_request.files.keys() ['file2', 'file0', 'file1']
file <FileStorage: 'images (4).jpg' ('image/jpeg')>
file.filename images (4).jpg
class_name, filename 3 images_4.jpg






request <Request 'http://127.0.0.1:5000/' [POST]>
request.form ImmutableMultiDict([('ml_models', 'inception_resnet_v2'), ('Nclasses', ''), ('row1', '2'), ('row2', '3'), ('import_options', 'checkpoints'), ('row0', '1')])
dict(request.form) {'ml_models': ['inception_resnet_v2'], 'Nclasses': [''], 'row1': ['2'], 'row2': ['3'], 'import_options': ['checkpoints'], 'row0': ['1']}
request.files ImmutableMultiDict([('row0', <FileStorage: 'images (4).jpg' ('image/jpeg')>), ('row0', <FileStorage: 'images (5).jpg' ('image/jpeg')>), ('row0', <FileStorage: 'images (6).jpg' ('image/jpeg')>), ('row0', <FileStorage: 'images (7).jpg' ('image/jpeg')>), ('row2', <FileStorage: '2Q== (5).jpg' ('image/jpeg')>), ('row2', <FileStorage: '2Q== (6).jpg' ('image/jpeg')>), ('row2', <FileStorage: '2Q== (7).jpg' ('image/jpeg')>), ('row2', <FileStorage: '2Q==.jpg' ('image/jpeg')>), ('row1', <FileStorage: '2Q== (3).jpg' ('image/jpeg')>)])
dict(request.files) {'row1': [<FileStorage: '2Q== (3).jpg' ('image/jpeg')>], 'row2': [<FileStorage: '2Q== (5).jpg' ('image/jpeg')>, <FileStorage: '2Q== (6).jpg' ('image/jpeg')>, <FileStorage: '2Q== (7).jpg' ('image/jpeg')>, <FileStorage: '2Q==.jpg' ('image/jpeg')>], 'row0': [<FileStorage: 'images (4).jpg' ('image/jpeg')>, <FileStorage: 'images (5).jpg' ('image/jpeg')>, <FileStorage: 'images (6).jpg' ('image/jpeg')>, <FileStorage: 'images (7).jpg' ('image/jpeg')>]}
list_request.files.keys() ['row0', 'row2', 'row1']
file <FileStorage: 'images (4).jpg' ('image/jpeg')>
file.filename images (4).jpg
class_name, filename 1 images_4.jpg

