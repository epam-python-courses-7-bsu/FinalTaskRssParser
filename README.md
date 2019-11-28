# FinalTaskRssReader
For final task pull requests.


## How to create a pull request

1. Create github account.  *Preferrably using email you used when registerer on this course*  
2. Fork this repository. ('Fork' button at the top right of this repository page)  
3. Open the page of your  *new repository*  that was created when you forked this repo.  
4. Press button clone or download at the middle right of the page and CTRL-C the url.  
5. On your machine go to the directory you want.  
6. Depending on the OS you are working with, open GitBash(Windows)/Command Line or Terminal(Linux) there  
7. Use command  `git clone <url_you_copied>`  
  
Congrats! You have successfully forked our repository.


## Additional project structure requirements

1. `setup.py` file for setuptools  *must*  be in the root of  `final_task`  folder. Use  `setup.py`  that is already there. (that means path to this file must end with  `final_task/setup.py` )  
2. Entry point to your application, aka its main module  *must*  be named as  `rss_reader.py` . Use  `rss_reader.py`  that is already in  `rss_reader`  folder.  
3. You should describe how does your project work, how to launch it and etc in README.md in the  `final_task/README.md`  file.  
4. If you used any non-standart libraries they must be listed in  `rss_reader/requirements.txt`  file.  
5. All unit test files should be in separate folder called `tests`.


## Pull request requirements(!!!)

1. When creating pull request make sure that  `target branch`  is  `master`  on OUR repo, not yours.  
2. Pull request name  *MUST*  be in format:  `YourFirstName_YourLastName_EmailYouUsedWhileRegisteringOnThisCourse`  
3. Pull request which have any other name format, or invalid e-mail  *will be ignored completely until you fix it*. So make sure you specified correct e-mail.  
4. In pull request description specify your current iteration. You also can add there any other info you want us to know before we start code review.  
5. *Pull request must NOT contain any .pyc files, any virtual environment files/folders, any IDE technical files*.