# Introduction 

Yet another alfred2-pinboard workflow. It provides INSTANT pinboard search and various functionality.

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/screenshot.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/search.jpg)

# Installation 

- (mandatory) install cron job
	- */10 * * * * (curl 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=username:TOKEN' > ~/.bookmarks.json) > /dev/null 2>&1
	- get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
- (optional) pbauth username:TOKEN <- set access token
	- Only need if you want to delete the bookmark or to change its status to read
	
- [Workflow Download](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pinboard.alfredworkflow)

# Command

- **pba** *query* : search *query* from description and link and tags
- **pbt** *query* : search *query* from description(title)
- **pbl** *query* : search *query* from link
- **pbd** *query* : search *query* from extended field
- **pbu** *query* : search *query* from description(title) in unread list
- **pbtag** *query* : search tag list. You can autocomplete it by pressing 'tab'
- **pbreload** : loads latest bookmarks from pinboard.in
- **pbauth** *username:token* : Set pinboard authentication token
- ctl-shift-cmd-p : launch **pba** (reset when importing)
- ctl-shift-cmd-c : launch **pbtag** (reset when importing)

# Action

- Open the selected url in the browser by enter
- Hold *cmd* while selecting a bookmark to copy it’s url to clipboard
- Hold *alt* while selecting to delete a bookmark from your pinboard. (not yet)
- Hold *shift* while selecting to change a bookmark to read. (not yet)

# Change Log 

- v0.9 : pre-release

# License 

MIT License

# Credits

Inspired by the following tips 

- [INSTANT Pinboard Search](https://gist.github.com/myfreeweb/5189568)
- [Pinboard Search Workflow](http://www.alfredforum.com/topic/979-pinboard-search-workflow/)
