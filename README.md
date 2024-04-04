# British National Library Scraper

*Created by Benjamin Eyal, April 2024.*

This program scrapes the catalog of the interim British National Library for technical items published between 1500 and 1930.

The program records the following data for each item:
- Title
- Publication Year
- Subject (query)

## Search details
The searches made by this scraper are equivalent to filling out the following fields in the advanced search (http://catalogo.bne.es/uhtbin/webcat) form of the catalog:
- [x] Years Published/Created: From 1500 to 1930 
- [x] Type of Material: Book
- [x] Subject = Query input
- [x] Language: Englidh

The scraper will scrape all of the results pages. If a search does not have any results, the program will not have any output. If it does, it will output a CSV of the results 

## Saving Results
The program will save a csv to your working directory that removes entries that are duplicates of another (Primary key = Year, Title)

## Functions
If you want to scrape a topic, or group of topics, load the functions in BritishScraperfunctions.R to your workspace. Then, run the following full code of BritishScraperMain.py:
```py
import BritainScraperFunctions as scraper
import pandas as pd 


#picks the list of subjects to scrape
Subject_List = ["Technology","Engineering", "Construction", "Civil engineering", "Architecture", "Mechanical engineering", "Nuclear engineering", "Electrical engineering", "Electronic engineering", "Maritime engineering", "Naval engineering", "Metal engineering","Mining engineering", "Chemical technology", "Manufacturing","Domestic arts", "Domestic sciences", "Industry","Commerce","Agriculture","Horticulture","Silk industry","Animal husbandry","Forestry","Fishing","Transportation","Traffic","Communications"]

df = scraper.Main_Function(Subject_List)

df.to_csv("FullBritishSearch.csv")
```
The function MainFunction is structured as follows:
1. Navigates through selenium from the search page to the first page of the results
2. Extract the number of results pages associated with that search.
3. Loop through each page number and:
   1. Extract the source code from the page.
   2. Iterate to the next page
4. Parse the HTML into a dataframe with the required results for each page
5. Collect all the dataframes into a single dataset
6. returns and collects the first version from all multiple versions pages
7. Clean the dataframe
8. Assign the subject category
9. Return the dataset


# Notes on results: The results remove duplicates on (Primary key = Title, Year), and removes books without years (coerced to year = 0). The most common reason why a book is coerced to 0 is that it has multiple versions. All titles with multiple versions are accounted for by the Find_Duplicates function and added after the subject. The zero entries are then removed. 