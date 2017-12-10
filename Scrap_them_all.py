
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from time import sleep
import pandas as pd 


# ## Loading the web page and click on more 

# In[2]:


def load_root_page (url,chrome_path,nombre):
	#Opens a Web Page in Chrome
	chrome_options = webdriver.ChromeOptions()
	# This is to stop the Chrome window from opening up ( --headless )
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
	driver.get(url)
# nombre is number of clicks to make on the more button in the web page each click generates 9 more articles
	for i in range(nombre):
		moreButton = driver.find_element_by_css_selector("#psirtMore > a")
		moreButton.click()
		sleep(0.3) #even 0.25 is not enough to get results back before the next click
	soup = BeautifulSoup(driver.page_source, "html.parser")
	return soup


# ## Lists all links and scrap them

# In[3]:


def scrap_root_page(soup):
    for record in soup.findAll('tr'): #look for the liste table in the source
        i=0
        for data in record.findAll('td'): #write them in the center 
            site = data.find('a', href=True) #
            if (i==0):
                center[i] = base + site['href'] #give the url of the article
                i+=1
            else:
                center[i] = data.text.strip() 
                center[i] = center [i]
                i+=1
        if center[0] is not None:
            scrap_article(center[0],center) #scrap the article and write it in the center
            if not(all(v is None for v in center)):
                df_centers.loc[len(df_centers.index)] = center


# ## Function to scrap one article

# In[4]:


def scrap_article(url,center):
    thepage = urllib.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    all_details = soup.findAll('div',attrs={'class':'psirt-set-out'}) #All information needed is in this class
    i=3 # the first 3 elements are written from the list page 
    for detail in all_details: # write all the information
        contenu =  detail.find('div',attrs={'class':'moreinfo'})
        tableau = contenu.findAll('tr')
        if tableau:
            center[i]=scrap_tableau_details(tableau)
            i+=1
            continue
        center[i] = contenu.text.strip()
        i+=1


# ### Function to scrap the Software affected and its versions

# In[5]:


#this table is written in the center as multiple lines as follows [product names, version1; version 2 etc...,upgrade version]
def scrap_tableau_details(tableau): 
    infos=["Prodcut Name","Versions","Upgrade"]
    info_totale=""
    for ligne in tableau[1:]:
            champs = ligne.findAll('td')
            if len(champs) == 3:
                info_totale = info_totale + "[" + infos[0] + "," + infos[1] + "," + infos[2] + "]" + "\n"
                infos=["","",""]
                i=0
                for champ in champs:
                    infos[i]=champ.text.strip()
                    i+=1    
            else:
                for champ in champs:
                    infos[1]=infos[1]+ "; " +champ.text.strip()
    return info_totale 


# ## Create the Dataframe Columns 

# In[6]:


df_centers = pd.DataFrame(columns=['Url', 'Title', 'Version','Summary','Software Versions and Fixes','Affected Versions','Resolved product and Version','Impact','Vulnerability Scoring Details','Technique Details','Temporary Fix','Obtaining Fixed Software','Source','Revision History','FAQs','Huawei Security Procedures','Declaration'])
center = [None] * 17


# ## Initialize parameters

# In[7]:


url="http://www.huawei.com/en/psirt/security-advisories"
chrome_path="/Users/abderrahmane/Desktop/Divers/scrap/chromedriver"
base="http://www.huawei.com"


# In[9]:


#choose the number of clicks on the more button according to the need
nombre=5
soup=load_root_page(url,chrome_path,nombre)


# In[10]:


#starts scraping and crawling
liste=scrap_root_page(soup) 


# In[11]:


#write results in excel sheet
df_centers.to_excel('Security_list.xlsx')

