import click
import numpy as np
import collections
import humanize
from tqdm import tqdm


@click.command()
@click.argument("input_file", type=click.Path(exists=True))
@click.argument("output_file", type=click.File("wb"))
def main(input_file, output_file):
    # read big endian
    chunk_size = 100000
    a = np.memmap(
        input_file,
        mode="r",
        dtype=np.dtype(">f4"),
        shape=(chunk_size * 10000,),
    )
    print("reading: {}".format(humanize.naturalsize(a.size)))
    n_chunks = a.size // chunk_size
    counter = collections.Counter()
    for i in tqdm(range(n_chunks)):
        sizes, counts = np.unique(
            a[i * chunk_size:(i + 1) * chunk_size],
            return_counts=True,
        )
        d = dict(zip(sizes, counts))
        counter.update(d)
    output_array = np.array(list(counter.items()), dtype=np.float16)
    np.save(output_file, output_array)



if __name__ == "__main__":
    main()
