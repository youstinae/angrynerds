import os


def get_app_base_path():
    return os.path.abspath(os.path.dirname(__file__))


def get_instance_folder_path():
    return os.path.join(get_app_base_path(), 'instance')
