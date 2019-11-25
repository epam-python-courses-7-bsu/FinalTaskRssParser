# That's how it works

* Creating rss_read class object
* Using feedparser to get a page with function parse
* Then using output functions get info from the page
* Info (source link, image link, etc.) for every novelty pack in class Novelty
* Create a pack of news filled with novelty class objects
* When a pack of news is done come back to rss_reader.py
* Here we prepare to output info according to arguments from console and write down information into DB
* If there is '--to-pdf' or '--to-html' (or both arguments) argument in console we use functions 
from PDF_and_HTML_converting to:
        1. Get some images (to avoid many copies of pictures we first of all delete images 
                            folder if it exists)
        2. Add them into PDF or/and html file
        3. Add all other information 

* If there is also '--date Y%M%D' in console with '--to-pdf' or/and '--to-html' we write down into the 
pdf or/and html file(s) news for that date.  
* If there is '--date Y%M%D' in console we take news with that date from our DB. If there is also 
'--limit N' arguments, we take N news from our DB. 
* If in addition to '--to-pdf' or/and '--to-html' and '--date Y%M%D' there is '--limit N' we write down 
N news with that date to file(s) pdf or/and html
* If '--colorize' is in console args then we colorize our news in random colors. If there is no '--colorize'
we use usual color (grey-white)
## Important!
When using pdf or html converting input your path in look like this: "C:\\Test\\" or "C:\\Test"

When input arguments to parse any page first of all put link, EXAMPLE: 
python rss_reader.py https://bla-bla-bla.by --limit 1 

If you don't want to input link and want to get news stored in local storage input for EXAMPLE
 like this: python rss_reader.py --colorize --limit 15
