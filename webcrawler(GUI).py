#Official script by n00nY

import threading
import tkinter, tkinter.scrolledtext
import os
import sys
import ssl
import re
import time
import urllib
import urllib.request
from threading import *
from tkinter import *
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
import time

sys.setrecursionlimit(2147483647) #eventually stops the infinite option after 2147483647 times
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_1) # hopefully prevents 403/4
main = None #tkinter main frame
begin_entry = None #first-page
search_button = None #self explaining
abort_button = None
mode1_radio = None #only crawl on one site
mode2_radio = None #crawl a certain threshold
mode2_entry = None #entry for mode2_radio
mode3_radio = None #crawl infinte sites
text_box = None #display for visited URLs
visited_urls_label = None #Number of URLs found
slide_label = None #displays proxy list, a tutorial, etc.
current_url_entry = None #current visited URL
#close = None #self explaining and not needed at the moment
proxy_entry = None #self-explaining
header_entry = None #self-explaining
sv = None #StringVar for mode1/2/3
counter = 1 #current hyperlink
thread_counter = 0 #counts Threads created when multiple URLs are given at beginning of search
l_length = 0 #total of hyperlinks
working = 0 #toal of working hyperlinks
threshold = 0 #for mode3_entry
proxy = "" #proxy option
p_working = True #checks if proxy is working
header = "" #user-agent option
search = False #if true -> [ SPIDER ] Started Crawling
abort = False #if true -> aborts crawling

f = open("links.txt", "w")
f.close()
f = open("LinksAndTerms.txt", "a")
f.close()

def crawler(start_url, search_term=None):
    global current_url_entry
    global text_box
    global visited_urls_label
    global context
    global header
    global proxy
    global l_length
    global abort
    global working

    if abort:
        return LinksToTXT(start_url, [], search_term)
    liste = []
    found = False
    start_url = start_url.strip("\n")
    current_url_entry.delete(0, len(current_url_entry.get()))
    current_url_entry.insert(0, start_url)

    try:
        if proxy != "Insert Proxy" and header != "Insert User-Agent":
            u = urllib.request.Request(start_url, headers={"User-Agent":header})
            u.set_proxy(proxy, "http")
            try:
                u = urllib.request.urlopen(u, context=context).read().decode("utf-8", 'ignore')
            except Exception as e:
                print(e)
                text_box.insert(END, "[ - ] Could not visit URL:\n" + start_url + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
                return LinksToTXT(start_url, [], search_term)
            u = u.splitlines()
        elif proxy != "Insert Proxy" and header == "Insert User-Agent":
            u = urllib.request.Request(start_url)
            u.setproxy(proxy)
            try:
                u = urllib.request.urlopen(u, context=context).read().decode("utf-8", 'ignore')
            except Exception as e:
                print(e)
                text_box.insert(END, "[ - ] Could not visit URL:\n" + start_url + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
                return LinksToTXT(start_url, [], search_term)
            u = u.splitlines()
        elif proxy == "Insert Proxy" and header != "Insert User-Agent":
            u = urllib.request.Request(start_url, headers={"User-Agent":header})
            try:
                u = urllib.request.urlopen(u, context=context).read().decode("utf-8", 'ignore')
            except Exception as e:
                print(e)
                text_box.insert(END, "[ - ] Could not visit URL:\n" + start_url + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
                return LinksToTXT(start_url, [], search_term)
            u = u.splitlines()
        else:
            try:
                u = urllib.request.urlopen(start_url, context=context).read().decode("utf-8", 'ignore')
            except Exception as e:
                print(e)
                text_box.insert(END, "[ - ] Could not visit URL:\n" + start_url + "\n", "negative")
                text_box.tag_config("negative", foreground="red")
                text_box.see(END)
                text_box.update()
                return LinksToTXT(start_url, [], search_term)
            u = u.splitlines()
    except:
        return LinksToTXT(start_url, [], search_term)

    st_found = 0
    st_counter = 0
    for i in u:
        if abort:
            return LinksToTXT(start_url, [], search_term)
        if search_term != None and search_term in i:
            if st_found == 1:
                st_counter += 1
            else:
                text_box.insert(END, "[ + ] Found " + search_term + " on " + start_url + "\n", "positive")
                text_box.tag_config("positive", foreground="green")
                st_found = 1
                st_counter += 1
        if "href" in i:
            i = i[i.find("href") + len("href"):]
            if "mailto:" not in i:
                if "'" in i:
                    first = i.find("'") + 1
                    i = i[first:]
                    last =  i.find("'")
                    i = i[:last]
                    found = True
                if '"' in i:
                    first = i.find('"') + 1
                    i = i[first:]
                    last =  i.find('"')
                    i = i[:last]
                    found = True
        elif "src" in i:
            i = i[i.find("src") + len("src"):]
            if "'" in i:
                first = i.find("'") + 1
                i = i[first:]
                last =  i.find("'")
                i = i[:last]
                found = True
            if '"' in i:
                first = i.find('"') + 1
                i = i[first:]
                last =  i.find('"')
                i = i[:last]
                found = True
        elif "action" in i:
            i = i[i.find("action") + len("action"):]
            if "'" in i:
                first = i.find("'") + 1
                i = i[first:]
                last =  i.find("'")
                i = i[:last]
                found = True
            if '"' in i:
                first = i.find('"') + 1
                i = i[first:]
                last =  i.find('"')
                i = i[:last]
                found = True
        '''else:
            tmp = extract_email(i, start_url)
            if tmp != []:
                f = open("E-Mail.txt", "a")
                for i in tmp:
                    f.write(i + " found on " + start_url + "\n")
                f.close()'''
        if found:
            if i.startswith("/"):
                i = start_url.strip("\n") + i
                liste.append(i)
            elif i.startswith("http"):
                liste.append(i)
            else:
                if not i.startswith("/"):
                    i = start_url.strip("\n") + "/" + i
                else:
                    i = start_url.strip("\n") + i
                liste.append(i)
            tmp = visited_urls_label.cget("text")
            tmp = tmp.split(":")[1].strip(" ")
            visited_urls_label["text"] = "Found URLs: " + str(int(tmp) + 1)
            visited_urls_label.update()
            if sv.get() == "Threshold":
                l_length = int(tmp) + 1
                if l_length == threshold:
                    liste = LinkCharChecker(liste)
                    working += len(liste)
                    text_box.insert(END, "[ * ] Theoratically working URLs: " + str(working) + "\n")
                    text_box.see(END)
                    text_box.update()
                    return LinksToTXT(start_url, liste, search_term)
        found = False

    if st_counter != 0:
        f = open("LinksAndTerms.txt", "a")
        f.write(start_url + " --> " + search_term + " " + str(st_counter) + " times")
        f.close()
    text_box.insert(END, "[ * ] Visited URL: " + start_url + "\n")
    text_box.see(END)
    text_box.update()
    liste = LinkCharChecker(liste)
    working += len(liste)
    text_box.insert(END, "[ * ] Theoratically working URLs: " + str(working) + "\n")
    text_box.see(END)
    text_box.update()
    return LinksToTXT(start_url, liste, search_term)

def LinksToTXT(url, liste, search_term=None):
    global counter
    global sv
    global text_box
    global l_length
    global threshold
    global abort
    global search
    global thread_counter
    global working
    
    zaehler = 0
    next_url = ""

    if abort:
        search = False
        l_length = 0
        counter = 1
        working = 0
        if thread_counter > 0:
            thread_counter -= 1
        if thread_counter == 0:
            abort = False
            text_box.insert(END, "[ SPIDER ] Aborted crawling\n", "spider")
            text_box.tag_config("spider", foreground="blue")
            text_box.see(END)
            text_box.update()
            search_button["state"] = "normal"
            mode1_radio["state"] = "normal"
            mode3_radio["state"] = "normal"
            mode2_entry["state"] = "normal"
            proxy_entry["state"] = "normal"
            header_entry["state"] = "normal"
            mode2_radio["state"] = "normal"
        return
        
    if liste == []:
        counter += 1
        f = open("links.txt", "rb")
        while zaehler != counter:
            try:
                next_url = f.readline().decode("utf-8").strip("\n")
            except:
                if zaehler < counter:
                    continue
                else:
                    counter += 1
                
            zaehler += 1
        f.close()
        if sv.get() != "one-site" and next_url != "":
            return crawler(next_url, search_term)
        elif sv.get() != "one-site" and next_url == "":
            text_box.insert(END, "[ ! ] No more URLs to visit...\n", "important")
            text_box.tag_config("important", foreground="red")
            text_box.see(END)
            text_box.update()
            if thread_counter == 0:
                working = 0
                search_button["state"] = "normal"
                mode1_radio["state"] = "normal"
                mode3_radio["state"] = "normal"
                mode2_entry["state"] = "normal"
                proxy_entry["state"] = "normal"
                header_entry["state"] = "normal"
                mode2_radio["state"] = "normal"
            if thread_counter > 0:
                thread_counter -= 1
                print(thread_counter)
            return
    
    if sv.get() == "one-site":
        f = open("links.txt", "w")
        for i in range(len(liste)):
            f.write(liste[i] + "\n")
        f.close()
        if thread_counter > 0:
            thread_counter -= 1
            if thread_counter != 0:
                return
            print(thread_counter)
        if thread_counter == 0:
            testLink()
            text_box.insert(END,"[ + ] Finished crawling at {0} hyperlinks --> Links in 'links.txt'\n".format(len(liste)), "positive")
            text_box.tag_config("positive", foreground="green")
            working = 0
            search_button["state"] = "normal"
            mode1_radio["state"] = "normal"
            mode2_radio["stat"] = "normal"
            mode3_radio["state"] = "normal"
            mode2_entry["state"] = "normal"
            proxy_entry["state"] = "normal"
            header_entry["state"] = "normal"
        return slide()

    elif sv.get() == "infinite":
        #print("[ + ] {0} hyperlinks found on {1}".format(len(liste), url))
        f = open("links.txt", "a")
        for i in liste:
            f.write(i + "\n")
        f.close()
        counter += 1
        f = open("links.txt", "rb")
        while zaehler != counter:
            try:
                next_url = f.readline().decode("utf-8").strip("\n")
            except:
                f.readline()
                next_url = f.readline().decode("utf-8").strip("\n")
            zaehler += 1
        f.close()
        text_box.insert(END, "[ * ] Next URL: " + next_url + "\n")
        text_box.see(END)
        text_box.update()
        if next_url == "":
            text_box.insert(END, "[ ! ] No more hyperlinks to select from\n", "important")
            text_box.tag_config("important", foreground="red")
            text_box.see(END)
            text_box.update()
            if thread_counter > 0:
                thread_counter -= 1
                if thread_counter != 0:
                    return
                print(thread_counter)
            if thread_counter == 0:
                testLink()
                l_length = 0
                counter = 1
                working  = 0
                search_button["state"] = "normal"
                mode1_radio["state"] = "normal"
                mode2_radio["stat"] = "normal"
                mode3_radio["state"] = "normal"
                mode2_entry["state"] = "normal"
                proxy_entry["state"] = "normal"
                header_entry["state"] = "normal"
            return slide()

    elif sv.get() == "Threshold":
        text_box.insert(END, "[ + ] {0} hyperlinks found on {1}\n".format(len(liste), url), "positive")
        text_box.tag_config("positive", foreground="green")
        text_box.see(END)
        text_box.update()
        f = open("links.txt", "a")
        for i in liste:
            f.write(i + "\n")
        f.close()
        counter += 1
        if l_length >= threshold:
            text_box.insert(END, "[ + ] Finished crawling --> Links in 'links.txt'\n", "positive")
            text_box.tag_config("positive", foreground="green")
            text_box.see(END)
            text_box.update()
            if thread_counter > 0:
                thread_counter -= 1
                if thread_counter != 0:
                    return
            if thread_counter == 0:
                testLink()
                l_length = 0
                counter = 1
                working = 0
                search_button["state"] = "normal"
                mode1_radio["state"] = "normal"
                mode2_radio["stat"] = "normal"
                mode3_radio["state"] = "normal"
                mode2_entry["state"] = "normal"
                proxy_entry["state"] = "normal"
                header_entry["state"] = "normal"
            return slide()
        f = open("links.txt", "rb")
        while zaehler != counter:
            try:
                zaehler += 1
                next_url = f.readline().decode("utf-8").strip("\n")
            except:
                counter += 1
        f.close()
    return crawler(next_url, search_term)

def on_closing():
    global main

    main.destroy()
    os.kill(os.getpid(), 1)

def LinkCharChecker(liste):
    char_map = []
    for i in range(48, 58):
        char_map.append(chr(i))
    for i in range(97, 123):
        char_map.append(chr(i))
    for i in range(65, 91):
        char_map.append(chr(i))
    char_map.append("?")
    char_map.append("&")
    char_map.append(":")
    char_map.append("$")
    char_map.append("-")
    char_map.append("_")
    char_map.append(".")
    char_map.append("+")
    char_map.append("!")
    char_map.append("*")
    char_map.append("'")
    char_map.append("(")
    char_map.append(")")
    char_map.append(",")
    char_map.append("/")
    char_map.append("=")
    char_map.append("#")
    char_map.append(";")
    i = 0
    while i < len(liste):
        if abort:
            return LinksToTXT(None, None)
        url = liste[i]
        if not url.startswith("http"):
            url = url[url.find("http"):]
        first = url.find(":")
        url = url.replace("\\", "/")
        url = url.replace(" ", "")
        if first == 4 or first == 5:
            for char in range(len(url)):
                if url[char] not in char_map:
                    if not char - 1 == len(url):
                        liste.remove(liste[i])
                    else:
                        liste[i] = url[:len(url)-1]
                    break
        else:
            liste.remove(liste[i])
        i += 1
    return liste

def testLink():
    global text_box
    global context
    global abort
    
    text_box.insert(END, "[ * ] Testing URLs...\n")
    text_box.see(END)
    text_box.update()
    f = open("links.txt", "rb")
    f2 = open("links_tmp.txt", "wb")
    f2.close()
    found = False
    theo = 0
    pract = 0
    while True:
        if abort:
            return LinksToTXT(None, None)
        tmp = f.readline().decode("utf-8")
        if tmp == "":
            break
        theo += 1
        u = urllib.request.Request(tmp, headers={"User-Agent":"Mozilla/5.0"})
        try:
            u = urllib.request.urlopen(u, context=context)
            found = True
        except:
            continue
        if found:
            f2 = open("links_tmp.txt", "rb")
            found = False
            while True:
                j = f2.readline()
                if j == b"" or j == b"\n":
                    break
                if j == tmp.encode():
                    found = True
                    break
            if found:
                found = False
                continue
            else:
                pract += 1
                f2.close()
                f2 = open("links_tmp.txt", "ab")
                f2.write(tmp.encode())
                f2.close()
                s3 = Thread(target=slide3, args=(theo, pract, 1))
                s3.start()
    f = open("links.txt", "wb")
    f2 = open("links_tmp.txt", "rb")
    text_box.insert(END, "[ * ] Writing...\n")
    text_box.see(END)
    text_box.update()
    while True:
        tmp = f2.readline()
        if tmp == b"":
            break
        f.write(tmp)
    f2.close()
    f.close()
    os.remove("links_tmp.txt")
    print(theo, pract)
    text_box.insert(END, "[ + ] Test succeded\n", "positive")
    text_box.tag_config("positive", foreground="green")
    text_box.see(END)
    text_box.update()
    
def testProxy():
    global proxy
    global context
    global text_box
    global p_working
    global search_button
    global mode1_radio
    global mode3_radio
    global mode2_radio
    global mode2_entry
    global header
    global begin_entry
    global thread_counter
    
    u = urllib.request.Request("http://google.de", headers={"User-Agent":"n00nY"})
    u.set_proxy(proxy, "http")
    try:
        proxy_entry["state"] = "disabled"
        u = urllib.request.urlopen(u, context=context).read().decode("utf-8", "ignore")
    except:
        text_box.insert(END, "[ - ] The proxy: " + proxy + " won't get you anywhere\n", "negative")
        text_box.tag_config("negative", foreground="red")
        text_box.see(END)
        text_box.update()
        proxy_entry["state"] = "normal"
        return
    text_box.insert(END, "[ + ] Proxy works\n", "positive")
    text_box.tag_config("positive", foreground="green")
    text_box.insert(END, "[ SPIDER ] Started Crawling\n", "spider")
    text_box.tag_config("spider", foreground="blue")
    text_box.see(END)
    text_box.update()
    search_button["state"] = "disabled"
    mode1_radio["state"] = "disabled"
    mode3_radio["state"] = "disabled"
    mode2_entry["state"] = "disabled"
    header_entry["state"] = "disabled"
    mode2_radio["state"] = "disabled"
    f = open("links.txt", "w")
    start_url = begin_entry.get()
    if "," in start_url:
        start_url = start_url.split(",")
        for i in range(len(start_url)):
            if not start_url[i].startswith("http"):
                if " " in start_url[i]:
                    start_url[i] = start_url[i].strip(" ")
                start_url[i] = "http://" + start_url[i]
            f.write(start_url[i] + "\n")
        f.close()
    else:
        if not start_url.startswith("http"):
            start_url = "http://" + start_url
        f.write(start_url + "\n")
        f.close()
    if not isinstance(start_url, list):
        t2 = threading.Thread(target=crawler, args=(start_url,))
        t2.start()
    else:
        for i in range(len(start_url)):
            threading.Thread(target=crawler, args=(start_url[i],)).start()
            thread_counter += 1
        print(thread_counter)
    
def slide(mode=None):
    while True:
        if mode == None:
            slide1()
            time.sleep(300)
            #slide2() tutorial image
            #time.sleep(15)
            slide3(None, None, None) #displays how many links actually work/are practical
            time.sleep(15)
        elif mode == s1:
            slide1()
            time.sleep(300)
        elif mode == s2:
            slide2()
            time.sleep(15)
        elif mode == s3:
            slide3(None, None, None)
            
def slide1():
    global slide_label

    u = urllib.request.urlopen("http://www.gatherproxy.com/proxylist/anonymity/?t=Elite").read().decode("utf-8")
    u = u.splitlines()
    proxy = "gp.insertPrx({"
    text = "{0:<40}{1:<20}{2:>10}\n".format("Country", "IP", "Port")
    ip = ""
    port = ""
    country = ""
    c = 0
    for i in u:
        if c == 20:
            break
        if proxy in i:
            i = i[i.find(proxy) + len(proxy):]
            i = i[:i.find("}")]
            l = i.splitlines()
            for j in l:
                tmp = j.split(",")
                for k in tmp:
                    if "PROXY_COUNTRY" in k:
                        country = k.split(":")[1].strip('"')
                    if "PROXY_IP" in k:
                        ip = k.split(":")[1].strip('"')
                    if "PROXY_PORT" in k:
                        port = k.split(":")[1].strip('"')
                        port = int(port, 16)
               
            text += "{0:<40}{1:<20}{2:>10}\n".format(country, ip, port)
            time.sleep(0.1)
            c += 1
        slide_label["text"] = text
        slide_label.update()
    slide_label["text"] = slide_label.cget("text") + ("{0:<40}".format("Source: http://www.gatherproxy.com/proxylist\n/anonymity/?t=Elite"))
    slide_label.update()

def slide2():
    return

def slide3(theo, pract, mode):
    global slide_label

    if theo == None or pract == None or mode == None:
        return slide()
    if mode == 1:
        slide_label["text"] = ""
        slide_label.update()
        slide_label["text"] = "Theoratical working URLs: " + str(theo) + "\n"
        slide_label.update()
        slide_label["text"] = slide_label.cget("text") + "Practical working URLs: " + str(pract)
        return
    elif mode == 2: #Probably tips or some other shit
        return
    elif mode == None:
        return
    
def entry_handler(e, func=None):
    global begin_entry
    global mode2_entry
    global proxy_entry
    global header_entry

    print(e)
    if e == "be" and begin_entry.get() == "Begin Search":
        begin_entry.delete(0, len(begin_entry.get()))
    if e == "he" and header_entry.get() == "Insert User-Agent":
        header_entry.delete(0, len(header_entry.get()))
    if e == "pe" and proxy_entry.get() == "Insert Proxy":
        proxy_entry.delete(0, len(proxy_entry.get()))
    if e == "m2" and mode2_entry.get() == "Threshold":
        mode2_entry.delete(0, len(mode2_entry.get()))
    if e == "foutbe" and begin_entry.get() == "":
        begin_entry.insert(0, "Begin Search")
    if e == "fouthe" and header_entry.get() == "":
        header_entry.insert(0, "Insert User-Agent")
    if e == "foutpe" and proxy_entry.get() == "":
        proxy_entry.insert(0, "Insert Proxy")
    if e == "foutm2" and mode2_entry.get() == "":
        mode2_entry.insert(0, "Threshold")
    if e == "begin":
        begin_entry.bind("<Key>", lambda  be: entry_handler("be"))
        begin_entry.bind("<FocusOut>", lambda be: entry_handler("foutbe"))
    if e == "header":
        header_entry.bind("<Key>", lambda he: entry_handler("he"))
        header_entry.bind("<FocusOut>", lambda he: entry_handler("fouthe"))
    if e == "proxy":
        proxy_entry.bind("<Key>", lambda pe: entry_handler("pe"))
        proxy_entry.bind("<FocusOut>", lambda pe: entry_handler("foutpe"))
    if e == "mode2":
        mode2_entry.bind("<Key>", lambda m2: entry_handler("m2"))
        mode2_entry.bind("<FocusOut>", lambda m2: entry_handler("foutm2"))
        
def action_handler(command, var=None):
    global search_button
    global mode1_radio
    global mode2_radio
    global mode3_radio
    global begin_entry
    global mode2_entry
    global sv
    global abort
    global text_box
    global header_entry
    global proxy_entry
    global proxy
    global threshold
    global header
    global search
    global visited_urls_label
    global thread_counter
    global p_working
    
    proceed = False
    proceed2 = False
    print("StringVar: " + sv.get())
    print(command, type(command))
    if command == "search":
        search_button.update()
        print(sv.get(), mode2_entry.get())
        if sv.get() != "UNDEF":
            proceed = True #Mode selected (one-site, infinite, Threshold)
            if sv.get() == "Threshold" and mode2_entry.get() == "Threshold" or mode2_entry.get() == "0":
                proceed = False
                
        if begin_entry.get() != "Begin Search" and begin_entry.get() != "":
            proceed2 = True #Entered a URL
        print(proceed, proceed2)
        if not proceed or not proceed2:
            text_box.insert(END, "[ ! ] Please enter a URL and select a mode\n", "important")
            text_box.tag_config("important", foreground="red")
            text_box.see(END)
            text_box.update()
            text_box.insert(END, "[ * ] If you've selected the threshold-checker do not forget to put a threshold in the entry.\n")
            text_box.see(END)
            text_box.update()
            search_button.update()
        else:
            search = True
            abort = False
            if sv.get() == "Threshold":
                try:
                    threshold = int(mode2_entry.get())
                except:
                    text_box.insert(END, "[ Threshold ] Only accepts numbers\n", "threshold")
                    text_box.tag_config("threshold", foreground="orange")
                    return
            
            visited_urls_label["text"] = "Found URLs: 0"
            current_url_entry.update()
            header = header_entry.get()
            proxy = proxy_entry.get()
            p_working = True
            if proxy != "Insert Proxy":
                pw = Thread(target=testProxy)
                pw.start()
                return
            text_box.insert(END, "[ SPIDER ] Started Crawling\n", "spider")
            time.sleep(0.5)
            text_box.tag_config("spider", foreground="blue")
            text_box.see(END)
            text_box.update()
            search_button["state"] = "disabled"
            mode1_radio["state"] = "disabled"
            mode3_radio["state"] = "disabled"
            mode2_entry["state"] = "disabled"
            proxy_entry["state"] = "disabled"
            header_entry["state"] = "disabled"
            mode2_radio["state"] = "disabled"
            f = open("links.txt", "w")
            start_url = begin_entry.get()
            search_term = None
            if "term:" in start_url:
               search_term = start_url[start_url.find("term:") + len("term:"):]
               start_url = start_url[:start_url.find("term:")]
            if "," in start_url:
                start_url = start_url.split(",")
                for i in range(len(start_url)):
                    if not start_url[i].startswith("http"):
                        if " " in start_url[i]:
                            start_url[i] = start_url[i].strip(" ")
                        start_url[i] = "http://" + start_url[i]
                    f.write(start_url[i] + "\n")
                f.close()
            else:
                if not start_url.startswith("http"):
                    start_url = "http://" + start_url
                f.write(start_url + "\n")
                f.close()
            if not isinstance(start_url, list):
                start_url = start_url.strip(" ")
                t2 = threading.Thread(target=crawler, args=(start_url, search_term))
                t2.start()
            else:
                for i in range(len(start_url)):
                    threading.Thread(target=crawler, args=(start_url[i], search_term)).start()
                    thread_counter += 1
                print(thread_counter)
                
    if str(command) == "<FocusIn event>" and var == "be":
        t1 = threading.Thread(target=entry_handler, args=("begin",))
        t1.start()
    if str(command) == "<FocusIn event>" and var == "he":
        t2 = threading.Thread(target=entry_handler, args=("header",))
        t2.start()
    if str(command) == "<FocusIn event>" and var == "pe":
        t3 = threading.Thread(target=entry_handler, args=("proxy",))
        t3.start()
    if str(command) == "<FocusIn event>" and var == "m2":
        t3 = threading.Thread(target=entry_handler, args=("mode2",))
        t3.start()

    if command == "abort":
        if search:
            abort = True
        
def gui_thread():
    global main
    global begin_entry
    global search_button
    global abort_button
    global mode1_radio
    global mode2_radio
    global mode2_entry
    global mode3_radio
    global text_box
    global visited_urls_label
    global current_url_entry
    global close
    global sv
    global header_entry
    global proxy_entry
    global slide_label

    # tkinter.TK
    main = tkinter.Tk()
    main.title("Webcrawler")
    main.wm_iconbitmap("")
    main.geometry("750x500")
    main.resizable(False, False)
    main.protocol("WM_DELETE_WINDOW", on_closing)
        
    # Var
    sv = tkinter.StringVar()
    sv.set("UNDEF")
    
    #Buttons
    search_button = tkinter.Button(main, text="search", command=lambda:action_handler("search"))
    search_button.place(x=375,y=0)
    abort_button = tkinter.Button(main, text="abort", command=lambda:action_handler("abort"))
    abort_button.place(x=120, y=80)
    #close = tkinter.Button(main,width=9, height=5, justify=CENTER, text="close", command=lambda:action_handler("close"))
    #close.place(x=670, y=430)
    
    #Radios
    mode1_radio = tkinter.Radiobutton(main, text="one-site", variable=sv, value="one-site")
    mode1_radio.place(x=0, y=33)
    mode2_radio = tkinter.Radiobutton(main, text="", variable=sv, value="Threshold")
    mode2_radio.place(x=200, y=33)
    mode3_radio = tkinter.Radiobutton(main, text="infinite", variable=sv, value="infinite")
    mode3_radio.place(x=100, y=33)
    
    #Entries
    begin_entry = tkinter.Entry(main, width=53)
    begin_entry.bind("<FocusIn>", action_handler("<FocusIn event>", "be"))
    begin_entry.insert(0, "Begin Search")
    begin_entry.place(x=0, y = 0)
    mode2_entry = tkinter.Entry(main)
    mode2_entry.bind("<FocusIn>", action_handler("<FocusIn event>", "m2"))
    mode2_entry.insert(0, "Threshold")
    mode2_entry.place(x=216, y=33)
    current_url_entry = tkinter.Entry(main, width=36)
    current_url_entry.insert(0, "")
    current_url_entry.place(x=200, y=90)
    header_entry = tkinter.Entry(main,width=36)
    header_entry.bind("<FocusIn>", action_handler("<FocusIn event>", "he"))
    header_entry.insert(0, "Insert User-Agent")
    header_entry.place(x=500, y=0)
    proxy_entry = tkinter.Entry(main, width=36)
    proxy_entry.bind("<FocusIn>", action_handler("<FocusIn event>", "pe"))
    proxy_entry.insert(0, "Insert Proxy")
    proxy_entry.place(x=500, y=33)

    #Labels
    visited_urls_label = tkinter.Label(main, text="Found URLs: 0")
    visited_urls_label.place(x=0, y=90)
    slide_label = tkinter.Label(main, width=50)
    slide_label.place(x=400, y=111)
    
    #Textboxes
    text_box = tkinter.scrolledtext.ScrolledText(main, width=50) 
    text_box.place(x=0, y=111)

    #Intro
    
    main.mainloop()
    
    
t_main = Thread(target=gui_thread)
t_main.start()
time.sleep(0.5)
t_slide = Thread(target=slide)
t_slide.start()
