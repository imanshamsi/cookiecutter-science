import os
import shutil


BASE_DIR = os.getcwd()

FEATURES = {
    "celery": {
        "flag": "{{ cookiecutter.use_celery }}",
        "paths": [
            os.path.join(BASE_DIR, "config", "celery.py"),
            os.path.join(BASE_DIR, "config", "utils", "celery.py"),
            os.path.join(BASE_DIR, "{{ cookiecutter.project_slug }}", "tasks"),
            os.path.join(BASE_DIR, "{{ cookiecutter.project_slug }}", "setup.py"),
        ],
    },
    # Add more features here later ...
}


def remove_paths(paths):
    for path in paths:
        if not os.path.exists(path):
            continue
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.isdir(path):
            shutil.rmtree(path)


def main():
    # Celery
    if FEATURES["celery"]["flag"].lower() != "y":
        remove_paths(FEATURES["celery"]["paths"])


if __name__ == "__main__":
    main()
