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
    "mkdocs": {
        "flag": "{{ cookiecutter.use_mkdocs }}",
        "paths": [
            os.path.join(BASE_DIR, "mkdocs.yml"),
            os.path.join(BASE_DIR, "docs"),
        ]
    },
    "pytest": {
        "flag": "{{ cookiecutter.use_pytest }}",
        "paths": [
            os.path.join(BASE_DIR, "pytest.ini"),
            os.path.join(BASE_DIR, "{{ cookiecutter.project_slug }}", "tests"),
        ]
    }
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

    # MKDocs
    if FEATURES["mkdocs"]["flag"].lower() != "y":
        remove_paths(FEATURES["mkdocs"]["paths"])

    # Pytest
    if FEATURES["pytest"]["flag"].lower() != "y":
        remove_paths(FEATURES["pytest"]["paths"])


if __name__ == "__main__":
    main()
