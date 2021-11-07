# -*- coding: utf-8 -*-
"""
Created on Sat Nov  6 22:55:13 2021

@author: seani
"""
if __name__ == '__main__':
    #read embed_data.txt
    file=open('embed_data.txt')
    api_key=file.readline().strip('\n')
    start=file.readline().strip('\n')
    final_park=file.readline().strip('\n')
    transport=file.readline().strip('\n')
    
    #get embed link
    link='https://www.google.com/maps/embed/v1/directions?'
    link+='key='+api_key
    link+='&origin='+start
    link+='&destination='+final_park
    link+='&mode='+transport
    
    #print (link)
    file=open('index.php', 'a')
    file.write('<html>\n\t<body>\n\t\t<p></p>\n\t\t<iframe id ="iframe" src="{}" width="600" height="450" style="border:0;" allowfullscreen="" loading="lazy"></iframe>>\n\t</body>\n</html>'.format(link))
    file.close()