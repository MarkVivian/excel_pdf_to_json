import os

import refurbish_info


class Scripter:
    def __init__(self):
        self.cleaned_data = refurbish_info.Refurbish.read_from_json("./json_files/cleaned.json")
        self.sql_script_data = []
        self.write_script()
        self.file_name = "./json_files/sql_script.sql"
        self.write_to_txt()

    def write_script(self):
        for item in self.cleaned_data:
            ippd = item["employee"]["payroll number"]
            for relations in item["employee info"]:
                information = {
                    "ippd": ippd,
                    "firstname": relations["first name"],
                    "middlename": relations["middle name"],
                    "surname": relations["surname"],
                    "dob": relations["date of birth"],
                    "relationship": self.relationship_handler(relations["relationship"])
                }

                self.sql_script_data.append(information)

    @staticmethod
    def relationship_handler(relationship):
        if relationship == "SPOUSE":
            real = 1
        elif relationship == "DAUGHTER":
            real = 3
        elif relationship == "SON":
            real = 2
        else:
            real = 0
        return real

    def generate_insert_sql(self):
        sql_template = """
        INSERT INTO `dependancy` (`ippd`, `firstname`, `middlename`, `surname`, `dob`, `status`, `relationship`, `covernumber`, `year`)
        VALUES
        """

        sql_values = []
        for record in self.sql_script_data:
            ippd = record.get("ippd", "")
            firstname = record.get("firstname", "")
            middlename = record.get("middlename", "")
            surname = record.get("surname", "")
            dob = record.get("dob", "")
            status = 1
            relationship = record.get("relationship", "")
            covernumber = ""
            year = 0

            sql_values.append(
                '("{}", "{}", "{}", "{}", "{}", "{}", "{}", "{}", {})'.format(
                    ippd, firstname, middlename, surname, dob, status, relationship,
                    covernumber, year
                )
            )

        return sql_template + ",\n".join(sql_values)

    def write_to_txt(self):
        data = self.generate_insert_sql()
        if not isinstance(data, (str, list)):
            raise ValueError("Data must be a string or a list of strings.")

        try:
            # Create the directory if it doesn't exist
            os.makedirs(os.path.dirname(self.file_name), exist_ok=True)

            with open(self.file_name, "w") as file:
                if isinstance(data, str):
                    file.write(data)
                elif isinstance(data, list):
                    file.write("\n".join(data))
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Error writing to file: {self.file_name}") from e
