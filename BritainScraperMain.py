import BritainScraperFunctions as scraper
import pandas as pd 

#instantiates a list to put the data in
Df_List = []

#picks the list of subjects to scrape
Subject_List = ["Agriculture", "Engineering", "Electricity"]

for subject in Subject_List:
    Df_List.append(scraper.Search_Subject(subject))

#gets both a raw and duplicates-removed frame 
FullDataFrame = pd.concat(Df_List)
DuplicatesRemovedDataFrame = FullDataFrame.drop_duplicates(subset=['Title','Year'], keep = 'first')

#saves frames to your computer 
FullDataFrame.to_csv("FullBritishData.csv")
DuplicatesRemovedDataFrame.to_csv("CleanBritishData.csv")