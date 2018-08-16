# upwise python assignment

Goal:
We want to write a program to harvest Github data, process it, and then saves it to a database.

Flow:
Our program needs to fetches repos for specific usernames using Github’s REST API. 

The user names are stored in a text file (the file is part of this repo)

For each user’s list of repos, we want to extract the repos with the most “stars”, and insert that repo’s name into our DB. 

We also want to print a list of all the repos we inserted after everything is done.

Concurrency : 
Our goal is to fetch at least 8 users at the same time from Github. To do this, use python concurrent map.

Error handling:
We want to handle errors from the github API and the DB. If an error occurs, 

Coding style:
Please do things in a “pythonic” way, and use OOP.


*** Please commit code to a branch with your name *** 


The test DataBase details - are in the document

Table : github_repo
columns : 
Id - auto_increment
Repo_name - where the “star” repo names need to go.
