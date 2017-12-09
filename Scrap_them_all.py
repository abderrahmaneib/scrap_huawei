
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup
import urllib
from time import sleep
import pandas as pd 


# In[2]:


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


# In[3]:


def scrap_root_page(soup):
    for record in soup.findAll('tr'):
        i=0
        for data in record.findAll('td'):
            site = data.find('a', href=True)
            if (i==0):
                #print (base + site['href'])
                center[i] = base + site['href']
                i+=1
            else:
                center[i] = data.text.lstrip() 
                i+=1
        print (center[0])
        if center[0] is not None:
            scrap_article(center[0],center)
            if not(all(v is None for v in center)):
                df_centers.loc[len(df_centers.index)] = center


# In[4]:


def scrap_article(url,center):
    thepage = urllib.urlopen(url)
    soup = BeautifulSoup(thepage, "html.parser")
    all_details = soup.findAll('div',attrs={'class':'psirt-set-out'})
    i=3
    for detail in all_details:
        print i
        #print detail.find('div', attrs={'class':'expand-moreb'}).text.strip()
        contenu =  detail.find('div',attrs={'class':'moreinfo'})
        tableau = contenu.findAll('tr')
        if tableau:
            center[i]="fe"
            i+=1
            continue
        '''
            table="("
            for ligne in tableau:
                data=""
                champs = ligne.findAll('td')
                for champ in champs:
                    data = data + "," + champ.text.strip()
                table = table + ";" + data[1:]
            table = table + ")"
            all_content = all_content + "," + table
            ''' 
        center[i] = contenu.text.strip()
        i+=1


# In[5]:


df_centers = pd.DataFrame(columns=['Url', 'Title', 'Version','Summary','Software Versions and Fixes','Impact','Vulnerability Scoring Details','Technique Details','Temporary Fix','Obtaining Fixed Software','Source','Revision History','FAQs','Huawei Security Procedures','Declaration'])
center = [None] * 15


# In[6]:


url="http://www.huawei.com/en/psirt/security-advisories"
chrome_path="/Users/abderrahmane/Desktop/Divers/scrap/chromedriver"
base="http://www.huawei.com"


# In[9]:


soup=load_root_page(url,chrome_path,2)


# In[10]:


liste=scrap_root_page(soup)


# In[11]:


df_centers


# In[12]:


df_centers.to_excel('hello2.xlsx')

