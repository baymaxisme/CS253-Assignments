import numpy as np
def apply_filter(image, kernel):
    rows, cols = image.shape
    padded_image = np.pad(image, pad_width = 1, mode ='constant', constant_values= 0 ) #Creating the 1-pixel border of zeros
    output_image = np.zeros((rows, cols))

    #Iterating through every pixel of the original image
    for i in range(rows):
        for j in range(cols):
            region = padded_image[i:i+3, j:j+3] #Extracting the 3x3 matrix from the padded image
            pixel_sum = np.sum(region*kernel) #multiplying that matrix by the kernel and summing it up
            output_image[i,j] = pixel_sum 
    
    output = np.clip(output_image, 0, 255) #cliping values to [0,255]

    # .astype(int) cast the output to int type
    return output.astype(int) 


#TO SEE OUTPUT
#if __name__ == "__main__":
#    import numpy as np
#
#   dummy_img = np.array([
#        [10, 10, 10],
#        [10, 50, 10],
#        [10, 10, 10]
#    ])
#
#   edge_kernel = np.array([
#       [-1, -1, -1],
#       [-1,  8, -1],
#        [-1, -1, -1]
#    ])
#
#    print(apply_filter(dummy_img, edge_kernel))