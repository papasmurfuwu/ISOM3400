import csv 

with open('data.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    with open('new_data.csv', 'w') as new_file:
        fieldnames = ['Name', 'Capital', 'Population']
        csv_writer = csv.DictWriter(new_file, fieldnames=fieldnames, delimiter='\t')

        for line in csv_reader:
            csv_writer.writerow(line)

