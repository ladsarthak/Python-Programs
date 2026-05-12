import json
import os
import time

def notepad():
    data = input("Start Typing (Press Enter to finish): ")
    if data == "":
        print("No data entered. Exiting.")
        time.sleep(2)
        exit()
    elif data == "XXX":
        print("Exiting.")
        time.sleep(2)
        exit()

    current_directory = os.getcwd()

    name = input("Enter a name for the file (without extension): ")
    if name == "":
        print("No name entered. Exiting.")
        time.sleep(2)
        return
    elif name == "XXX":
        print("Exiting.")
        time.sleep(2)
        exit()

    extension = input("Enter the file extension (exclude period (.)): ")
    if extension == "":
        print("No extension entered. Exiting.")
        time.sleep(2)
    elif extension == "XXX":
        print("Exiting.")
        time.sleep(2)
        exit()

    name_extension = f"{name}.{extension}"

    file_path = os.path.join(current_directory, name_extension)

    with open(file_path, "w") as file:
        if extension == "json":
            json.dump(data, file, indent=4)
        else:
            file.write(str(data))

    print(f"File '{name_extension}' has been created in the directory: {current_directory}")
    notepad()
notepad()