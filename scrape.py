import os
import csv
from bs4 import BeautifulSoup

def scrape_requirements(html_file):
    output_list = []
    with open(html_file, "r", encoding='utf-8') as f:
        html = f.read()
    soup = BeautifulSoup(html, 'html.parser')
    requirements_table = soup.find_all('table')[3]
    trs = requirements_table.find_all('tr')[1:]
    for tr in trs:
        tds = tr.find_all('td')
        for i, td in enumerate(tds):
            print(i, td.text.strip())
        input()
        item_name = tds[0].text.strip()
        prior_to = tds[2].text.strip()
        
        #date_certified = tds[5].strip()

        output_list.append(item_name)
    return output_list

def write_requirements(worktype, requirements_list):
    with open('output/{}.csv'.format(worktype), mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        for row in requirements_list:
            writer.writerow([row])
    print('Successfully created requirements list for {}'.format(worktype))

# Define the folder structure
main_folder = "input"

def main():
    worktypes = []

    # Get all worktype folders from the main folder
    for item in os.listdir(main_folder):
        # Check if the item is a directory/folder
        if os.path.isdir(os.path.join(main_folder, item)):
            # Add the folder name to the list
            worktypes.append(item)
    print('Found {} worktype folders.'.format(len(worktypes)))

    # Loop over each worktype folder
    for worktype in worktypes:
        # Define the output CSV filename
        csv_filename = worktype + ".csv"

        required_items_output = []

        # Loop over each HTML file in the worktype folder
        for filename in os.listdir(os.path.join(main_folder, worktype)):
            if filename.endswith(".html"):
                
                #load html file
                html_file = os.path.join(main_folder, worktype, filename)
                requirements = scrape_requirements(html_file)

                for requirement in requirements:
                    if requirement not in required_items_output:
                        required_items_output.append(requirement)
        
        #only unique required items should be passed
        required_items_output = set(required_items_output)

        #write requirements csv for worktype
        write_requirements(worktype, required_items_output)

    print('Done.')

if __name__ == "__main__":
    pass