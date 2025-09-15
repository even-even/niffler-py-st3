from dynaconf import Dynaconf


def get_settings(env: str = "default") -> Dynaconf:
    return Dynaconf(
        env=env,
        settings_files=[
            "./settings.toml",
            "./.secrets.toml"
        ],
        environments=True,
        merge_enabled=True
)
