# Introduction 

Yet another alfred-pinboard workflow. It provides INSTANT pinboard search and the following function.

- search pinboard (`pba`) - supports various search condition such as `or(|)`, `and( )`, and `not(-)`
- search tag : Type `pba #`
- search untagged entries : Type `pba # :`
- search pinboard memo (`pbmemo`)
- show starred bookmark (`pbs`)
- browse and search history (`pbhis`)
- browse launch history (`pblog`)

- goto or delete the searched bookmark 
- copy url of the searched bookmark
- send url to pocket
- mark or unmark the favorite bookmark

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/search.jpg)

# Installation 

0. Download and Install [alfred-pinboard Workflow](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pinboard.alfredworkflow)
	- You need to set short-key manually
1. pbauth username:TOKEN <- set access token
    - Get it from [https://pinboard.in/settings/password](https://pinboard.in/settings/password)
2. pbreload - loads latest bookmarks and memo from pinboard.in
3. search with `pba`, `pbmemo`, `pbl`, and `pbu` command

---

- (optional) pbauthpocket 
    - needed only if you want to send URL to pocket
- (optional) install cron job  : for faster searching without pbreload
    - download it from [pinboard-download.py](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pinboard-download.py)
    - `chmod a+x pinboard-download.py`
    - register script in crontab using `crontab -e`
	
      `*/15 * * * * /path/to/pinboard-download.py > /dev/null 2>&1`
	
# Command

- **pba** *query* : search *query* from title, description and tags
- **pbnote** *query* : search *query* from pinboard notes
- **pbu** *query* : search *query* from description(title) in unread list
- **pbl** *query* : search *query* from link
- **pbs** *query* : search *query* from starred bookmarks
- **pba #** *query* : search tag list. You can autocomplete it by pressing `tab` or `enter`

- **pbhis** : show search history
- **pblog** : show launch history

- **pbreload** : loads latest bookmarks from pinboard.in

- **pbauth** *username:token* : Set pinboard authentication token (optional)
- **pbauthpocket** : Pocket authentication (optional)

## Search Condition

- `-` before search word stands for **not** `ex) -program`
- ` ` stands for **and** query `ex) python alfred`
- `|` stands for **or** query `ex) python|alfred`
- **and** query is evaluated first, than **or** query is processed

## special keys

- `#` : select tag
- `^` : sort option (^a title ascending, ^z title descending, ^d time ascending, ^l last accessed time)

## Keys 

You need to set it manually because of alfred restriction

- ctl-shift-cmd-p : launch **pba** 
- ctl-shift-cmd-c : launch **pba #** 
- ctl-shift-cmd-n : launch **pbnote**
- ctl-shift-cmd-s : launch **pbs**
- ctl-shift-cmd-h : launch **pbhis**
- ctl-shift-cmd-l : launch **pblog**

## Action

- *enter* to open the selected url in the browser
- Hold *cmd* while selecting a bookmark to copy it’s url to clipboard
- Hold *alt* while selecting to delete a bookmark from your pinboard
- Hold *ctrl* while selecting a bookmark to mark or unmark it
- Hold *shift* while selecting to send URL to pocket. You need to set auth_token using
  **pbauthpocket**

# Screenshot

## Help

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pbhelp.jpg)

## Search 

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/search.jpg)

## Tag Browse

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pbtag.jpg)

## Tag Search

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pbtag-search.jpg)

## Multiple Tag Group Search

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/multi-tag-search.jpg)

## Starred Bookmark

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pbs.jpg)

## Search History

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/pbhis.jpg)

## Sort option

![screenshot](https://raw.github.com/jmjeong/alfred-extension/master/alfred-pinboard/sort-option.jpg)

# Change Log

- v2.24 (2014-07-14)
  - pbload records `copy` command
  - guard code for invalid bookmark data
- v2.22 (2014-06-20)
  - Launch history command (`pblog`)
  - Sort option : last accessed time (`^l`)
  - '!' is used to sort key too
  
- v2.11 (2014-06-15)
  - multiple tag search : specify tag group for searching (#)
  - display last modified time of local cached bookmarks
  - display host name only in main list
  - display tag information in main list too
  - update the number of entries in the history list after searching
  - display untagged bookmarks in tag list
  - support sort option : title ascending(`^a`), title descending(`^z`),
	time ascending(`^d`), time descending(default)

- v2.0 (2014-05-26)
  - move the location of config file from workflow directory to data directory. you need to run
    `pbauth` again
  - add `pbnote` query
  - starred/unstarred bookmark `pbs`
  - remove pbt, pbl, pbe because they are not used frequently
  - change search condition
	  - *' '* stands for **and** query `ex) python alfred`
	  - *'|'* stands for **or** query `ex) python|alfred`
	  - Add a dash(`-`) before a word to exclude all results that include that word `ex) python -alfred`
  - add the number of links in the first line
  - browse *search history* `pbhis`

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
