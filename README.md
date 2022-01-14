

# Table of contents

 - [Locker - CRM (CS50 Web Capstone)](#locker---crm-cs50-web-capstone)
  - [Locker Features](#locker-features)
  - [Distinctiveness and Complexity](#distinctiveness-and-complexity)
  - [Tech Stack](#tech-stack)
  - [Python Requirements](#python-requirements)
  - [Installation](#installation)
  - [Running your local server](#running-your-local-server)
  - [File structure](#file-structure)
  - [Sale Process summary](#sale-process-summary)
  - [Preview](#preview)
  - [User Guide](#user-guide)
    - [Registration](#registration)
    - [Creating Companies](#creating-companies)
    - [Adding People](#adding-people)
    - [Creating Pipelines](#creating-pipelines)
      - [Adding stages](#adding-stages)
      - [Editing a stage name](#editing-a-stage-name)
      - [Adding stage tasks](#adding-stage-tasks)
    - [Creating Products](#creating-products)
    - [Creating Leads](#creating-leads)
    - [Working with a Lead](#working-with-a-lead)
      - [Finding a lead](#finding-a-lead)
      - [Completing stage tasks](#completing-stage-tasks)
      - [Changing the status of a lead](#changing-the-status-of-a-lead)
      
# Locker - CRM (CS50 Web Capstone)
Before the Internet, it was much easier to keep track of contacts and customer information. Now, because we can connect on such a vast level, it can be much more difficult to manage contacts and customer data. This is where Locker comes into play.

Locker is an easy to understand, easy to use, and easy to access Customer Relationship Management (CRM) tool. Locker is built for managing all your company’s relationships and interactions with current and potential customers.  

## Locker Features
The current release of Locker is limited to one user per registered customer. Each user has access to the following modules:

 1. **Companies**: this module provides the ability to view and create a list of current and potential businesses you may be in business with. 
 2. **People**: this module allows you to view and create a list of people for each current or potential customer created.
 3. **Pipelines**: the Pipelines module lets you define a set of stages and tasks that each lead needs to go through to completion. 
 4. **Leads**: this module lets you view and create a list of potential sales to your business.
 5. **Products**: this module enables you to view and create a list goods/services your businesses provides. 


Near future releases of Locker will include a users module.

## Distinctiveness and Complexity
The nature of Locker differs from all previously submitted projects. It has been emphatically stated that the final project may not appear to be a social network application nor an e-commerce site. Locker is a customer relationship management application, which is aimed at improving business relationships of an organization. Therefore, Locker may not be assimilated to all other CS50 Web projects.

It was additionally stated the final project should be more complex than the previously submitted projects. It is reasonable to say that Locker's scope of work is greater than the previous projects, which contributes to the complexity of implementation. Furthermore, the implementation of the business logic is fairly more challenging to get correctly. In addition to logic, the project required to learn the usage of new javascript libraries such as, but not limited to charts libraries used to implement the dashboard. 

This project was fairly more challenging to implement than any previous project. Even more time and care was infested into the implementation of Locker, which has greatly contributed to expanding our abilities. 
## Tech Stack
* Python (Django)
* Javascript 
* HTML
* CSS
## Python packages
* asgiref==3.2.10
* Django==3.1.6
* django-rest-framework==0.1.0
* djangorestframework==3.12.2
* pytz==2019.3
* sqlparse==0.3.0


## Installation

 1. Clone repository
       ```
		 git clone https://github.com/jeanjoelkapula/locker.git 
	 ```
 3. cd into the project folder
 4. Install the project requirements 
	 ```
			 pip install -r requirements.txt
	 ```
	 

## Running your local server

 1. Ensure you have made all migrations
	```
	>> python manage.py migrate
	```
1. Start the server
	```
	>> python manage.py runserver
	>> python manage.py migrate
	```
## File structure
```
	-> capstone \:this folder contains the default created files for a project
	------> asgi.py
	------> settings.py: this file contains the entire project settings
	------> urls.py: this file contains the url patterns for all apps
	------> wsgy.py 
	-> CRM
	------> migrations \: this folder contains the sql migrations files
	------> static \: this folder contains site assets (js, css, img)
	------> templates \: the app html files are in this folder
	------> templatetags \: this folder contains custom template filters 
	------> admin.py: this file registers models to be used in the admin portal
	------> apps.py: this file contains the app config
	------> forms.py: this file contains all ModelForm definitions
	------> models.py: this file contains all Model definitions
	------> tests.py
	------> urls.py: this file contains all url patterns for the CRM app
	------> util.py: this file contains all helper functions 
	------> views.py: this file contains the view functions the CRM app
	-> manage.py 
		
```

## Sale Process summary
![Locker Sale Process Summary](https://user-images.githubusercontent.com/44115772/149214273-01158f18-58f7-420a-be56-999f6083973b.png)
## Preview
![image](https://user-images.githubusercontent.com/44115772/149214685-78b9f54f-0b61-4dd4-80eb-28e8610f0f52.png)
![image](https://user-images.githubusercontent.com/44115772/149215084-276048b8-5433-4ae1-ad07-16de61fff3dd.png)
![image](https://user-images.githubusercontent.com/44115772/149216429-95f5d5ac-fa7d-4eed-a8aa-8221bad8b2bb.png)
![image](https://user-images.githubusercontent.com/44115772/149215289-65050ccb-9eab-475c-9ee1-f4b6d6b0d8e2.png)

## User Guide

### Registration
![Register](https://user-images.githubusercontent.com/44115772/149371463-3de70a9e-7de7-4744-8695-65272ac7fe3b.png)
### Creating Companies
![Companies_create](https://user-images.githubusercontent.com/44115772/149371905-d9236e04-7381-47c2-a0eb-7451d868e7bf.png)
### Adding People

![people_create](https://user-images.githubusercontent.com/44115772/149372221-68ecac08-5cff-4adf-9ee7-2f3a86ba5d5b.png)
### Creating Pipelines
#### Adding stages
![enter image description here](https://user-images.githubusercontent.com/44115772/149375454-dba0c2a5-eaa0-453e-8680-a627f460ecaa.png)
#### Editing a stage name
![enter image description here](https://user-images.githubusercontent.com/44115772/149376859-526abeec-93bb-496e-a2ca-78adb92846af.png)
#### Adding stage tasks
![enter image description here](https://user-images.githubusercontent.com/44115772/149378059-98c48477-1cbe-44a5-92fc-44f2953e15f3.png)
### Creating Products
![product create](https://user-images.githubusercontent.com/44115772/149383688-08b66953-001b-4ab9-95ca-f01f2b7ff739.png)


### Creating Leads
![lead create](https://user-images.githubusercontent.com/44115772/149379225-6fa2bc50-4d73-4827-9a72-bd737118c1ad.png)
### Working with a Lead
#### Finding a lead

![lead list](https://user-images.githubusercontent.com/44115772/149381312-63065c31-cdff-40ab-beed-cd96fc845b3d.png)
#### Completing stage tasks
![stage complete](https://user-images.githubusercontent.com/44115772/149382699-50cbc050-c6a7-44b1-87ad-b1c4b2c533db.png)
#### Changing the status of a lead
![lead status](https://user-images.githubusercontent.com/44115772/149383130-2d65d1b3-4238-4f04-b613-f1e1f1a30b9d.png)


