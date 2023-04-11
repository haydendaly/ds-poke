import os


def swap_files(path_0, path_1):
    os.rename(path_0, path_0 + ".temp")
    os.rename(path_1, path_0)
    os.rename(path_0 + ".temp", path_1)
