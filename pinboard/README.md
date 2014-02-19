# Introduction 

Yet another alfred2-pinboard workflow. It provides INSTANT pinboard search and various search command.

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/screenshot.jpg)

# Installation 

- (mandatory) install cron job
	- */10 * * * * (curl 'https://api.pinboard.in/v1/posts/all?format=json&auth_token=username:TOKEN' > ~/.bookmarks.json) > /dev/null 2>&1
	- get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
- (optional) pbauth username:TOKEN <- set access token 
	- Only need if you want to delete the bookmark or to change its status to read
	
- ([Download](https://raw.github.com/jmjeong/alfred-extension/master/pinboard/pinboard.alfredworkflow))


# Command

- pba query : search query from all field
- pbt query : search query from description(title)
- pbl query : search query from link
- pbd query : search query from extended field
- pbu query : search query from description(title) in unread list
- pbtag query : search tag list. You can autocomplete it by pressing ‘tab’

# Action

- Open the selected url in the browser by enter
- Hold *cmd* while selecting a bookmark to copy it’s url to clipboard
- Hold *ctl* while selecting to delete a bookmark from your pinboard. (not yet)
- Hold *shift* while selecting to change a bookmark to read. (not yet)

# Change Log 

- v0.9 : pre-release

# Credits

Inspired by the following tips 

- [INSTANT Pinboard Search](https://gist.github.com/myfreeweb/5189568)
- [Pinboard Search Workflow](http://www.alfredforum.com/topic/979-pinboard-search-workflow/)
