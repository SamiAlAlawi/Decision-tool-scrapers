"""
Masters degree webscraper by Sami

Program iterates through course names in the course_masters txt files 
and scrapes the desired information, producing a csv file with the fields:
(course name, duration, eu fees, international fees, entry requirements, about)
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

def scrape(course_name, part_time):
    """ Does the actual scraping

    parameters
    ----------
        course_name : str = name of the course being scraped
        part_time: boolean - Two different page structures depending if the course is part time or not

    returns
    -------
        None - Output written directly to csv file
    """
    #setting up the connection
    url = "https://www.ucl.ac.uk/prospective-students/graduate/taught-degrees/" + course_name.replace(" ", "-")
    uClient = uReq(url)
    page_html = uClient.read()
    uClient.close()
    page_soup = soup(page_html, "html.parser")

    #getting the important fields
    try:
        #indexing the duration data
        data_in_divs = page_soup.findAll("div" , {"class" : "clearfix"})
        duration_data = data_in_divs[5].div.findAll("div")
        duration = duration_data[0].text.strip()
        if part_time:
            duration = duration + " or " + duration_data[1].text.strip()

        #indexing the fee data. Structure changes if part time
        fee_data = data_in_divs[6].findAll("div")
        if part_time:
            EU_fees = fee_data[2].text.strip().replace("," , ";") + fee_data[3].text.strip().replace("," , ";")
            international_fees = fee_data[6].text.strip().replace("," , ";") + fee_data[6].text.strip().replace("," , ";")
        else:
            EU_fees = fee_data[2].text.strip().replace("," , ";")
            international_fees = fee_data[5].text.strip().replace("," , ";")

        section_entryReq = page_soup.findAll("div", {"class" : "col--1-2-lg-content"})
        entry_requirements = section_entryReq[2].p.text.replace("," , ";").replace("\n" , "")

        section_about = page_soup.findAll("div", {"class" : "collapse__content"})
        about = section_about[0].p.text.replace("," , ";").replace("\n" , "")

        #writing the fields to the csv file
        f.write(course_name + "," + duration + "," + EU_fees + "," + international_fees + "," + entry_requirements + "," + about + "\n")
    except (IndexError) as error:
        f.write(course_name + ", na, na, na, na, na, na \n")


#setting up the csv file and the file with courses
f = open("TaughtMasters.csv" , "w")
f_courseNames = open("courses_masters.txt", "r")
f_courseNamesWithPartTime = open("courses_masters2.txt", "r")

headers = "course name, duration, eu fees, international fees, entry requirements, about \n"
f.write(headers)

for course in f_courseNames:
    scrape(course.strip(), False)
    #keep track of progress
    print(course.strip())

for course in f_courseNamesWithPartTime:
    scrape(course.strip(), True)
    #keep track of progress
    print(course.strip())

f.close()
f_courseNames.close()
f_courseNamesWithPartTime.close()