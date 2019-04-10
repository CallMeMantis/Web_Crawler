import urllib2
import HTMLParser

class Page(object):
    
    def __init__(self, url):
        self.url = url
    
    def open_page(self):
        try:
            print("Trying to load site", self.url)
            return urllib2.urlopen(self.url)
        except Exception:
            print("\t Connection error", self.url)
            return None

    
    def read_page(self):
        page = self.open_page()
        if page:
            page_content = page.read()
            return page_content
        return None
        
    def find_a(self):
        page_content = self.read_page()
        
        if page_content is None:
            return []
        
        links=[]
        a=0
        b=0
        while a != -1:
            a = page_content.find('<a',b)
            b = page_content.find('</a>',a)
            z = page_content[a:b]
            links.append(z)
        return links
            
    def get_links(self):
        links = self.find_a()
        table=[]
        for link in links:
            c = link.find('href="')
            d = link.find('"',c + 6)
            e = link.find('>')
            #print link[c+6:d], '---', link[e+1:]
            k = link[c+6:d]
            table.append(k)
        return table
    
    def get_unique_links(self):
        table = self.get_links()
        for element in table:
            quantity = table.count(element)
            while quantity != 1:
                table.remove(element)
                quantity = table.count(element)
        return table
    
    def get_proper_links(self):
        table = self.get_unique_links()
        for element in table[1:]:
            #print element
            if element.startswith('#') or element == '/' or element == 'me=':
                table.remove(element)
            if element.startswith('/'):
                temporary_element = element
                element = 'http://www.if.uz.zgora.pl' + temporary_element
        return table   




class Crawler(object):
    
    def __init__(self, url):
        self.url = url

    def crawl(self): 
        visited_links = [self.url]
        for link_lev_1 in Page(self.url).get_proper_links():
            if not link_lev_1 in visited_links:
                visited_links.append(link_lev_1)
                for link_lev_2 in Page(link_lev_1).get_proper_links():
                    if not link_lev_2 in visited_links:
                        visited_links.append(link_lev_2)
                        for link_lev_3 in Page(link_lev_2).get_proper_links():
                            if not link_lev_3 in visited_links:
                                visited_links.append(link_lev_3)
        print(">>>>>>>", len(visited_links))
        return visited_links
        
    def creating_file(self):
        plik = open('links.txt','w')
        calc = 0
        for element in self.crawl():
            plik.write(element)
            calc = calc + 1
        plik.close()    
        return plik, calc

    #def calculator(self):
        #plik = open('links.txt','r')
        #calc = 0
        #for line in plik.readline():
            #calc +=1
        #plik.close()
        #return plik
    

#table = Page('http://www.if.uz.zgora.pl').get_proper_links()
print(Crawler('http://www.if.uz.zgora.pl').creating_file())
