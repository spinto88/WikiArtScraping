import dryscrape
import time

dryscrape.start_xvfb()

for letter in 'abcdefghijklmnopqrstuvwxyz':

    try:
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

    	links = ['https://www.wikiart.org' + img_src[i].get_attr('href') for i in range(len(img_src))]
    
	fp = open('links_artists.txt','a')
	for link in links:
        	fp.write(u'{}\n'.format(link))
	fp.close()

	sess.reset()

    except:
	pass

