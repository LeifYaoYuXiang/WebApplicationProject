# WebApplicationProject
## Before You Grade:
- **Please don't delete the database**: one dangerous action, since the file information is saved in the database, if you delete them, "resources download function" will be invalid
## Functionality Provided
### General Overview
In this project, I design my own web blog. It enables visitors to see my published blogs, albums and resources. People can make comments on my blogs, make suggestions, and download resources. In addition, people can make suggestions.
### Functionality Details
- Blog List Presentation
- Search Blog
- Blog Rankings
- Blog Content Presentation
- Blog Comment Commit
- Resources List Presentation
- Resources Search
- Resources Download
- Album Presentation
- Photo Presentation
- Suggestions Commit
- Log In Commit
- Sign In Commit
- Log Out Commit
## Architecture 
### Directory 
- .git
- .idea
- \_\_pycache \_\_
- blogapp
	- \_\_pycache \_\_
	- static
	  - assets
	  -  js
	  -  css
  - templates
  - \_\_init\_\_.py
  - blogdb.db
  - config.py
  - form.py
  - models.py
  - routes.py
- static
- templates
- venv
- .flaskenv
- microblog.py
- README.md
### Database
Table：  *blog*

| Field | Meaning |
| ----- | ------- |
| id    | the id of one blog |
| title| the title of one blog |
| tag | the tag belongs to this blog |
| time | the time when one blog is published |
| click | how many times this blog has been viewed |
Table： *comment*

| Field       | Meaning                                                    |
| ----------- | ---------------------------------------------------------- |
| id          | the id of one comment                                      |
| information | the content of one comment                                 |
| blog_id     | this blog id to identify the blog the comment committed on |
| user_id     | this blog id to identify the user who commit the comment   |

Table:  *user*

| Field         | Meaning                       |
| ------------- | ----------------------------- |
| id            | the id of one user            |
| username      | the name of one user          |
| email         | the email of one user         |
| password_hash | the hash password of one user |

Table： *resource*

| Field       | Meaning                                         |
| ----------- | ----------------------------------------------- |
| id          | the id of one resource                          |
| name        | the name of one resource                        |
| tag         | the tag belong to one resource                  |
| description | the brief description of one resource           |
| download    | how many times one resource has been downloaded |

Table:  *suggestion*

| Field      | Meaning                                          |
| ---------- | ------------------------------------------------ |
| id         | the id of one suggestion                         |
| suggestion | the content of one suggestion                    |
| user_id    | the user id to identify who make this suggestion |

