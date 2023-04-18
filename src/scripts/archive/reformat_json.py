import json
import os
from datetime import datetime


def update_json_format(folder_path):
    paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".json") and not file[0:2] == "._":
                file_path = os.path.join(root, file)
                try:
                    paths.append(file_path)
                    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                        original_content = json.load(f)

                    updated_content = {
                        "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "data": original_content,
                    }

                    with open(file_path, "w", encoding="utf-8") as f:
                        json.dump(updated_content, f, indent=2)
                except Exception as e:
                    print(f"Error: {e} - {file_path}")

    print(len(paths))


def main():
    folder_path = "/Volumes/T7/db/json"
    update_json_format(folder_path)


if __name__ == "__main__":
    main()
