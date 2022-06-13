from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
import click

@click.command()
@click.option("--channels", default=5, help="Number of Channels to include in the file")
@click.option(
    "--path", default="files/test_data.h5",
    help="File to save to. If the file exists a valid intiger "
         "will be appended to the file stem."
)
def generate_sample_test_file(channels, path):
    sampling_freq = 4_000
    sample_spacing = 1 / sampling_freq
    start_freq = 10
    stop_freq = sampling_freq // 2
    freq_content = np.array(range(start_freq, stop_freq + 1))
    sample_duration = 5
    rng = np.random.default_rng()

    # Index for out test file is the time steps in seconds
    index = np.arange(0, sample_duration + sample_spacing, sample_spacing)

    # Create the DF that will be used to add randomness to for each channel.
    df = pd.DataFrame(
        np.tile(index * 2 * np.pi,(len(freq_content),1)).T * freq_content,
        index=index,
        columns=freq_content
    )

    # Create the output df which will include all channels.
    channel_names = list(f"CHANNEL {i}" for i in range(1,channels + 1))
    output_df = pd.DataFrame(0.0, index=index, columns=channel_names)

    # create an overall shape to the PSD, smc breakpoints
    shape = pd.Series(150, index=pd.RangeIndex(start_freq, stop_freq+1))
    shape[shape.index >= 800] = 800 / shape.index[shape.index >= 800] * 150
    shape[shape.index <= 150] = shape.index[shape.index <= 150]

    for channel in channel_names:
        # Offset the sine waves.
        random_start = rng.random(len(freq_content)) * 2 * np.pi
        channel_df = df.add(random_start)

        channel_df = channel_df.apply(np.sin)

        # Create a random amplitude.
        random_factor = 1_000

        random_amplitude = rng.random(len(freq_content)) * shape
        channel_df = channel_df.mul(random_amplitude)

        # Sum the content of all the generated sine waves for a sudo random signal
        output_df[channel] = channel_df.sum(axis=1)

    # file saving
    output_path = Path(path)
    while output_path.is_file():
        version = output_path.stem.split("_")[-1]
        stem = output_path.stem.split("_")[:-1]

        if not stem:
            # There are no `_` in the string
            stem=version
            version = 1
        elif not version.isnumeric():
            # The last segment is not numeric, assumed not to be a version.
            stem = output_path.stem
            version = 1

        output_path = output_path.parent / f"{stem}_{version:03}{output_path.suffix}"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_df.to_hdf(output_path, 'data', 'w')

    print(f"Wrote {channels} channels to {output_path.absolute()}")

if __name__ == '__main__':
    generate_sample_test_file()