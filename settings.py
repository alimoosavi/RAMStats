import yaml


def _load_settings():
    with open("settings.yml", "r") as file:
        return yaml.safe_load(file)


SETTINGS = _load_settings()
