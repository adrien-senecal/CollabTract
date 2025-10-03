import folium
import structlog
import pandas as pd

from .csv_loading import get_df_adresse_locale

logger = structlog.get_logger()


def build_address(row):
    """
    Constructs a standardized address string from a DataFrame row.

    Args:
        row (pd.Series): A row from the df_ville DataFrame.

    Returns:
        str: Formatted address string.
    """
    # Extract components
    numero = str(int(row["numero"])) if pd.notna(row["numero"]) else ""
    rep = f" {row['rep']}" if pd.notna(row["rep"]) else ""
    nom_voie = row["nom_voie"] if pd.notna(row["nom_voie"]) else ""
    code_postal = str(int(row["code_postal"])) if pd.notna(row["code_postal"]) else ""
    nom_commune = row["nom_commune"] if pd.notna(row["nom_commune"]) else ""

    # Build address parts
    address_parts = []
    if numero:
        address_parts.append(numero + rep)
    if nom_voie:
        address_parts.append(nom_voie)

    # Combine into full address
    address_line = ", ".join(address_parts)
    full_address = f"{address_line}, {code_postal} {nom_commune}".strip(", ")

    return full_address


def generate_map(city: str, dep_code: int):
    """
    Generate a map for the specified city.

    Args:
        city: City name
        dep_code: Department code

    Returns:
        folium.Map: The generated map
    """
    logger.info("Generating map", city=city, dep_code=dep_code)

    # Use department code if provided, otherwise try to extract from city data
    try:
        if not isinstance(dep_code, int):
            logger.error("Department code must be an integer", dep_code=dep_code)
            raise ValueError("Department code must be an integer")
        df = get_df_adresse_locale(dep_code)
        df = df[df["nom_commune"] == city]
        if df.empty:
            logger.error(
                "City not found in the department", city=city, dep_code=dep_code
            )
            raise ValueError("City not found in the department")
    except Exception as e:
        logger.error("Error generating map", error=str(e))
        raise ValueError("Error generating map")

    center_lat = df["lat"].mean()
    center_lon = df["lon"].mean()
    logger.info("Center of the map", center_lat=center_lat, center_lon=center_lon)
    m = folium.Map(location=[center_lat, center_lon], zoom_start=14)
    for _, row in df.iterrows():
        adresse = build_address(row)
        folium.Marker([row["lat"], row["lon"]], popup=adresse).add_to(m)
    # m.save("map.html")
    return m


if __name__ == "__main__":
    generate_map("Paris")
