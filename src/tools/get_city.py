import pathlib

import pandas as pd
from thefuzz import process
import structlog
from ..settings import COMMUNES_FRANCE_FILENAME

logger = structlog.get_logger()


def get_cities_by_postal_code(
    postal_code: str | int, folder_path: str | pathlib.Path | None = None
) -> list[str]:
    """
    Retrieve the list of cities associated with a given postal code.

    Args:
        postal_code: The postal code to search for (e.g., "34000" or 34000).
        folder_path: Optional path to the folder where the CSV files are stored.
                    If None, uses the default CSV_FOLDER from settings.

    Returns:
        A list of city names associated with the postal code.
    """
    logger.info("Getting city by postal code", postal_code=postal_code)

    df = pd.read_parquet(COMMUNES_FRANCE_FILENAME)
    df = df[df["code_postal"] == str(postal_code)]
    city_department_records = []
    for city in df["nom_standard"].unique().tolist():
        res = df[df["nom_standard"] == city][["nom_standard", "dep_code"]]
        city_department_records.extend(res.to_dict(orient="records"))
    return city_department_records


def filter_cities(cities: list[tuple[str, int]]) -> list[str]:
    # Check if any city has a value of 100
    city_with_100 = [city for city, value in cities if value == 100]

    if city_with_100:
        return city_with_100  # Return only the city/cities with 100
    else:
        # Sort cities by their value in descending order and return up to 5
        sorted_cities = sorted(cities, key=lambda x: x[1], reverse=True)
        return [city for city, value in sorted_cities]


def get_city_by_name(
    city_name: str, folder_path: str | pathlib.Path | None = None
) -> str:
    """
    Retrieve the city name associated with a given postal code.
    """
    logger.info("Getting city by name", city_name=city_name)
    df = pd.read_parquet(COMMUNES_FRANCE_FILENAME)
    list_city_name = df["nom_standard"].unique().tolist()
    city_names = process.extractBests(city_name, list_city_name, score_cutoff=80)
    city_names = filter_cities(city_names)
    city_department_records = []
    for city in city_names:
        res = df[df["nom_standard"] == city][["nom_standard", "dep_code"]]
        city_department_records.extend(res.to_dict(orient="records"))
    return city_department_records


if __name__ == "__main__":
    list_communes = get_cities_by_postal_code("30140")
    print(list_communes)
    city_names = get_city_by_name("Anduza")
    print(city_names)
