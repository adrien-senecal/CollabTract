import pathlib

from ..settings import CSV_FOLDER
import structlog

logger = structlog.get_logger()


def check_folder_path(folder_path: pathlib.Path | None) -> pathlib.Path:
    if folder_path is None:
        folder_path = pathlib.Path(CSV_FOLDER)
    elif not isinstance(folder_path, pathlib.Path):
        raise ValueError("folder_path must be a string or a pathlib.Path object")
    folder_path.mkdir(parents=True, exist_ok=True)
    return folder_path


def validate_departement(departement: str | int) -> str:
    # Convert to string if it's an integer
    if isinstance(departement, int):
        departement = str(departement)

    # Handle string cases (including 'a' or 'b')
    if isinstance(departement, str):
        departement = departement.upper()  # Transform 'a' or 'b' to 'A' or 'B'

        # Check for valid string formats (2A or 2B)
        if departement in ["2A", "2B"]:
            return departement

        # Check for valid integer ranges (01-95 or 971-989)
        if departement.isdigit():
            num = int(departement)
            if (1 <= num <= 95) or (971 <= num <= 989):
                return departement.zfill(
                    2
                )  # Pad with leading zero if needed (e.g., 1 → "01")

    # Return None or raise an error if invalid
    logger.error("Invalid departement", departement=departement)
    raise ValueError(
        f"Invalid departement: {departement}. Must be 01-95, 971-989, or 2A/2B."
    )
