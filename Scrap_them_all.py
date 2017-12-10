
# coding: utf-8

# In[13]:


from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from time import sleep
import pandas as pd 


# In[14]:


def load_root_page (url,chrome_path,nombre):
	#Opens a Web Page in Chrome
	chrome_options = webdriver.ChromeOptions()
	# This is to stop the Chrome window from opening up ( --headless )
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(chrome_path, chrome_options=chrome_options)
	driver.get(url)
	for i in range(nombre):
		moreButton = driver.find_element_by_css_selector("#psirtMore > a")
		moreButton.click()
		sleep(0.3) #even 0.25 is not enough to get results back before the next click
	soup = BeautifulSoup(driver.page_source, "html.parser")
	return soup


# In[15]:


def scrap_root_page(soup):
    for record in soup.findAll('tr'):
        i=0
        for data in record.findAll('td'):
            site = data.find('a', href=True)
            if (i==0):
                center[i] = base + site['href']
                i+=1
            else:
                center[i] = data.text.strip() 
                center[i] = center [i]
                i+=1
        if center[0] is not None:
            scrap_article(center[0],center)
            if not(all(v is None for v in center)):
                df_centers.loc[len(df_centers.index)] = center


# In[16]:


def scrap_article(url,center):
    thepage = urllib.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    all_details = soup.findAll('div',attrs={'class':'psirt-set-out'})
    i=3
    for detail in all_details:
        contenu =  detail.find('div',attrs={'class':'moreinfo'})
        tableau = contenu.findAll('tr')
        if tableau:
            center[i]=scrap_tableau_details(tableau)
            i+=1
            continue
        center[i] = contenu.text.strip()
        i+=1


# In[17]:


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


# In[18]:


df_centers = pd.DataFrame(columns=['Url', 'Title', 'Version','Summary','Software Versions and Fixes','Affected Versions','Resolved product and Version','Impact','Vulnerability Scoring Details','Technique Details','Temporary Fix','Obtaining Fixed Software','Source','Revision History','FAQs','Huawei Security Procedures','Declaration'])
center = [None] * 17


# In[19]:


url="http://www.huawei.com/en/psirt/security-advisories"
chrome_path="/Users/abderrahmane/Desktop/Divers/scrap/chromedriver"
base="http://www.huawei.com"


# In[20]:


soup=load_root_page(url,chrome_path,2)


# In[21]:


liste=scrap_root_page(soup)


# In[22]:


df_centers.to_excel('Security_list.xlsx')

