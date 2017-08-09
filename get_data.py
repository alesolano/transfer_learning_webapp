from urllib.request import urlretrieve
from os.path import isfile, isdir
from tqdm import tqdm
import tarfile

cifar10_dataset_folder_path = 'flower_photos'
cifar10_file_path = 'flower_photos.tar.gz'

class DLProgress(tqdm):
    last_block = 0

    def hook(self, block_num=1, block_size=1, total_size=None):
        self.total = total_size
        self.update((block_num - self.last_block) * block_size)
        self.last_block = block_num

if not isfile(cifar10_file_path):
    with DLProgress(unit='B', unit_scale=True, miniters=1, desc='Flowers Dataset') as pbar:
        urlretrieve(
            'http://download.tensorflow.org/example_images/flower_photos.tgz',
            cifar10_file_path,
            pbar.hook)

if not isdir(cifar10_dataset_folder_path):
    with tarfile.open(cifar10_file_path) as tar:
        tar.extractall()
        tar.close()