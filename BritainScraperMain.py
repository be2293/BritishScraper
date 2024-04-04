import BritainScraperFunctions as scraper
import pandas as pd 


#picks the list of subjects to scrape
Subject_List = ["Technology","Engineering", "Construction", "Civil engineering", "Architecture", "Mechanical engineering", "Nuclear engineering", "Electrical engineering", "Electronic engineering", "Maritime engineering", "Naval engineering", "Metal engineering","Mining engineering", "Chemical technology", "Manufacturing","Domestic arts", "Domestic sciences", "Industry","Commerce","Agriculture","Horticulture","Silk industry","Animal husbandry","Forestry","Fishing","Transportation","Traffic","Communications"]

df = scraper.Main_Function(Subject_List)

df.to_csv("FullBritishSearch.csv")
