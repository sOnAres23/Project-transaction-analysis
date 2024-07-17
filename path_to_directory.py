import os


def find_directory(path: str = os.getcwd(), recursive_counting: str | int = None) -> dict:
    """Функция, которая смотрит путь директории и
    возвращает кол. папок и файлов"""
    directory_count = {"files": 0, "folders": 0}
    if os.path.isdir(path) is True:
        find_dir = os.scandir(path)
        for file in find_dir:
            if os.path.isfile(file) is True:
                directory_count['files'] += 1
            if os.path.isdir(file) is True:
                directory_count['folders'] += 1

    if recursive_counting is not None:
        for root, dirs, files in os.walk(path):
            for name in files:
                print(os.path.join(root, name))
            for name in dirs:
                print(os.path.join(root, name))
    return directory_count


if __name__ == "__main__":
    print(find_directory())