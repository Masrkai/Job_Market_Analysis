import  csv
import logging
from pathlib import Path
from helpers.resolve_path import resolve_file_path

# Optional: configure logging (you can adjust level/format as needed)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def ensure_dir(
    dir_path: str,
    base_dir: str | None = None,
    exist_ok: bool = True,
    mode: int = 0o755,
    raise_on_file_conflict: bool = True,
) -> str:
    """
    Ensure a directory exists, creating it (and parents) if necessary.

    Args:
        dir_path (str):
            Path to the directory. Can be:
              - Absolute (e.g., "/opt/app/data")
              - Relative to current working dir (e.g., "output/logs")
              - Relative to script (default if base_dir=None)
              - Relative to custom base_dir
        base_dir (str | None):
            Optional base directory for resolving relative paths.
            If None, resolves relative to the calling script (like resolve_file_path).
        exist_ok (bool):
            If True (default), no error if dir already exists.
            If False, raises FileExistsError if dir exists.
        mode (int):
            Permissions for created directories (default: 0o755 → rwxr-xr-x).
        raise_on_file_conflict (bool):
            If True (default), raises OSError if a *file* exists at the path.
            If False, logs warning and returns path (but no dir is created).

    Returns:
        str: Absolute path to the ensured directory.

    Raises:
        OSError: If a file exists at the path and raise_on_file_conflict=True.
        FileExistsError: If directory exists and exist_ok=False.
        PermissionError, etc.: Standard OS errors on mkdir failure.
    """
    # Resolve to absolute path
    abs_path = resolve_file_path(dir_path, base_dir=base_dir)

    path_obj = Path(abs_path)

    # Check if something already exists at this path
    if path_obj.exists():
        if path_obj.is_dir():
            if not exist_ok:
                raise FileExistsError(f"Directory already exists: {abs_path}")
            logger.debug(f"Directory already exists (ok): {abs_path}")
        elif path_obj.is_file():
            msg = f"Path exists but is a file, not a directory: {abs_path}"
            if raise_on_file_conflict:
                raise OSError(msg)
            else:
                logger.warning(msg)
        # else: could be symlink, socket, etc. — treat cautiously (let mkdir handle?)
    else:
        # No path exists → safe to create
        try:
            path_obj.mkdir(parents=True, mode=mode, exist_ok=exist_ok)
            logger.info(f"Created directory: {abs_path}")
        except Exception as e:
            logger.error(f"Failed to create directory {abs_path}: {e}")
            raise

    return abs_path


# 🛠 Convenience wrappers (optional but handy)

def ensure_data_dir(dir_name: str = "data", base_dir: str | None = None) -> str:
    """Ensure a 'data' subdirectory relative to script or base_dir."""
    return ensure_dir(dir_name, base_dir=base_dir)

def ensure_output_dir(dir_name: str = "output", base_dir: str | None = None) -> str:
    """Ensure an 'output' subdirectory."""
    return ensure_dir(dir_name, base_dir=base_dir)

def ensure_logs_dir(dir_name: str = "logs", base_dir: str | None = None) -> str:
    """Ensure a 'logs' subdirectory."""
    return ensure_dir(dir_name, base_dir=base_dir)


def ensure_file(
    file_path: str,
    base_dir: str | None = None,
    mode: int = 0o644,
    content: str | None = None
) -> str:
    """
    Ensure a file exists. Creates parent directories and the file itself.

    Args:
        file_path (str): Path to the file.
        base_dir (str | None): Optional base directory for resolution.
        mode (int): Permissions for the file (default: rw-r--r--).
        content (str | None): Optional string to write if the file is newly created.

    Returns:
        str: Absolute path to the file.
    """
    abs_path = resolve_file_path(file_path, base_dir=base_dir)
    path_obj = Path(abs_path)

    # 1. Ensure the parent directory exists first
    ensure_dir(str(path_obj.parent), base_dir=base_dir)

    # 2. Create the file if it doesn't exist
    if not path_obj.exists():
        path_obj.touch(mode=mode, exist_ok=True)
        logger.info(f"Created empty file: {abs_path}")

        # 3. Optionally add initial content
        if content:
            path_obj.write_text(content, encoding='utf-8')
            logger.info(f"Initial content written to: {abs_path}")
    else:
        logger.debug(f"File already exists: {abs_path}")

    return abs_path


def save_to_csv(data, filepath):
    """Helper function to write a list of dicts to CSV, ensuring dir exists first."""
    if not data:
        return

    abs_path = Path(resolve_file_path(filepath))
    ensure_dir(str(abs_path.parent))

    keys = data[0].keys()
    with open(abs_path, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)

def append_to_csv(data, filepath):
    """Appends sanitized dicts to a CSV, ensuring one row per record."""
    if not data:
        return

    abs_path = Path(resolve_file_path(filepath))
    ensure_dir(str(abs_path.parent))
    
    # --- Sanitization Step ---
    # Replace newlines with a space or a comma to keep the data readable
    clean_data = []
    for row in data:
        clean_row = {
            k: (v.replace('\n', ' ').replace('\r', '').strip() if isinstance(v, str) else v)
            for k, v in row.items()
        }
        clean_data.append(clean_row)
    # -------------------------

    file_exists = abs_path.exists() and abs_path.stat().st_size > 0
    keys = clean_data[0].keys()

    with open(abs_path, 'a', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        if not file_exists:
            dict_writer.writeheader()
        dict_writer.writerows(clean_data)

# 🔍 Example usage (run only if script is main)
if __name__ == "__main__":
    # Example 1: Directory relative to current script (most common)
    data_dir = ensure_dir("../../Data/Processed")
    print("Data dir:", data_dir)

    # Example 2: With custom base
    custom_base = resolve_file_path("../..")  # e.g., project root
    cache_dir = ensure_dir("cache", base_dir=custom_base)
    print("Cache dir:", cache_dir)

    # Example 3: Fail if already exists
    try:
        ensure_dir("temp", exist_ok=False)
    except FileExistsError as e:
        print("Expected conflict:", e)

    # Example 4: Use convenience helpers
    out_dir = ensure_output_dir("results")
    print("Output dir:", out_dir)

    # Create an empty .gitkeep or placeholder file in a new directory
    placeholder = ensure_file("project/logs/.gitkeep")
    print("Created file at:", placeholder)

    # Create a file with initial headers/content
    config_file = ensure_file("config.ini", content="[DEFAULT]\nStatus = Active")
    print("Config file ready.")