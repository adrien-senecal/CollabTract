from math import radians, cos, sin, sqrt, atan2
import pandas as pd
from sklearn.cluster import KMeans
import structlog

logger = structlog.get_logger()


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great-circle distance between two points
    on the Earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371000  # Radius of Earth in meters
    return r * c


def detect_outliers(series: pd.Series) -> pd.Series:
    """
    Detect outliers in a series using the IQR method.
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 5 * IQR
    upper_bound = Q3 + 5 * IQR
    outliers = series[(series < lower_bound) | (series > upper_bound)]
    return outliers if len(outliers) == 1 else pd.Series()


def estimate_street_type(df: pd.DataFrame, street_name: str) -> str:
    """
    Estimate the type of street based on the distribution of the number of addresses.
    """
    df_street = df[df["nom_voie"] == street_name]
    numeros = df_street["numero"].sort_values()
    outliers = detect_outliers(numeros)
    if not outliers.empty:
        # Filter outliers for analysis
        numeros = numeros[~numeros.isin(outliers)]
    # Calculate the distances between consecutive numbers
    numero_distance = numeros.diff().dropna()
    # If the median of the distances is < 3, it's a center-city
    if numero_distance.median() < 3:
        if not outliers.empty:
            logger.warning(
                f"Attention : valeurs aberrantes détectées pour {street_name} : {outliers.tolist()}"
            )
        return "Center"
    else:
        return "Side"


def estimate_street_length(df: pd.DataFrame, street_name: str) -> int:
    df_street = df[df["nom_voie"] == street_name]
    street_type = estimate_street_type(df, street_name)
    if street_type == "Side":
        return int(df_street["numero"].max())
    else:
        lat_min = df_street["lat"].min()
        lat_max = df_street["lat"].max()
        lon_min = df_street["lon"].min()
        lon_max = df_street["lon"].max()
        return int(haversine(lat_min, lon_min, lat_max, lon_max))


def get_street_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Count the number of addresses, calculate the mean latitude and longitude for each street and estimate the street length.

    Returns:
        pd.DataFrame: Indexed by 'nom_voie', with columns 'count', 'mean_lat', 'mean_lon', and 'length'.

    """
    result = (
        df.groupby("nom_voie")
        .agg(
            count=("address", "count"),
            mean_lat=("lat", "mean"),
            mean_lon=("lon", "mean"),
        )
        .reset_index()
    )
    result["length"] = result["nom_voie"].apply(
        lambda street: estimate_street_length(df, street)
    )
    result["length"] = result["length"].astype(int)
    result.set_index("nom_voie", inplace=True)
    result.rename(columns={"mean_lat": "lat", "mean_lon": "lon"}, inplace=True)
    return result


def weighted_spatial_clustering(
    df: pd.DataFrame, column_to_balance: str, n_clusters: int
):
    logger.info("Starting Weighted Spatial Clustering")
    logger.info(f"Clustering {column_to_balance} with {n_clusters} clusters")
    result_df = df.copy()
    X = df[["lat", "lon"]].values
    if column_to_balance is None:
        weights = None
    else:
        weights = df[column_to_balance].values
    kmeans = KMeans(n_clusters=n_clusters, random_state=42).fit(
        X, sample_weight=weights
    )
    result_df["cluster"] = kmeans.labels_
    stats_cluster = result_df.groupby("cluster").agg({"count": "sum", "length": "sum"})
    logger.info(f"Clustering Complete for {column_to_balance}")
    logger.info(stats_cluster)
    logger.info("Clustering Complete")
    return result_df, stats_cluster


def add_cluster_to_df(df: pd.DataFrame, df_cluster: pd.DataFrame) -> pd.DataFrame:
    """
    Add the cluster column to the df dataframe.
    """
    df_with_cluster = df.merge(
        df_cluster[["cluster"]], left_on="nom_voie", right_index=True, how="left"
    )
    return df_with_cluster


def make_balanced_clustering(
    df: pd.DataFrame,
    column_to_balance: str,
    n_clusters: int,
) -> pd.DataFrame:
    """
    Make a balanced clustering of the df dataframe.
    """
    df_streets = get_street_data(df)

    df_clustered, stats_cluster = weighted_spatial_clustering(
        df_streets, column_to_balance, n_clusters
    )
    df = add_cluster_to_df(df, df_clustered)
    return df, stats_cluster


if __name__ == "__main__":
    print("Not supposed to be run directly")
