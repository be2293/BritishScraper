from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import math
from bs4 import BeautifulSoup
import pandas as pd 
from time import sleep
import re

#instantiates a driver
driver = webdriver.Firefox()


#Manuevers to the first page and extracts the number of pages associated with a query
def Get_Page_Number(subject):
    url = "https://bll01.primo.exlibrisgroup.com/discovery/search?query=sub,contains,"+subject+",AND&pfilter=lang,exact,eng,AND&pfilter=rtype,exact,books,AND&pfilter=dr_s,exact,15000101,AND&pfilter=dr_e,exact,19301231,AND&tab=LibraryCatalog&search_scope=Not_BL_Suppress&vid=44BL_INST:BLL01&lang=en&mode=advanced&offset=0"
    driver.get(url)
    sleep(5)
    driver.execute_script("return document.documentElement.outerHTML")
    try:
        Text_Of_Entries = driver.find_element(By.XPATH, "/html/body/primo-explore/div/prm-explore-main/ui-view/prm-search/div/md-content/div[2]/prm-facet/div/div/div[5]/prm-facet-group/div/prm-facet-exact/div/div/div/div/strong/span[2]").text
        Number_Of_Entries = int(Text_Of_Entries.replace(",", ""))
    except:
        Number_Of_Entries = 0
    Number_Of_Pages = math.ceil(Number_Of_Entries/10)
    return Number_Of_Pages

#Iterates through a subject and extracts the HTML of each, with all dynamic text. 
def Get_HTML(subject):

    #Navigates to and find the page number of the query
    Number_Of_Pages = Get_Page_Number(subject)
    HTML_List = []
    if Number_Of_Pages == 0:
        return HTML_List
    for x in range(0, Number_Of_Pages):
        try:
            url = "https://bll01.primo.exlibrisgroup.com/discovery/search?query=sub,contains,"+subject+",AND&pfilter=lang,exact,eng,AND&pfilter=rtype,exact,books,AND&pfilter=dr_s,exact,15000101,AND&pfilter=dr_e,exact,19301231,AND&tab=LibraryCatalog&search_scope=Not_BL_Suppress&vid=44BL_INST:BLL01&lang=en&mode=advanced&offset="+str(10*x)
            driver.get(url)
            sleep(5)
            HTML_List.append(driver.execute_script("return document.documentElement.outerHTML"))
        except:
            HTML_List = []
            break
    return HTML_List

#extracts title and year from an html object
def Parse_HTML(response):
    #opens a parser
    soup = BeautifulSoup(response, "html.parser")
    
    #finds the elements corresponding to each item
    Xpath_Expression = 'html>body>primo-explore>div>prm-explore-main>ui-view>prm-search>div>md-content>div>prm-search-result-list>div>div>div>div>prm-brief-result-container>div>div>prm-brief-result'
    Element_List = soup.select(Xpath_Expression)
    
    #extracts title and year from each item
    Title_List = []
    Year_List = []
    for element in Element_List:
        Element_Disc = []
        for child in element.find_all(recursive=False):
            if child.text.strip():
                Cleaned_Element = child.text.strip().replace(';', '').replace('\n', '').replace('\t', '')
                Element_Disc.append(Cleaned_Element)
        Year_List.append(re.sub(r'[^0-9-]','',Element_Disc[-1]))
        Title_List.append(Element_Disc[0])
    
    #ensures the correct year is found, NA = 0
    for i in range(len(Year_List)):
        if len(Year_List[i]) != 4:
            Year_List[i] = 0
    
    #returns a dataframe
    if len(Title_List) == len(Year_List):
        Page_Data = pd.DataFrame({"Title":Title_List, "Year":Year_List})
        print(Page_Data)
    else:
        Page_Data = pd.DataFrame()
        print(Page_Data)
    return Page_Data

#Searchs a subject. Gets all the html and then parses and concatenates it all 
def Search_Subject(subject):
    HTML_List = Get_HTML(subject)
    if HTML_List == []:
        return 
    Df_List = []
    for index, item in enumerate(HTML_List):
        Page_List = Parse_HTML(item)
        Page_List["Page Number"] = index
        Df_List.append(Page_List)
    Raw_Data = pd.concat(Df_List, ignore_index=True)
    Raw_Data["Subject"] = subject
    return Raw_Data

#retrieves the first version associated with any entry with the "multiple versions" error
def Find_Duplicate(subject):
    #gets page numbers
    Number_Of_Pages = Get_Page_Number(subject)

    #initiates lists
    HTML_List = []
    Year_List = []
    Title_List = []

    #goes through each page of a subject, and gets the HTML of each page associated with a "Multiple Versions" entry
    for x in range(0, Number_Of_Pages):
        url = "https://bll01.primo.exlibrisgroup.com/discovery/search?query=sub,contains,"+subject+",AND&pfilter=lang,exact,eng,AND&pfilter=rtype,exact,books,AND&pfilter=dr_s,exact,15000101,AND&pfilter=dr_e,exact,19301231,AND&tab=LibraryCatalog&search_scope=Not_BL_Suppress&vid=44BL_INST:BLL01&lang=en&mode=advanced&offset="+str(10*x)
        driver.get(url)
        sleep(5)
        driver.execute_script("return document.documentElement.outerHTML")
        elements = driver.find_elements(By.XPATH,"//span[@translate='nui.frbrversion.found']")
        for i in range(len(elements)):
            try:
                driver.find_elements(By.XPATH,"//span[@translate='nui.frbrversion.found']")[i].click()
                sleep(5)
                HTML_List.append(driver.execute_script("return document.documentElement.outerHTML"))
                driver.back()
            except:
                sleep(5)
            sleep(5)
    
    #Creates year and titles lists associated with the new entries
    for item in HTML_List:
        soup = BeautifulSoup(item, "html.parser")
        Xpath_Expression = 'html>body>primo-explore>div>prm-explore-main>ui-view>prm-search>div>md-content>div>prm-search-result-list>div>div>div>div>prm-brief-result-container>div>div>prm-brief-result'
        
        #finds each element and strips out title and year
        element = soup.select(Xpath_Expression)[0]
        Element_Disc = []     
        for child in element.find_all(recursive=False):
            if child.text.strip():
                Cleaned_Element = child.text.strip().replace(';', '').replace('\n', '').replace('\t', '')
                Element_Disc.append(Cleaned_Element)
        print(Element_Disc[0])
        Year_List.append(re.sub(r'[^0-9-]','',Element_Disc[-1]))
        Title_List.append(Element_Disc[0])
    
    #removes entries with errors
    for i in range(len(Year_List)):
        if len(Year_List[i]) != 4:
            Year_List[i] = 0
    Page_Data = pd.DataFrame({"Title":Title_List, "Year":Year_List})
    return Page_Data


#Searches all subjects and then adds in the multiple versions check, and then removes yearless entries. 
def Main_Function(Subject_List):
    Df_List = []
    for subject in Subject_List:
        Df_List.append(Search_Subject(subject))
        Duplicate_Frame = Find_Duplicate(subject)
        Duplicate_Frame["Subject"] = subject
        Df_List.append(Duplicate_Frame)
    FullDataFrame = pd.concat(Df_List)
    DuplicatesRemovedDataFrame = FullDataFrame.drop_duplicates(subset=['Title','Year'], keep = 'first')
    ZerosRemovedDataFrame = DuplicatesRemovedDataFrame[DuplicatesRemovedDataFrame["Year"] != 0]
    return ZerosRemovedDataFrame
