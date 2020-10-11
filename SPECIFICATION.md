# Project Specification

This is a specification for my Udacity capstone project for the Full-Stack Developer Nanodegree. This may be subject to change but my intention is to plan all functionality of the project before implementing.

### Title
Flat Tutorials

### Outline
Flat Tutorials will be a publishing application for text-based tutorials. The tutorials will be formatted in Markdown. Users can specify tags relating to whichever technologies are covered. Tags will have versions as well.

### Implementation
- Back end: Flask-SQLAlchemy
- Front end: React

### Roles and Privileges
1. User
	- Submit tutorials for publication
	- Submit edits to tutorials authored by User
	- Delete tutorials authored by User
2. Moderator
	- Approve or deny tutorials
3. Admin
	- Promote and demote Users and Moderators

### Models
1. Tutorial
2. Tag
3. Version
4. User

### Views
1. Front Page
2. Display Tutorial
3. Display Tutorial list
4. Author Profile
6. Edit/Write Tutorial

### API Endpoints
- Get Tutorial
- Post Tutorial
- Patch Tutorial
- Delete Tutorials
- Tutorial List by Author
- Unpublished Tutorials
- Get Tutorial List
- Search Tutorials
- List by tag
- List by two tags
