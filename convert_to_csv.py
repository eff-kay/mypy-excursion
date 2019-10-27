import sys
import json,csv


if __name__ == "__main__":    
    json_file_name = sys.argv[1]
    csv_file_name = sys.argv[2]

    jsonD = json.load(open(json_file_name))
    field_names  = list(jsonD[0].keys())

    csv_file = open(csv_file_name, 'w')
    for item in jsonD:
        writer = csv.DictWriter(csv_file, fieldnames=field_names)
        writer.writerow(item)