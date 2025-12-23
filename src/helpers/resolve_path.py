import os

def resolve_file_path(file_path, base_dir=None):
    """
    Resolve a file path from different possible input formats.

    Args:
        file_path: Can be:
            - Absolute path (e.g., "/home/user/data/file.json")
            - Relative path from current directory (e.g., "data/file.json")
            - Path relative to this script (e.g., "../../Data/file.json")
            - Path relative to a specified base directory
        base_dir: Optional base directory for relative paths. If None,
                  uses the directory of the calling script.

    Returns:
        Absolute path to the file

    Example usage:
        # Relative to this script
        json_file = resolve_file_path("../../Data/Alternative_Names.json")

        # Relative to current working directory
        json_file = resolve_file_path("Data/Alternative_Names.json")

        # With custom base directory
        json_file = resolve_file_path("Alternative_Names.json", base_dir="/my/base/dir")
    """
    # If it's already an absolute path, return it as-is
    if os.path.isabs(file_path):
        return os.path.abspath(file_path)

    # If base_dir is provided, use it
    if base_dir is not None:
        return os.path.abspath(os.path.join(base_dir, file_path))

    # Otherwise, use the directory of the calling script (like in your original code)
    # Get the directory of the script that called this function
    import inspect
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    caller_dir = os.path.dirname(os.path.abspath(caller_file))

    return os.path.abspath(os.path.join(caller_dir, file_path))


# More specialized versions for common use cases:

def resolve_from_script(file_path):
    """Resolve path relative to the calling script's directory."""
    import inspect
    caller_frame = inspect.stack()[1]
    caller_file = caller_frame.filename
    caller_dir = os.path.dirname(os.path.abspath(caller_file))
    return os.path.abspath(os.path.join(caller_dir, file_path))


def resolve_from_module(file_path, module_file):
    """Resolve path relative to a specific module file."""
    module_dir = os.path.dirname(os.path.abspath(module_file))
    return os.path.abspath(os.path.join(module_dir, file_path))


def resolve_from_cwd(file_path):
    """Resolve path relative to current working directory."""
    return os.path.abspath(file_path)


# Usage examples:
if __name__ == "__main__":
    # Original style usage
    json_file = resolve_from_script("../../Data/Alternative_Names.json")
    print("File path:", json_file)

    # More flexible usage
    json_file = resolve_file_path("../../Data/Alternative_Names.json")
    print("File path:", json_file)

    # Or if you want to be explicit about the base
    json_file = resolve_file_path("Alternative_Names.json",
                                 base_dir=os.path.join(os.path.dirname(__file__), "../../Data"))
    print("File path:", json_file)