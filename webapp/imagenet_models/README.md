Well, we need image recognition models to make the magic happen.
But first, you need to clone the repository of TensorFlow models so you can use some methods not included in TensorFlow.

```
cd path/for/cloning/tensorflow/models
git clone https://github.com/tensorflow/models.git
```

### Download and use Inception ResNet V2 model


#### Model checkpoints

You can run `download_and_save_inceptionresnet.py` to download the InceptionResNetV2 checkpoints and save them into the `models/` folder.

```
cd /path/to/webapp/models
python download_and_save_inceptionresnet.py
```

But, **hey**: you need to set the variables `models_slim_dir` and `download_dir` inside of `download_and_save_inceptionresnet.py` before running it.


- models_slim_dir: is located inside the cloned tensorflow models folder:

	clone_dir/models/slim from: git clone https://github.com/tensorflow/models.git


- download_dir: is any temporal directory to save the raw file for the model



### Other models

Hopefully (not tested yet) you can download easily all the models from [here](https://github.com/tensorflow/models/tree/master/slim#pre-trained-models) changing just a bit of the code in `download_and_save_inceptionresnet.py`.
