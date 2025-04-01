import argparse
import numpy as np
import matplotlib as mpl
from PIL import Image
from time import perf_counter

import pycuda.autoinit
import pycuda.driver as drv
from pycuda.compiler import SourceModule

# the CUDA kernel
mod = SourceModule("""
__global__ void mandelbrot_kernel(int width, int height, unsigned char* img_data) {
    const double xmin = -0.748766713922161;
    const double xmax = -0.748766707771757;
    const double ymin = 0.123640844894862;
    const double ymax = 0.123640851045266;
    const unsigned char max_iter = 255;

    const int i = blockIdx.x * blockDim.x + threadIdx.x;

    if (i >= width * height) {
        return;
    }

    const int xi = i%width;
    const int yi = i/width;

    const double x = xmin + (xmax - xmin) * xi / width;
    const double y = ymin + (ymax - ymin) * yi / height;

    double zr = 0.0, zi = 0.0, cr = x, ci = y;

    unsigned char n = 0;
    for (n = 0; n < max_iter; n++) {
        double tmp = zr;
        zr = zr*zr - zi*zi + cr;
        zi = 2*tmp*zi + ci;
        if (zr*zr + zi*zi > 4.0) {
           break;
        }
    }

    img_data[i] = n;
    return;
}
""")

mandelbrot_kernel = mod.get_function("mandelbrot_kernel")


def generate_mandelbrot(width, height):

    threads = 256
    blocks = (width*height + threads - 1) // threads

    img_data = np.zeros(width*height, dtype=np.uint8)
    mandelbrot_kernel(np.int32(width), np.int32(height), drv.Out(img_data), block=(threads,1,1), grid=(blocks,1))

    return img_data.reshape(height,width)


if __name__ == '__main__':

    # create the argument parser
    parser = argparse.ArgumentParser(
        description='Builds a Mandelbrot set image using a GPU.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--width', default=1024,
                       help='image width in pixels')
    parser.add_argument('--height', default=1024,
                       help='image height in pixels')

    # parse the arguments
    args = parser.parse_args()

    width = int(args.width)
    height = int(args.height)

    start = perf_counter()
    image_data = generate_mandelbrot(width, height)
    elapsed = perf_counter() - start

    cmap = mpl.colormaps['viridis']

    m,M = np.min(image_data), np.max(image_data)
    image_data = ((image_data-m)/(M-m)*255).astype(np.uint8)
    image_data = (255*cmap(image_data)).astype(np.uint8)
    image = Image.fromarray(image_data)

    fname = f'mandelbrot_{width}x{height}_cuda.png'
    image.save(fname)

    print()
    print(f'Elapsed time: {elapsed}s')
    print(f'Saved image to {fname}.')
    print()
