import yaml


class Config:
    @staticmethod
    def from_file(location: str):
        with open(location, "r") as file:
            return yaml.safe_load(file)


if __name__ == "__main__":
    config = Config.from_file("../../config.yml")
    print(config)
