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

- pbauth username:TOKEN <- set access token
  - Get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
- pbreload - loads latest bookmarks from pinboard.in

- (optional) pbauthpocket 
  - needed only if you want to send URL to pocket
- (optional) install cron job  : for faster search without pbreload
  - download it from [pinboard-download.py](https://gist.github.com/jmjeong/6986c9db0cc193f5b51d)
  - You need to set PINBOARD_TOKEN in `pinboard-download.py`
  - `chmod a+x pinboard-download.py`
  - register script in crontab using `crontab -e`
    - `*/15 * * * * /path/to/pinboard-download.py  > ~/.bookmarks.json > /dev/null 2>&1`
	
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

- v1.6 (2014-04-12)
  - add encoding parameter to xml output
  - add subtitle in output
- v1.4 (2014-03-26)
  - url part is not displayed to increase max of search result
  - limit search result to 100
- v1.3 (2014-03-04)
  - Fix a bug that items are not displayed sometimes
- v1.2 (2014-02-24)
  - Remove the dependency of cron job 
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
