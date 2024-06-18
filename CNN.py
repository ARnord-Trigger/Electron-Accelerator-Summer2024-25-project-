import numpy as np

def conv2D(input , filters , stride =1 , padding=0): #takes in 2D input and generates 3D output
    """
    perform a 2D conv operation
    
    Parameters:
    -input : 2D np array
    -filters : 3D np array shape:(num_filters, filter_height, filter_width)
    -stride
    -padding
    
    Returns:
    -output: 3D array with shape (num_filters, output_height, input_width)
    """
    num_filters , filter_height , filter_width = filters.shape
    input_height , input_width = input.shape
    
    #apply padding if !=0
    if (padding>0):
        input = np.pad(input , ((padding , padding),(padding , padding)), mode = 'constant')
    
    #calculate output dimensions
    output_height = (input_height - filter_height + 2 * padding) // stride + 1
    output_width = (input_width - filter_width + 2 * padding) // stride + 1
    output = np.zeros((num_filters, output_height, output_width))
    
    # Extract patches from the input data
    patches = np.lib.stride_tricks.as_strided(
        input,
        shape=(output_height, output_width, filter_height, filter_width),
        strides=(input.strides[0] * stride, input.strides[1] * stride, input.strides[0], input.strides[1]),
        writeable=False
    )
    for i in range(num_filters):
        filter = filters[i]
        output[i] = np.tensordot(patches, filter, axes=((2, 3), (0, 1)))
    
    return output
    
class ConvLayer:
        def __init__(self, num_filters, filter_size, input_shape):
          self.num_filters = num_filters
          self.filter_size = filter_size
          self.input_shape = input_shape
          self.filters = np.random.randn(num_filters, filter_size, filter_size)
        
        def forward(self, input):  
            self.output = conv2D(input , self.filters)
            return self.output;
        def backward():pass