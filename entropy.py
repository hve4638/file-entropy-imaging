from collections import Counter
import os
import numpy as np
from PIL import Image
import sys

def get_dataset_path(dirpath):
    result = []
    for dirpath, _, filenames in os.walk(dirpath):
        result.extend((dirpath, filename) for filename in filenames)
    return result

def count_byte_frequency(filename:str) -> Counter:
    with open(filename, 'rb') as f:
        data = f.read()
    byte_groups = [byte for byte in data]
    frequency = Counter(byte_groups)
    return frequency

def export_image(filename:str, byte_counter:Counter):
    size = 16
    max_prob = byte_counter.most_common(1)[0][1]
    pixel1d = [round(byte_counter[i]*255/max_prob) for i in range(256)]
    pixels = [pixel1d[i * size:(i + 1) * size] for i in range(size)]
    # print(pixels)
    final_image = Image.fromarray(np.array(pixels), 'L')
    final_image.save(filename)

# dataset_dirpath = './dataset/normal'
datasetpath = get_dataset_path(sys.argv[1])

for dir, file in datasetpath:
    os.makedirs(f'./export/{dir}', exist_ok=True)
    counter = count_byte_frequency(f'{dir}/{file}')
    export_image(f'./export/{dir}/{file}.png', counter)