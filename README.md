## NAME
Library Management System

## DESCRIPTION
A locally hosted **Open Source** mini web based application built using the **Django** development framework, **sqlite** database and **Bootstrap**.

### Base technologies
|Technolgy     | Version         |
|------------- | -------------   |
|Python        | 3.8 and higher  |
|pip           | 22.0 and higher |
|sqlite        | 3.9 and higher  |
|Django        | 4.0             |
|Bootstrap     | 5.x             |

- - - -

## INSTALLATION
Note: Please ensure that atleast **python 3.8** and **pip** are installed on you machine before you follow the procedure. 

1. Install [virtualenv](https://docs.python.org) on your machine:
* __For windows__:  
```
$ python -m pip install virtualenv
```
* __For Linux and Mac OS__:  
```
$ pip install virtualenv 
```
2. Create a directory called LMS and move into that directory:   
```
$ mkdir LMS
$ cd LMS
```

3. Clone this projects public repository from [gitlab](https://gitlab.com):  
```
$ git clone https://gitlab.com/12th2/g12-library-system.git
```

4. Change the current working directory into the cloned projects directory:  
```
$ cd g12-library-system
```

5. Create a new virtual environment to manage the projects local modules:  
```
$ virtualenv lms-env
```

6. A new folder lms-env will be created in the current directory.  
* __On Windows activate the environment using:__   
```
$ lms-env\Scripts\activate
```

* __On linux and Mac OS activate the environment using:__   
```
$ source lms-env/bin/activate  
```

You should see the name __lms-env__ in brackets on your terminal line eg    
```
$(lms-env)user@laptop:~$
```

6. Install the project dependencies:  
```
$ pip install -r requirements.txt
```

7. Start the project using:    
```
$ python manage.py runserver
```

## SYSTEM USAGE
The system should ideally be used by a librarian to manage the library's daily activities. It should improve __book record keeping__ and __save time in related processes__. It should also enable the librarian to __manage book transactions more effectively__. 
Customers can also __request for books__ through the system.

## SUPPORT
__Email__ any of the project contributors:
* joelofelectronics@gmail.com
* leonardobilly8@gmail.com
* eleazarmish@gmail.com 

## CONTRIBUTIONS
The Project is open to contributions in form of feature ideas or code.   
Ideas can be __emailed__ to the owner @eleazarmish@gmail.com

## AUTHORS AND ACKNOWLEDGEMENT
Project contributors:  
__Joel Steven Ssekyewa__ @joel_of_electronics
__Kalanzi Grace__ @gracemercy
__Eleazar Misheal__ @eleazarmish
__Leonard Billy Ssekanjako__ @leonardobilly8

## LICENSE
The project is __open source__, there is __no__ use warrantly. 

## PROJECT STATUS
The project is currently under __active development__. 
