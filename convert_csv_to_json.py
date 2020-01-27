import sys
import json,csv


if __name__ == "__main__":    
    csv_file_name = sys.argv[1]
    json_file_name = sys.argv[2]

    jsonD = []

    with open(csv_file_name) as csv_file:
        csv_reader = csv.reader(csv_file)
        count=0
        for row in csv_reader:
            # if count==3:
            #     break
            # count+=1
            data={}
            data['url'] = row[0]
            data['repo_name'] = row[1]
            data['labels'] = row[2]
            data['action'] = row[3]
            jsonD.append(data)
    print("done")
    
    with open(json_file_name, 'w') as json_file:
        json_file.write(json.dumps(jsonD, indent=4))