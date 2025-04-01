import argparse
import numpy as np
import matplotlib as mpl
from PIL import Image
from multiprocessing import Pool
from time import perf_counter

xlim = [-0.748766713922161, -0.748766707771757];
ylim = [ 0.123640844894862,  0.123640851045266];

def process_chunk(process, width, height, x, y, max_iter, rows_per_chunk):

    i_start = process*rows_per_chunk
    i_end   = min(i_start + rows_per_chunk, height)

    X,Y = np.meshgrid(x,y[i_start:i_end])
    C   = X + 1j*Y
    Z   = 0*C

    image_data = np.ones_like(C, dtype=np.uint)*max_iter
    for k in range(max_iter):
        ind = image_data==max_iter
        Z[ind] = Z[ind]**2 + C[ind]
        image_data[ind*(np.abs(Z) > 2.0)] = k

    return image_data


def generate_mandelbrot(width, height, max_iter, processes):

    x = np.linspace(xlim[0], xlim[1], width)
    y = np.linspace(ylim[0], ylim[1], height)

    rows_per_chunk = (height + processes - 1) // processes


    with Pool(processes=processes) as pool:
        results = [pool.apply_async(process_chunk, (p,width,height,x,y,max_iter,rows_per_chunk)) for p in range(processes)]
        pool.close()
        pool.join()

    return np.concatenate([r.get() for r in results])

if __name__ == '__main__':

    # create the argument parser
    parser = argparse.ArgumentParser(
        description='Builds a Mandelbrot set image using multiprocessing.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--width', default=1024,
                       help='image width in pixels')
    parser.add_argument('--height', default=1024,
                       help='image height in pixels')
    parser.add_argument('--proc', default=1,
                       help='number of processes to run on')

    # parse the arguments
    args = parser.parse_args()

    width = int(args.width)
    height = int(args.height)
    max_iter = 255
    processes = int(args.proc)

    start = perf_counter()
    image_data = generate_mandelbrot(width, height, max_iter, processes)
    elapsed = perf_counter() - start

    cmap = mpl.colormaps['viridis']

    m,M = np.min(image_data), np.max(image_data)
    image_data = ((image_data-m)/(M-m)*255).astype(np.uint8)
    image_data = (255*cmap(image_data)).astype(np.uint8)
    image = Image.fromarray(image_data)

    fname = f'mandelbrot_{width}x{height}_{processes}P.png'
    image.save(fname)

    print()
    print(f'Elapsed time: {elapsed}s')
    print(f'Saved image to {fname}.')
    print()
