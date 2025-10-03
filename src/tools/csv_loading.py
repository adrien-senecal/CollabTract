import requests
import pandas as pd
import pathlib
import structlog

from .validation import validate_departement, check_folder_path

logger = structlog.get_logger()


def load_base_adresse_locale(
    departement: str | int, output_folder: pathlib.Path | None = None
) -> pathlib.Path:
    logger.info(
        "Loading base adresse locale",
        departement=departement,
        output_folder=output_folder,
    )

    departement = validate_departement(departement)
    output_folder = check_folder_path(output_folder)

    # Define the file path
    filename = f"adresses-{departement}.csv.gz"
    filepath = output_folder / filename

    # Download the file
    url = rf"https://adresse.data.gouv.fr/data/ban/adresses/latest/csv/adresses-{departement}.csv.gz"
    response = requests.get(url)
    response.raise_for_status()

    # Save the file
    with open(filepath, "wb") as f:
        f.write(response.content)

    logger.info("File saved", filepath=filepath)
    return filepath


def get_df_adresse_locale(
    departement: str | int, folder_path: pathlib.Path | None = None
) -> pd.DataFrame:
    """
    Get address data for a specific department.

    Args:
        departement: Department code (e.g., "34", "2A", "971")
        folder_path: Optional path to the folder where CSV files are stored

    Returns:
        pd.DataFrame: Address data for the department
    """
    logger.info("Getting df adresse locale", departement=departement)
    departement = validate_departement(departement)
    filename = f"adresses-{departement}.csv.gz"
    folder_path = check_folder_path(folder_path)
    filepath = folder_path / filename

    if not filepath.exists():
        logger.info("File does not exist, loading from internet", filepath=filepath)
        try:
            load_base_adresse_locale(departement, folder_path)
        except Exception as e:
            logger.error(
                "Failed to load address data from internet",
                error=str(e),
                departement=departement,
            )
            return pd.DataFrame()  # Return empty DataFrame on error
    else:
        logger.info("File exists, loading from local", filepath=filepath.name)

    try:
        df = pd.read_csv(filepath, compression="gzip", delimiter=";")
        logger.info(
            "Successfully loaded address data", rows=len(df), departement=departement
        )
        return df
    except Exception as e:
        logger.error(
            "Failed to read address data file", error=str(e), filepath=filepath
        )
        return pd.DataFrame()  # Return empty DataFrame on error
