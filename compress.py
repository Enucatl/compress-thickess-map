import click
import numpy as np
import collections
import humanize
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.Path())
def main(input_file, output_file):
    # read big endian 4byte = 32 bit float
    chunk_size = 100000
    a = np.memmap(
        input_file,
        mode="r",
        dtype=np.dtype(">f4"),
        shape=(chunk_size * 100,),
    )
    print("reading: {}".format(humanize.naturalsize(a.size * a.dtype.itemsize)))
    n_chunks = a.size // chunk_size
    counter = collections.Counter()
    for i in tqdm(range(n_chunks)):
        size, counts = np.unique(
            a[i * chunk_size:(i + 1) * chunk_size],
            return_counts=True,
        )
        d = dict(zip(size, counts))
        counter.update(d)
    output_array = np.array(list(counter.items()))
    print("saving results...")
    np.savetxt(
        output_file,
        output_array,
        header="size,counts",
        delimiter=",",
        comments="")



if __name__ == "__main__":
    main()
