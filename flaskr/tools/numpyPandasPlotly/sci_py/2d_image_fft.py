from skimage import color
from skimage import io
import matplotlib.pyplot as plt
from scipy.fft import fft, ifft, fft2, ifft2
import numpy as np

img_load = io.imread('flaskr/tools/numpyPandasPlotly/sci_py/2d_image_flower.PNG')
rgb_img = color.rgba2rgb(img_load)
gray_img = color.rgb2gray(rgb_img)
plt.imshow(gray_img, cmap='gray')
plt.show()

# fft in 2D
img_FT = fft2(gray_img)
fy = np.fft.fftfreq(gray_img.shape[0],d=10) #suppose the spacing between pixels is 10mm, for example
fx = np.fft.fftfreq(gray_img.shape[1],d=10)
print('{:.2f} correponds to fx={:.6f} and fy={:.6f}'.format(img_FT[10,20], fx[20], fy[10]))
plt.imshow(np.abs(img_FT), cmap='gray', vmax=50)
plt.colorbar()
plt.show()

# Remove low frequencies
img_FT_alt = np.copy(img_FT)
img_FT_alt[-2:] = 0
img_FT_alt[:,-2:] = 0
img_FT_alt[:2] = 0
img_FT_alt[:,:2] = 0
# inverse fft in 2D
img_alt = np.abs(ifft2(img_FT_alt))
plt.imshow(img_alt, cmap='gray')
plt.colorbar()
plt.show()
