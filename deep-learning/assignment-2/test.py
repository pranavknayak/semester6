import numpy as np
from PIL import Image
import typing

def pad(image: np.ndarray, padding: int):
    padded_image = np.zeros((image.shape[0] + 2 * padding, image.shape[1] + 2 * padding, image.shape[2]))
    padded_image[padding:-padding, padding:-padding, :] = image
    return padded_image


def sigmoid(z: np.ndarray, alpha: np.ndarray):
    return 1/(1 + np.exp(-z))

def tanh(z: np.ndarray, alpha: np.ndarray):
    return np.tanh(z)

def relu(z: np.ndarray, alpha: np.ndarray):
    return np.maximum(0, z)

# PReLU assumes that the passed ndarray 'z' and the parameter ndarray 'alpha' are broadcastable
def prelu(z: np.ndarray, alpha: np.ndarray):
    return np.maximum(0, z) + np.multiply(alpha, np.minimum(0, z))


def linear(z: np.ndarray, alpha: np.ndarray):
    return z


def softmax(z: np.ndarray, alpha: np.ndarray):
    return np.exp(z) / np.exp(z).sum()

#-----------------CONVOLUTION-----------------------#
def convolve(image: np.ndarray, kernel: np.ndarray, stride: int, padding: int, nl: callable, nl_parameter: np.ndarray):

  # number of channels is the third axis for both image and kernel

  if kernel.ndim == 3 and image.shape[2] != kernel.shape[2]:
    print("Kernel volume not compatible with number of image channels")
    return

  # pads the image with zeros
  if padding != 0:
    image = pad(image=image, padding=padding)

  w = image.shape[0]
  h = image.shape[1]
  c = image.shape[2]
  k = kernel.shape[0]

  final_img = np.zeros((int((w - k)/stride) + 1, int((h - k)/stride) + 1))

  for i in range(0, w - k + 1, stride):
    for j in range(0, h - k + 1, stride):
      final_img[i, j] = np.sum(np.multiply(image[i:i+k, j:j+k, :], kernel))

  final_img = nl(final_img, nl_parameter)

  return final_img
#-----------------CONVOLUTION-----------------------#


#------------------POOLING FUNCTIONS------------------#
def max_pooling(z: np.ndarray):
    return z.max()


def min_pooling(z: np.ndarray):
    return z.min


def avg_pooling(z: np.ndarray):
    return np.average(z)
#------------------POOLING FUNCTIONS------------------#



#------------------SINGLE POOLING---------------------#
def pooling(input_map: np.ndarray, stride: int, pool: callable):
    w = input_map.shape[0]
    h = input_map.shape[1]

    output_map = np.zeros((int(w/stride), int(h/stride)))

    for i in range(0, w - stride, stride):
        for j in range(0, h - stride, stride):
            output_map[int(i/stride), int(j/stride)] = pool(input_map[i: min(w, i + stride), j: min(h, j + stride)])

    return output_map
#------------------SINGLE POOLING---------------------#



#-----------------------CONV LAYER----------------------#
def convolution_layer(image: np.ndarray, nb_filters: int, kernel_dims: typing.List[typing.Tuple[int, int]], stride: int, padding: int, nl: int, nl_param: np.ndarray):
    filters = [np.random.randn(k_r, k_c, k_ch) for (k_r, k_c, k_ch) in kernel_dims]
    if isinstance(image, list):
        image = np.array(image)
        image = np.moveaxis(image, 0, -1)
        filters = [np.random.randn(k_r, k_c, image.shape[2]) for k_r, k_c, k_ch in kernel_dims]
    conv_volume = [convolve(image=image, kernel=kernel, stride=stride, padding=padding, nl=nl, nl_parameter=nl_param) for kernel in filters]
    #conv_volume = np.moveaxis(np.array(conv_volume), 0, -1)

    return conv_volume
#-----------------------CONV LAYER----------------------#



#-----------------POOLING LAYER----------------#
def pooling_layer(input_map_volume: typing.List[np.ndarray], pool: callable, stride: int, global_average=False):
    if not global_average:
        pooled_volume = [pooling(input_map=i, stride=stride, pool=pool) for i in input_map_volume]
        return pooled_volume
    else:
        pooled_volume = [np.average(i) for i in input_map_volume]
        return pooled_volume
#-----------------POOLING LAYER----------------#


#------------------------FLATTEN---------------------#
def flatten(input_volume: typing.List[np.ndarray], output_size: int):
    output_layer = np.concatenate(tuple([i for i in input_volume]), axis=None)
    reduction_matrix = np.random.randn(output_size, output_layer.shape[0])
    output_layer = np.matmul(reduction_matrix, output_layer)
    return output_layer.reshape((output_layer.shape[0], 1))
#------------------------FLATTEN---------------------#


#------------------------------MLP------------------------#
def mlp(input_layer: np.ndarray, nb_hidden_layers: int, hidden_layers: typing.List[int], nl: callable, nl_param: np.ndarray, output_size: int):
    input_layer = input_layer.reshape(input_layer.shape[0], 1)
    nb_layers = 2 + len(hidden_layers)
    sizes = [input_layer.shape[0]]
    sizes += hidden_layers
    sizes.append(output_size)

    biases = [np.random.randn(y, 1) for y in sizes[1:]]
    weights = [np.random.randn(y, x) for x,y in list(zip(sizes[:-1], sizes[1:]))]

    activations = []

    output_layer = input_layer
    for bias, weight in list(zip(biases, weights)):
        linear_input = np.dot(weight, output_layer) + bias
        output_layer = nl(linear_input, nl_param)

    return output_layer, softmax(output_layer, alpha=0)
#------------------------------MLP------------------------#



#-----------------------FEEDFORWARD-----------------------#
def cnn_feedforward(image: np.ndarray):
    conv_layer1 = convolution_layer(image=image, nb_filters=16, kernel_dims=[(3, 3, 3)] * 16, stride=1, padding=0, nl=sigmoid, nl_param=0)
    pooled_layer1 = pooling_layer(input_map_volume=conv_layer1, pool=max_pooling, stride=2)
    conv_layer2 = convolution_layer(pooled_layer1, nb_filters=8, kernel_dims=[(3, 3, 1)] * 8, stride=1, padding=0, nl=sigmoid, nl_param=0)
    pooled_layer2 = pooling_layer(input_map_volume=conv_layer2, pool=max_pooling, stride=2)
    pooled_layer3 = pooling_layer(input_map_volume=pooled_layer2, pool=max_pooling, stride=1, global_average=True)
    mlp_output_layer, softmax_layer = mlp(input_layer=np.array(pooled_layer3), nb_hidden_layers=1, hidden_layers=[len(pooled_layer3)], nl=sigmoid, nl_param=0, output_size=10)

    return mlp_output_layer, softmax_layer
#-----------------------FEEDFORWARD-----------------------#


#--------IMAGE EXTRACTION-------#
def unpickle(file):
    import pickle
    with open(file, 'rb') as fo:
        dict = pickle.load(fo, encoding='bytes')
    return dict

batch1 = unpickle('cifar-10-python/cifar-10-batches-py/data_batch_1')
data = batch1[b'data']
red_channel = data[0, :1024].reshape(32, 32, 1)
green_channel = data[0, 1024:2048].reshape(32, 32, 1)
blue_channel = data[0, 2048:3072].reshape(32, 32, 1)

cifar_image = np.concatenate((red_channel, green_channel, blue_channel), axis=2)
#--------IMAGE EXTRACTION-------#



#------FINAL-----------#
test_output, sm_output = cnn_feedforward(image=cifar_image.astype(np.float64))
