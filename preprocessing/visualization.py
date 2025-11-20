from pathlib import Path
import sys
from typing import Optional

from images_analysis import show_image_array

REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RELATIVE = Path(r"/Users/pierrebernadet/Documents/projet-2/jamunet-morpho-braided/data/satellite2/original/JRC_GSW1_4_MonthlyHistory_training_r1/1988_02_01_training_r1.tif")
FALLBACK_FOLDER_RELATIVE = Path(r"/Users/pierrebernadet/Documents/projet-2/jamunet-morpho-braided/data/satellite2/original/JRC_GSW1_4_MonthlyHistory_training_r1")


def resolve_path(path_str: str) -> Path:
    """Return an existing path, trying both absolute and repo-relative locations."""
    candidate = Path(path_str).expanduser()
    if candidate.exists():
        return candidate

    repo_candidate = REPO_ROOT / path_str
    if repo_candidate.exists():
        return repo_candidate

    raise FileNotFoundError(f"{path_str} does not exist (checked {candidate} and {repo_candidate})")


def pick_image(path_str: Optional[str]) -> Path:
    """Return a valid GeoTIFF path, optionally using the provided path."""
    if path_str:
        path = resolve_path(path_str)
        if path.is_dir():
            tif_files = sorted(path.glob("*.tif"))
            if not tif_files:
                raise FileNotFoundError(f"No .tif files found in directory: {path}")
            return tif_files[0]
        return path

    default_path = REPO_ROOT / DEFAULT_RELATIVE
    if default_path.exists():
        return default_path

    fallback_folder = REPO_ROOT / FALLBACK_FOLDER_RELATIVE
    if not fallback_folder.exists():
        raise FileNotFoundError(f"{fallback_folder} does not exist")

    tif_files = sorted(fallback_folder.glob("*.tif"))
    if not tif_files:
        raise FileNotFoundError(f"No .tif files found in {fallback_folder}")
    return tif_files[0]


def main() -> None:
    selected_image = pick_image(sys.argv[1] if len(sys.argv) > 1 else None)
    print(f"Displaying {selected_image}")
    show_image_array(str(selected_image))


if __name__ == "__main__":
    main()
