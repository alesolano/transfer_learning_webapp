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


    # create_folder()