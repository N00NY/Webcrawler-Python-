# Webcrawler-Python-
A basic webcrawler GUI made in python

This is a project I worked quite a bit on (mostly because of the sh*tty GUI).
This webcrawler can only search for hyperlinks on a webpage by looking for 'href', 'src' and 'action'.
It might actually look for mail addresses, but this lead to some downsides such as being very slow.
The webcrawler can look for hyperlinks on more than just website simultaneously in three different modes:
  - one-site search
  - infinite search (could crash the program, because it is recursive)
  - threshold search (could also crash the program, because it is recursive)

The one-site search is pretty much self explanatory, because you only search on the starting website. 
Infinite search means that it will look for hyperlinks as long as it has a current URL which is not 'None' or until the program
crashes, pretty much an open ending.
Last but not least is the threshold search, which looks for a certain amount of hyperlinks from the user input. This could
lead to the problem either crashing the program or if it searches on multiple websites at the same time, the found hyperlinks
could exceed the given threshold, because of the threads created for each given start URL.

You can also look for a term on websites. For example the term "Hello" on "http://www.thewebsiteyoulookingFor.com".
The user input would look like this: 'http://www.thewebsiteyoulookingFor.com term:Hello'. At the moment it is only capable
to look for one term on a website.
If you only want to look for hyperlinks, the input should look something like this: 'http://www.thewebsiteyoulookingFor.com, http://thewebsiteyoulookingFor.com, thewebsiteyoulookingFor.com'. Anything else won't be accepted by the program.

The webcrawler also comes with a proxy list which is 'downloaded' from http://www.gatherproxy.com/proxylist/anonymity/?t=Elite.
This list is updated every 5 minutes, so that it keeps the extra traffic on this site low as I don't own it and I don't plan to
(D)DoS it.

Another feature is the User-Agent. I didn't make a list of User-Agents, because from my experience you can put any User-Agent in it. But with this piece of software, I mostly chose the User-Agent 'n00nY'. Feel free to use it or block it from your own website
by adding one or two lines to the robots.txt file.

The webcrawler also allows the user to abort the crawling or any other task it is performing.

Speaking of performance. The webcrawler can find around 10000 URLs in 20 to 90 seconds. But those results are depending on the
starting website(s) and your internet connection.

One last thing should be mentioned though. I do not take any responsibilities for the damage you might cause to the websites you let the webcrawler crawl, so read their terms of conditions first.
For further questions you might be having: https://www.reddit.com/user/captainreeetardo
