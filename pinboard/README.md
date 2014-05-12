# Introduction 

Yet another alfred2-pinboard workflow. It provides INSTANT pinboard search and the following function.

- search pinboard (`pba`)
- search tag (`pbtag`)
- goto or delete the searched bookmark 
- copy url of the searched bookmark

- search pinboard memo (`pbmemo`)

![screenshot](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/pbhelp.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/search.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/pbtag.jpg)
![screenshot](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/pbtag-search.jpg)

# Installation 

0. Download and Install [alfred-pinboard Workflow](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/pinboard.alfredworkflow)

1. pbauth username:TOKEN <- set access token
    - Get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
2. pbreload - loads latest bookmarks and memo from pinboard.in
3. search with `pba`, `pbtag`, `pbmemo` command

---

- (optional) pbauthpocket 
    - needed only if you want to send URL to pocket
- (optional) install cron job  : for faster searching without pbreload
    - download it from [pinboard-download.py](https://raw.github.com/jmjeong/alfred-extension/beta/pinboard/pinboard-download.py)
    - `chmod a+x pinboard-download.py`
    - register script in crontab using `crontab -e`
          `*/15 * * * * /path/to/pinboard-download.py  > ~/.bookmarks.json > /dev/null 2>&1`
	

# Command

- **pba** *query* : search *query* from description and link and tags
- **pbnote** *query* : search *query* from pinboard notes
- **pbu** *query* : search *query* from description(title) in unread list
- **pbl** *query* : search *query* from link
- **pbtag** *query* : search tag list. You can autocomplete it by pressing 'tab'
- **pbreload** : loads latest bookmarks from pinboard.in
- **pbauth** *username:token* : Set pinboard authentication token (optional)
- **pbauthpocket** : Pocket authentication (optional)

## Keys 

You need to set it manually because of alfred restriction

- ctl-shift-cmd-p : launch **pba** 
- ctl-shift-cmd-c : launch **pbtag** 
- ctl-shift-cmd-n : launch **pbnote** 

# Action

- *enter* to open the selected url in the browser
- *tab* to expand in pbtag command
- Hold *cmd* while selecting a bookmark to copy it’s url to clipboard
- Hold *alt* while selecting to delete a bookmark from your pinboard
- Hold *shift* while selecting to send URL to pocket. You need to set auth_token using **pbauthpocket**

# Change Log

- v2.0
  - move the location of config file from workflow directory to data directory. you need to run
    `pbauth` again
  - add pbnote query
  - remove pbt, pbl, pbe because they are not used frequently
  - change search condition
	  - *' '* stands for **and** query `ex) python alfred`
	  - Add a dash(`-`) before a word to exclude all results that include that word `ex) python -alfred`
  - add the number of links in the first line		

- v1.8 (2014-04-29)
  - escape url character for compatibility 
  - support or(|) operator in search
- v1.7 (2014-04-29)
  - retain item order of the result
  - don't limit the number of output
  - change the encoding of output to 'NFD'
- v1.6 (2014-04-28)
  - some tweak for xml output (item order)
  - fix typo in delete routine 
- v1.5 (2014-04-12)
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
