# Introduction 

Yet another alfred2-pinboard workflow. It provides INSTANT pinboard search and the following function.

- search pinboard
- search tag 
- search description 
- delete searched bookmark 
- copy url of bookmark
- send to pocket

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pbhelp.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/search.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pbtag.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pbtag-search.jpg)

# Installation 

- (mandatory) install cron job
  - */10 * * * * (curl 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=username:TOKEN' > ~/.bookmarks.json) > /dev/null 2>&1
  - get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
- (optional) pbauth username:TOKEN <- set access token
  - Only need if you want to delete the bookmark or reload bookmark
- (optional) pbauthpocket 
  - Only need if you want to send URL to pocket
	
- [Workflow Download](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pinboard.alfredworkflow)

# Command

- **pba** *query* : search *query* from description and link and tags
- **pbt** *query* : search *query* from description(title)
- **pbl** *query* : search *query* from link
- **pbd** *query* : search *query* from extended field
- **pbu** *query* : search *query* from description(title) in unread list
- **pbtag** *query* : search tag list. You can autocomplete it by pressing 'tab'
- **pbreload** : loads latest bookmarks from pinboard.in
- **pbauth** *username:token* : Set pinboard authentication token (optional)
- **pbauthpocket** : Pocket authentication (optional)
- ctl-shift-cmd-p : launch **pba** (reset when importing)
- ctl-shift-cmd-c : launch **pbtag** (reset when importing)

# Action

- *enter* to open the selected url in the browser
- Hold *cmd* while selecting a bookmark to copy it’s url to clipboard
- Hold *alt* while selecting to delete a bookmark from your pinboard
- Hold *shift* while selecting to send URL to pocket. You need to set auth_token using **pbauthpocket**

# Change Log 

- v1.1 (2014-02-23)
  - add send-to-pocket in shift
  - limit search result to 16
- v1.0 (2014-02-22)
  - delete bookmark
  - reload bookmarks
- v0.9 : pre-release

# License 

- MIT License

# Credits

- Author : [Jaemok Jeong](mailto:jmjeong@gmail.com)
- Inspired by the following tips 
	- [INSTANT Pinboard Search](https://gist.github.com/myfreeweb/5189568)
	- [Pinboard Search Workflow](http://www.alfredforum.com/topic/979-pinboard-search-workflow/)
	- [Pocket for alfred](https://github.com/altryne/pocket_alfred) - oAuth authentication code
