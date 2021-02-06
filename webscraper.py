"""
Undergraduate webscraper by Sami

Program iterates through course names in the undergraduate txt files 
and scrapes the desired information, producing a csv file with the fields:
(course_name, duration, entry_requirement_Alevel_grades, entry_requirement_Alevel_subjects, IB_grades, IB_requirements, EU_fees, International_fees, course_description, course url, accreditation)
"""

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq


def scrape(name, offset):
    """ Does the actual scraping

    parameters
    ----------
        name : str = name of the course being scraped
        offset: boolean - Two different page structures, offset helps correct indexing between these

    returns
    -------
        None - Output written directly to csv file
    """

    #html tags are slightly different based on the courses on the website. Offset handles this issue
    if offset:
        offsets = [1,2]
    else:
        offsets = [0,0]
    
    #create the url parameter
    base_url = "https://www.ucl.ac.uk/prospective-students/undergraduate/degrees/"
    course_name = course.strip()
    course_url = base_url + course_name.replace(" ","-")
    
    #opening a connection, grabbing the page
    uClient = uReq(course_url)
    page_html = uClient.read()
    uClient.close()

    #beautiful soup is used to tidy up the html in the page_html (html parsing)
    page_soup = soup(page_html, "html.parser")

    try:
        #get the html elements that contain the important details
        course_name = page_soup.h1.text
        most_data = page_soup.findAll("dd")
        duration = most_data[1].text.strip()
        entry_requirement_grades = most_data[4 + offsets[0]].text
        #output is to csv file, so replace all the commas with a semicolon
        entry_requirement_subjects = most_data[5 + offsets[0]].text.replace("," , ";")
        IB_entry_grades = most_data[10 + offsets[0]].text
        IB_entry_requirements = most_data[11 + offsets[0]].text.replace("," , ";")
        EU_fees = most_data[14 + offsets[1]].text.replace("," , ";")
        International_fees = most_data[15 + offsets[1]].text.replace("," , ";")
        intro = page_soup.findAll("p", {"class":"copy__intro"})
        course_description = intro[0].text.strip().replace("," , ";")

        #accreditation depends on the different web pages (offset)
        if offset:
            accreditiation = most_data[2].text
        else:
            accreditiation = "none"
    
        #write all of this to the csv file. Need to make sure there are no ','
        f_out.write(course_name + "," + duration + "," + entry_requirement_grades + "," + entry_requirement_subjects + "," + IB_entry_grades + "," + IB_entry_requirements + "," + EU_fees + "," + International_fees + "," + course_description + "," + course_url + "," + accreditiation + "\n")
    
    except (IndexError) as error:
        #fill in n/a values. We can fill them in manually later
        f_out.write(course_name + ", n/a, n/a, n/a, n/a, n/a, n/a, n/a, n/a, n/a \n")



#creating the csv file to write to, and getting the course names from the txt file.
#Also, defining the base url that is shared for each course
filename = "undergradCourses.csv"
f_out = open(filename, "w")
f_courses = open("courses_undergrad.txt","r")
f_courses2 = open("courses_undergrad2.txt", "r")
headers = "course_name, duration, entry_requirement_Alevel_grades, entry_requirement_Alevel_subjects, IB_grades, IB_requirements, EU_fees, International_fees, course_description, course url, accreditation, ucl API courseID \n"
f_out.write(headers)


for course in f_courses:
    scrape(course, False)
    #see progress in terminal
    print(course.strip())
f_courses.close()

#doing the same thing for the other txt file for undergrad. This is because some pages have different html layouts
for course in f_courses2:
    scrape(course, True)
    #see progress in terminal
    print(course.strip())
f_courses2.close()

f_out.close()