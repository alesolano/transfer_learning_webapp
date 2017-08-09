# transfer_learning_webapp

## Set environment

```
conda create -n transfer_webapp python=3.6
source activate transfer_webapp
```

```
pip install tensorflow
conda install -c conda-forge tqdm
conda install scikit-learn
```

## Download models

Git clone TensorFlow models.
`git clone https://github.com/tensorflow/models.git`

Run `download_and_save_inceptionresnet.py` to download Inception Resnet V2.

## Run

```
python get_data.py
python extract_features.py
python retrain.py
python predict_flower.py tests/rose_test.jpg
```