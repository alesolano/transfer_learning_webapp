# transfer_learning_webapp

## Set environment

```
conda create -n transfer_webapp python=3.6
source activate transfer_webapp
```

```
pip install tensorflow
conda install -c anaconda flask
conda install scikit-learn
```

## Download models

Git clone TensorFlow models.
`git clone https://github.com/tensorflow/models.git`

Run `download_and_save_inceptionresnet.py` to download Inception Resnet V2.

## Run

```
cd webapp
export FLASK_APP=webapp.py
flask run
```