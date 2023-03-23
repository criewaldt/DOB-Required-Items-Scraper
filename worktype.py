import os
import csv
from bs4 import BeautifulSoup
import datetime

# Define the folder to search
rootdir = "worktypes"

def scrape_requirements(html_file, job_number, worktype, output_list):
    with open(html_file, "r", encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    requirements_table = soup.find_all('table')[3]
    trs = requirements_table.find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        item_name = tds[0].text.strip()
        prior_to = tds[2].text.strip()
        output_list.append([worktype, job_number, item_name, prior_to])
    return output_list

def write_requirements_to_csv(worktype, requirements_list):
    #create a csv file of successful job data
    today = datetime.date.today()
    output_location = 'output/WorkType Requirements - {} - {}.csv'.format(worktype, today.strftime('%Y-%m-%d'))
    with open(output_location, 'w', newline="") as f:
        writer = csv.writer(f)
        writer.writerows(requirements_list)
    print('Wrote requirements CSV to file: {}'.format(output_location))

if __name__ == "__main__":
    
    # Traverse each subfolder within the folder
    for subdir, dirs, files in os.walk(rootdir):
        #fresh requirements output list
        requirements_output = []

        for file in files:
            # print(subdir, file)

            worktype = subdir.split("\\")[1]
            job_number = file.split(".html")[0]
            file_path = os.path.join(subdir, file)

            print('..loading the following:', worktype, job_number, file_path)
            
            #do the scrape
            requirements_output = scrape_requirements(file_path, job_number, worktype, requirements_output)
    
        #write the file when done
        write_requirements_to_csv(worktype, set(requirements_output))
    
print('Done.')