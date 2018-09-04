
# coding: utf-8

# In[4]:


import dryscrape
import time


# In[5]:


for letter in 'abcdefghijklmnopqrstuvwxyz':

    sess = dryscrape.Session()

    url = 'https://www.wikiart.org/en/alphabet/' + letter

    sess.visit(url)

    time.sleep(2)

    for i in range(200):
        try:
            loadmore_button = sess.xpath("//*[@class = 'loadmore-icon']")[0]
            loadmore_button.click()
            time.sleep(2)
        except:
            pass

    img_src = sess.xpath("//div[@class = 'artist-name']/a[@class = 'ng-binding']")

    links = ['https://www.wikiart.org' +              img_src[i].get_attr('href')              for i in range(len(img_src))]
    
    fp = open('links_artists.txt','a')
    for link in links:
        fp.write(u'{}\n'.format(link))
    fp.close()

    sess.reset()


# In[6]:


links = open('links_artists.txt','r').read().split('\n')
links = list(set(links))

for link in links:

    try:
        sess = dryscrape.Session()

        sess.visit(link + '/all-works/text-list')

        img_src = sess.xpath("//li[@class = 'painting-list-text-row']/a")
    
        links_artw = ['https://www.wikiart.org' +              img_src[i].get_attr('href')              for i in range(len(img_src))]
    
        fp = open('links_artworks.txt','a')
        for link_art in links_artw:
            fp.write(u'{}\n'.format(link_art))
        fp.close()

        sess.reset()    
    
    except:
        pass


# In[7]:


def imagedownload(img_page):
    
    import dryscrape
    import shutil
    import requests

    sess = dryscrape.Session()
    sess.visit(img_page)
    
    a = sess.xpath('//*[@class = "ms-zoom-cursor"]')[0]    
   
    img_src = a['src']
    img_title = a['title']

    response = requests.get(img_src, stream=True)
    img_file = u'{}.jpg'.format(img_title)
    with open(img_file, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
    del response
        
    # Artwork Metadata
    aux = sess.xpath('//article')[0]
    info = aux.text().split('\n')

    artw_info = {}
    artw_info['artwork name'] = info[0]
    artw_info['author'] = info[1]
    artw_info['image_file'] = img_file
    artw_info['url'] = img_page
    
    try:
        artw_info['date'] = filter(lambda x: 'Date' in x, info)[0].split(': ')[1]
    except:
        artw_info['date'] = None
    try:
        artw_info['style'] = filter(lambda x: 'Style' in x, info)[0].split(': ')[1]
    except:
        artw_info['style'] = None
    try:
        artw_info['genre'] = filter(lambda x: 'Genre' in x, info)[0].split(': ')[1]
    except:
        artw_info['genre'] = None
    try:
        artw_info['media'] = filter(lambda x: 'Media' in x, info)[0].split(': ')[1]
    except:
        artw_info['media'] = None
    try:
        artw_info['dimensions'] = filter(lambda x: 'Dimensions:' in x, info)[0].split(': ')[1]
    except:
        artw_info['dimensions'] = None

    sess.reset()
    
    return artw_info


# In[10]:


links = open('links_artworks.txt','r').read().split('\n')
links = list(set(links))


# In[50]:


import json
for link in links:
    try:
        data = imagedownload(link)
        fname = data['image_file'].replace('.jpg', '.dat')
        fp = file(fname, 'w')
        fp.write(json.dumps(data, ensure_ascii = True))
        fp.close()
    except:
        pass

