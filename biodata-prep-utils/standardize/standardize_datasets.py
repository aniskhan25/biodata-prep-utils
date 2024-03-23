import os
import pandas as pd


def standardize_datasets(metadata, overwrite=False):
    """
    Standardizes datasets based on metadata.

    Args:
        metadata (DataFrame): Metadata containing information about datasets.
        overwrite (bool, optional): Whether to overwrite existing standardized datasets. Default is False.

    Returns:
        DataFrame: Merged and standardized dataset with column names following Darwin Core terminology.
    """

    standardized_dataframes = []  # List to store standardized DataFrames

    for index, row in metadata.iterrows():

        file_name = row["fileName"]
        dataset_name = row["datasetName"]

        if not os.path.exists(file_name):
            print(f"File {file_name} not found. Skipping.")
            continue

        vector_for_recode = dict(
            [(key, value) for key, value in dict(row[2:]).items() if not pd.isna(value)]
        )  # Columns to select and rename

        standard_dataset = standardize_dataset(
            file_name, vector_for_recode, dataset_name
        )

        # Append the standardized DataFrame to the list
        standardized_dataframes.append(standard_dataset)

    # Merge the standardized DataFrames based on a common key column
    merged_dataframe = pd.concat(
        standardized_dataframes, axis=1
    )  # Adjust axis as needed

    return merged_dataframe


def standardize_dataset(file_name, vector_for_recode, dataset_name):
    """
    Standardizes a dataset based on specified parameters.

    Args:
        file_name (str): File name of the dataset to be standardized.
        vector_for_recode (list): List of columns to be recoded.
        dataset_name (str): Name of the dataset being standardized.

    Returns:
        DataFrame: Standardized dataset with recoded columns.
    """

    standard_dataset = pd.read_csv(file_name, skipinitialspace=True)

    # Select specific columns
    standard_dataset = standard_dataset[vector_for_recode.values()]

    # Rename columns
    standard_dataset.columns = vector_for_recode.keys()

    # Add 'database_id' column
    standard_dataset.insert(
        0, "database_id", dataset_name + "_" + standard_dataset.index.astype(str)
    )
    # standard_dataset['database_id'] = dataset_name + '_' + standard_dataset.index.astype(str)

    # Convert numeric columns to string
    numeric_columns = standard_dataset.select_dtypes(include="number").columns
    standard_dataset[numeric_columns] = standard_dataset[numeric_columns].astype(str)

    print("Standardizing", dataset_name, "file")

    return standard_dataset
