import json

def read_json_file(path: str) -> dict:
    """
    Reading json file into a dictionary
    :param path: Path to json file
    :return dict: dict result
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            paths = json.load(f)
        return paths
    except Exception as ex:
        print(f"Failed to read json file: {ex}")


def write_json_file(path: str, input_dict: dict) -> None:
    """
    Writing input dict to a json file
    :param path: Path to json file
    :param input_dict: input dict
    :return:
    """
    try:
        with open(path, 'w', encoding="utf-8") as f:
            json.dump(input_dict, f, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"Failed to write json file: {ex}")
