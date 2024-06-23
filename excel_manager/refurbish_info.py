import json


class Refurbish:
    def __init__(self):
        self.file_path = "./json_files/info.json"
        self.repeating_path = "./json_files/repeating.json"
        self.cleaned_path = "./json_files/cleaned.json"

    @staticmethod
    def write_to_json(filepath, data):
        with open(filepath, "w") as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def read_from_json(filepath):
        with open(filepath, "r") as file:
            data = json.load(file)
        return data

    def check_redundancy(self):
        info = []
        clean = []
        data = self.read_from_json(self.file_path)
        for i in range(len(data)):
            print(f"{i}")
            j = i + 1
            if j < len(data):
                if data[i] == data[j]:
                    info.append(data[i])
                else:
                    clean.append(data[i])
        self.write_to_json(self.cleaned_path, clean)
        self.write_to_json(self.repeating_path, info)
