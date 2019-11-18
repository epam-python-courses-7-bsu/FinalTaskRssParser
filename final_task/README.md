# RSS-READER

## What is rss-reader?

This is small application for watching feed on your device. It shows shot information about the latest news and keeps previous news.

## How to install?

1. To install the application on your device must be python 3.7 and more.
2. Download this repository on your device.
3. Open command line(Terminal) in this directory.
4. Enter next command:
```
python setup.py sdist
cd dist
pip install feedparser
pip install requests
pip install fpdf
pip install colored
pip install rss-reader-5.1.tar.gz
```
5. Check workability with command: 
```
rss-reader -h
```

## Parameters:
```
rss-reader -h
usage: rss-reader [-h] [--version] [--json] [--verbose] [--limit LIMIT] [--date DATE] [--to-html TO_HTML] [--to-pdf TO_PDF] [source]

positional arguments:
  source             RSS URL

optional arguments:
  -h, --help         show this help message and exit
  --version          Print version info
  --json             Print result as JSON in stdout
  --verbose          Outputs verbose status messages
  --limit LIMIT      Limit news topics if this parameter provided
  --date DATE        Obtaining the cached news without the Internet
  --to-html TO_HTML  The argument gets the path where the HTML news will be saved
  --to-pdf TO_PDF    The argument gets the path where the PDF news will be saved
  --colorize         Colorize text
```

##JSON format

```
{
    "title": "News by Mon, 18 Nov 2019 ",
    "items": [
        {
            "title": "The Problem with Hypersonic Missiles: \"None of this stuff works yet.\"",
            "published": "Mon, 18 Nov 2019 02:26:00 -0500",
            "link": "https://news.yahoo.com/problem-hypersonic-missiles-none-stuff-072600256.html",
            "summary": "[image: The Problem with Hypersonic Missiles: \"None of this stuff works yet.\"]Don’t get too excited about hypersonic weapons, one prominent U.S. defense journalist advised. According to him, we still don’t know for sure whether the Mach-5-plus munitions actually work.",
            "contain_image": true,
            "link_on_image": "http://l2.yimg.com/uu/api/res/1.2/YOhob5Hzzh5bR_GUbztqLg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en/the_national_interest_705/ef38aa18f65ca8d1c745a2f38867a67c"
        },
        {
            "title": "Ukraine ex-president named witness in power abuse probe",
            "published": "Mon, 18 Nov 2019 12:33:39 -0500",
            "link": "https://news.yahoo.com/ukraine-ex-president-named-witness-power-abuse-probe-173339651.html",
            "summary": "[image: Ukraine ex-president named witness in power abuse probe]Ukraine's former president Petro Poroshenko has been designated a witness in a criminal investigation related to the nomination of judges, the state investigation bureau said on Monday.  Poroshenko has been embroiled in a number of investigations since leaving office in May.  \"His status is that of a witness,\" a spokeswoman for the state investigation bureau, which handles high-profile cases, told AFP.",
            "contain_image": true,
            "link_on_image": "http://l1.yimg.com/uu/api/res/1.2/gxuHKLF4ZjFgen0ZN5.vRA--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/http://media.zenfs.com/en_us/News/afp.com/9f494baee33192289c2a59c3f93e2bb40c49c4d5.jpg"
        }
    ]
}
```

* "title" - source name\
* "items" - list with dictionary which contains one news information\
    * "title" - headline news
    * "published" - date publication
    * "link" - link
    * "summary" - description
* "links" - this is a list with links to the image of the I-th news

##How is data keeping?

Data keep in local file which is located in directory:
Windows:`C:\Users\User\AppData\Local\Programs\Python\Python38-32\Lib\site-packages\rss_reader`
Linux:\
macOS:

There is only json string in the file. JSON format: 
```
{
   "20191116" : {
      "title" : "News by Sat, 16 Nov 2019 ",
      "items" : [
         {
            "contain_image" : true,
            "link" : "https://news.yahoo.com/chile-police-stopped-rescue-workers-004537157.html",
            "published" : "Sat, 16 Nov 2019 19:45:37 -0500",
            "summary" : "[image: Chile police stopped rescue workers helping dying protester: human rights watchdog]Chile's independent human rights watchdog said on Saturday it would file a formal complaint for murder against police officers who allegedly prevented paramedics from attending a heart attack victim amid a protest Friday.  Security forces firing tear gas, rubber bullets and water cannons made it impossible for rescue workers to properly treat the victim, Chile's publicly-funded National Institute for Human Rights said.  Twenty-nine year old Abel Acuna died shortly after at a nearby Santiago hospital.",
            "title" : "Chile police stopped rescue workers helping dying protester: human rights watchdog",
            "link_on_image" : "http://l1.yimg.com/uu/api/res/1.2/msfkqScfjEDGkZw0FpwuYQ--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/reuters.com/4fcd3b80fd76604f970966b9f77b32bd"
         },
         {
            "contain_image" : true,
            "link" : "https://news.yahoo.com/heres-everything-know-mina-chang-205907562.html",
            "published" : "Sat, 16 Nov 2019 16:39:46 -0500",
            "summary" : "[image: Here's everything we know about Mina Chang, who rapidly rose from a self-described singer to a State Department official with a dubious résumé]A closer look at her history reveals the Trump official may have misrepresented her work history and educational background.",
            "title" : "Here's everything we know about Mina Chang, who rapidly rose from a self-described singer to a State Department official with a dubious résumé",
            "link_on_image" : "http://l.yimg.com/uu/api/res/1.2/SViNbM6UMykaG6aS3FTZPg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/business_insider_articles_888/6ce7057ecba60c171f6ee9381c8db196"
         }
      ]
   }
   "20191115" : {
      "title" : "News by Sat, 15 Nov 2019 ",
      "items" : [
         {
            "contain_image" : true,
            "link" : "https://news.yahoo.com/prince-andrew-didn-t-sex-004304182.html",
            "published" : "Sat, 15 Nov 2019 19:43:04 -0500",
            "summary" : "[image: Prince Andrew: I Didn’t Have Sex With Virginia Roberts Giuffre. I Was Eating Pizza.]Screenshot/BBCNewsnight/TwitterPrince Andrew says he is prepared to give evidence about his friendship with late accused child sex trafficker Jeffrey Epstein under oath, and claimed to have no recollection of the notorious photograph of him with his arm around the waist of alleged Epstein victim Virginia Roberts Giuffre being taken.Inside Jeffrey Epstein’s Creepy Parties With Prince AndrewTo support his latter claim, Andrew told the BBC’s Newsnight program on Saturday that the “traveling clothes” he was wearing in the picture were not clothes he would wear in London. The claim is demonstrably false, as there are images of him leaving London nightclub Chinawhite in July 2000, wearing almost the exact same outfit.Giuffre has accused Prince Andrew of having sex with her on three occasions when she was being trafficked by Epstein, an allegation he has denied. Andrew also insisted he couldn’t have had sex with Roberts on the night she claimed, as he was at a chain pizza restaurant, Pizza Express, in suburban Woking with his daughters. He said the pizza party was at about 4 p.m. or 5 p.m. and then he was at home.He sought to discredit Roberts’ account of dancing with him at Tramp nightclub, in which she described him as sweating profusely, by claiming that he was suffering from a post-combat condition that meant he didn’t sweat. He went on to dispute Giuffre's claim that he bought her a drink, saying he “didn’t know where the bar was” in Tramp, despite admitting having been there several times.“I don’t believe it’s a picture of me in London because... when I go out in London, I wear a suit and a tie. That’s what I would describe as my traveling clothes if I’m going overseas. I’ve got plenty of photographs of me dressed in that sort of kit but not there,” Andrew said.He repeatedly questioned the authenticity of the photograph of him and Giuffre: “I’m afraid to say that I don’t believe that photograph was taken in the way that has been suggested.”He repeatedly said he had “no memory” of the photograph being taken.At one stage he said: “I can’t, we can’t be certain as to whether or not that’s my hand on her left side.”Andrew gave a bewildering array of other reasons to support his claim that the picture was fake, including saying he had never been upstairs in Ghislaine Maxwell’s London home, and that Epstein never carried a camera (in fact, Giuffre claims the photo was taken on her camera).  “Nobody can prove whether or not that photograph has been doctored, but I don’t recollect that photograph ever being taken.”Andrew flatly denied having sex with Giuffre, saying: “Without putting too fine a point on it, if you’re a man it is a positive act to have sex with somebody. You have to take some sort of positive action and so therefore if you try to forget, it’s very difficult to try and forget a positive action and I do not remember anything. I can’t.”“I’ve wracked my brain and thinking oh… when the first allegations, when the allegations came out originally I went, ‘Well that’s a bit strange, I don’t remember this,’ and then I’ve been through it and through it and through it over and over and over again, and no, nothing. It just never happened.”Interviewer Emily Maitlis also asked if Andrew believed rumors that Epstein had not in fact committed suicide.In response, Andrew appeared to show more than just a passing familiarity with the work of celebrity pathologist-for-hire, Dr. Michael Baden, who was hired by Epstein’s brother to observe the official autopsy.Jeffrey Epstein Camp Sent Pathologist Michael Baden to Watch Over His AutopsyAndrew replied: “I’m not one to be able to answer that question. I believe that centers around something to do with a bone in his neck, so whether or not if you commit suicide that bone breaks or something. But I’m afraid to say I’m not an expert, I have to take what the coroner says and he has ruled that it was suicide.”Baden claimed that a collection of neck fractures in Epstein’s hyoid bone and thyroid cartilage were “extremely unusual in suicidal hangings and could occur much more commonly in homicidal strangulation.”In fact, numerous studies show that hyoid and thyroid fractures are not rare in suicidal hangings, especially as people age.Emily Maitlis questions Prince Andrew on 'Newsnight'Screenshot/BBCNewsnight/TwitterMaitlis pressed Andrew about the circumstances in which a photograph was taken of himself and Jeffrey Epstein walking in Central Park, after Epstein had been convicted of a child sex offense. Andrew said he had been staying with Epstein with the express purpose of breaking off his friendship with Epstein because of his child sex conviction. He said that he had decided to break off the friendship in person because he believed it was the “honorable” thing to do. “I felt that doing it over the telephone was the chicken’s way of doing it. I had to go and see him and talk to him,” Andrew said.Asked why he stayed at the home of a “convicted sex offender,” Andrew said: “It was a convenient place to stay. I mean I’ve gone through this in my mind so many times. At the end of the day, with a benefit of all the hindsight that one can have, it was definitely the wrong thing to do. But at the time, I felt it was the honorable and right thing to do, and I admit fully that my judgement was probably colored by my tendency to be too honorable but that’s just the way it is.”Asked about the steady procession of young girls coming and going, Andrew said: “I wasn’t a party to any of that.  I never saw them. I mean you have to understand that his house, I described it more as almost as a railway station if you know what I mean in the sense that there were people coming in and out of that house all the time. What they were doing and why they were there I had nothing to do with. So I’m afraid I can’t make any comment on that because I really don’t know.”Andrew repeatedly denied ever noticing there was anything amiss in Epstein’s behavior, despite, as he said, being a patron of British child protection charity the NSPCC.Andrew admitted that he had stayed with Epstein on his private island and flown on his private jet, and also confirmed that he invited Epstein to a party at Buckingham Palace, a shooting weekend at the Queen’s country estate, and to his daughter’s birthday party.Andrew said he was invited because he was the boyfriend of his old friend, Ghislaine Maxwell.Andrew said he did not regret his friendship with Epstein, saying, “the people that I met and the opportunities that I was given to learn either by him or because of him were actually very useful.”Maitlis later asked again if he regretted ever befriending Epstein, saying: “Do I regret the fact that he has quite obviously conducted himself in a manner unbecoming? Yes.”“Unbecoming?” Maitlis asked in disbelief: “He was a sex offender!”Andrew said: “I’m sorry, I’m being polite, I mean in the sense that he was a sex offender. But no, was I right in having him as a friend? At the time, bearing in mind this was some years before he was accused of being a sex offender. I don’t think there was anything wrong then. The problem was the fact that once he had been convicted… I stayed with him and that’s the bit that, as it were, I kick myself for on a daily basis, because it was not something that was becoming of a member of the royal family and we try and uphold the highest standards and practices and I let the side down, simple as that.”Maitlis asked Andrew if he would “be willing to testify or give a statement under oath if you were asked.”Andrew replied: “Well I’m like everybody else and I will have to take all the legal advice that there was before I was to do that sort of thing. But if push came to shove and the legal advice was to do so, then I would be duty bound to do so.”Maitlis concluded by offering Andrew the opportunity to say “anything you feel has been left unsaid that you would like to say now?”“No, I don’t think so,” drawled Andrew. “ I think you’ve probably dragged out most of what is required.”Read more at The Daily Beast.Get our top stories in your inbox every day. Sign up now!Daily Beast Membership: Beast Inside goes deeper on the stories that matter to you. Learn more.",
            "title" : "Prince Andrew: I Didn’t Have Sex With Virginia Roberts Giuffre. I Was Eating Pizza.",
            "link_on_image" : "http://l2.yimg.com/uu/api/res/1.2/hxEVKpLLNwh0Yqb4N6xvSg--/YXBwaWQ9eXRhY2h5b247aD04Njt3PTEzMDs-/https://media.zenfs.com/en-US/thedailybeast.com/1ca9a23aefca6c158388b9b9ab47eadc"
         }
      ]
   }
}
```