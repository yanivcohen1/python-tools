import numpy as np
import matplotlib.pyplot as plt
from skimage.data import gravel
from skimage.filters import difference_of_gaussians, window
# import scipy.signal
# Load an example image (you can replace this with your own image)
image = gravel()

# Apply a Hann window to reduce edge artifacts
wimage = image * window('hann', image.shape)

# Apply the Difference of Gaussians (DoG) filter
filtered_image = difference_of_gaussians(image, 1, 12)
filtered_wimage = filtered_image * window('hann', image.shape)

# Display original and filtered images
fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))

ax[0,0].imshow(image, cmap='gray')
ax[0,0].set_title(f'original image')
fft_image = np.fft.fft2(image)
ax[0,1].imshow(np.log1p(np.abs(fft_image)), cmap='gray')
ax[0,1].set_title('fft image')

ax[1,0].imshow(filtered_image, cmap='gray')
ax[1,0].set_title(f'filterd image')
fft_filtered_image = np.fft.fft2(filtered_image)
ax[1,1].imshow(np.log1p(np.abs(fft_filtered_image)), cmap='gray')
ax[1,1].set_title('fft filterd image')

plt.show()
