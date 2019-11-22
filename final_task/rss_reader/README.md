#JSON structure:
####1) for news from the internet:
    {   
     "feed":    {
                 "feed_title": feed title,
                 "feed_language": feed language
                }
    
     "entries":
         [
               {                  
                 "title": news title,
                 "summary": news content,
                 "date": news publication date,
                 "link": news link },
               
               {  
                 "title": news title,
                 "summary": news content,
                 "date": news publication date,
                 "link": news link },

               ...
               
         ]
    }
    
####2) for news from the local storage:
     [
               {      
                 "feed_title": feed title,
                 "feed_language": feed language,            
                 "title": news title,
                 "summary": news content,
                 "date": news publication date,
                 "link": news link },
               
               {  
                 "feed_title": feed title,
                 "feed_language": feed language, 
                 "title": news title,
                 "summary": news content,
                 "date": news publication date,
                 "link": news link },

               ...
               
         ]
