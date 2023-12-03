



import re

import csv




# Using regex to extract the list of baby names from the babies1990.html file
def baby_names_extraction(file_path):
    with open(file_path, 'r') as file:
        html_content = file.read()

    pattern = re.compile(r'<td>([0-9]+)</td>\s*<td>([A-Za-z]+)</td>\s*<td>([A-Za-z]+)</td>')

    baby_names = re.findall(pattern, html_content)

    # Make a tuple with only the Popularity rank, and Female name columns
    result = [(match[0], match[2]) for match in baby_names]


    return result

# Define the file path parameter  for the baby names extraction function
file_path = 'babies1990.html'
baby_names = baby_names_extraction(file_path)






def create_new_csv_file(baby_names):
    baby_names = baby_names_extraction(file_path)

    csv_file_path = 'baby_names.csv'

    # Write data to the CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',')
    
        # Write header to the CSV file
        csv_writer.writerow(['Popularity Rank', 'Name'])
    
        # Write data to the CSV file
        csv_writer.writerows(baby_names)

    return f'Data has been written to {csv_file_path}.'

print(create_new_csv_file(baby_names))



