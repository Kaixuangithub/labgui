# README #

Watch the video high-lighting the advantages of LabGui over LabView
https://www.youtube.com/watch?v=NH5Nc5k7Jrk
Slides used in the video and the script are in the README/ folder.

### What is this repository for? ###

This is to communicate with scientific measure instruments and collect data using these instruments, plotting the data, fitting the data and saving it into files. It does the job and it is much simpler than LabView for more complicated experiences.


### How do I get set up? ###

* Summary of set up
You go in the recordsweep folder and look for LabGui.py, then you run that file.
The configuration details are contained in the file named config.txt

We haven't yet written a nice package that you can install through python (if you know how to do that we would love to learn from an expert!)


* Requirements
-Python 2.7 (you can install python XY on windows)
-PyVisa (and the additionnal NI-Visa, you can find more info on pyvisa and NI-Visa here : http://pyvisa.readthedocs.org/en/master/

* Dependencies
not done yet 

* How to run tests
not done yet

* Deployment instructions
You might have to add the folders to your python path manually, if you know how to automate that process I will be happy to learn that!
You need to add the "recordsweep" and "driver" folders

The configuration details are contained in the file named config.txt, you can use the file config_example.txt and rename it.

You can set a Debug mode, it means it will never actually connect to any instrument but to their debug version instead, this is useful to test your interface when you are not in the lab.



### Who do I talk to if I encounter problems? ###

We wanted to have more people using our programm although it could (and should) be more commented and explained, we guessed the best way to know where we lack good explanations is to have people try to use our programm. As there will be a workshop in McGill on May 19th 2015 this will likely trigger questions and lead to a better help and readme file!

* Repo owner pfduc@physics.mcgill.ca or schmidtb@physics.mcgill.ca
