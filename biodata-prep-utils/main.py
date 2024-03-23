"""Main module of your code

Author(s): Anis Ur Rahman

This code is covered under the GNU General Public License v3.0.
Please refer to the LICENSE located in the root of this repository.
"""

import os

import pandas as pd

from standardize.standardize_datasets import standardize_datasets


if __name__ == "__main__":

    path = "/Users/anisjyu/Documents/bdc/bdc/data"

    metadata = pd.read_csv(os.path.join(path, "DatabaseInfo.csv"))

    metadata["fileName"] = metadata["fileName"].str.replace(
        "https://raw.githubusercontent.com/brunobrr/bdc/master/inst/extdata/input_files/",
        os.path.join(path, "input/"),
    )

    print(metadata["fileName"])
    merged_df = standardize_datasets(metadata)

    # Write the standardized dataset to a CSV file
    merged_df.to_csv(
        os.path.join(path, "output", "00_merged_database.csv"),
        index=False,  # Set to True if you want to include row indices in the output file
    )
