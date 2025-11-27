# API Reference

## Selectors
::: {{cookiecutter.project_slug}}.selectors
    options:
      members: true
      show_source: true
      filters:
        - "!^_"
      show_submodules: true

## Services
::: {{cookiecutter.project_slug}}.services
    options:
      members: true
      show_source: true
      filters:
        - "!^_"
      show_submodules: true

## Models
::: {{cookiecutter.project_slug}}.models
    options:
      members: true
      show_source: true
      filters:
        - "!^_"
      show_submodules: true

{% if cookiecutter.use_celery == "y" %}
## Tasks
::: {{cookiecutter.project_slug}}.tasks
    options:
      members: true
      show_source: true
      filters:
        - "!^_"
      show_submodules: true
{% endif %}
