from threading import Lock

file_data = {}
read_lock = Lock()


def _read_from_file(filepath):
    with read_lock:
        if filepath in file_data:
            return

        print(f'lazy reading... ({filepath})')
        with open(filepath, 'r') as file_handle:
            file_data[filepath] = file_handle.read()


def get_file_data(filepath):
    if filepath in file_data:
        return file_data[filepath]

    _read_from_file(filepath)
    return file_data[filepath]


__all__ = [
    'get_file_data'
]