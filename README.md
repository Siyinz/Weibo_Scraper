# Sina Weibo Scraper

The Cultural Revolution is the dividing line in modern Chinese history and separates its century of revolutions, when China was known for mass mobilization to generate social change, and the Reform Era, which is deeply depoliticized and economically driven. This scraper project is for Prof. Xu's (UM Sociology) work on Cultural Revolution's fluence on shaping contemporary China and its relationship to global capitalism.

This project uses Weibo's advanced search to implement keyword-based content crawling and scraping.

### Crawl Html page
This part uses Sina Weibo's advanced search function to search for culture revolution related keywords' URLs. 

### Scrape key content from html page
By using BeautifulSoup, in this part, I scraped Weibo users' personal information, like location, gender, education, ect. Since the results are all in Chinese, I used unicode_escape transcoding to ensure that the Chinese display is normal with a text editor.

Sample result: Keywork "Green Guard" trend in Weibo Search
![green guard trend](https://github.com/Siyinz/Weibo_Scraper/blob/main/greenGuardByMonth.png)
