## things ([Download](https://raw.github.com/jmjeong/alfred-extension/master/things/things.alfredworkflow))

Add to Things workflow. Supports date parsing for easy input.

![Screenshot](https://raw.github.com/jmjeong/alfred-extension/master/things/screenshot.jpg)

###  Usage

```
t title #tag @t|n|s ::note > duedate (ex. fri, 3d, 2w, 12/31)
tm title #tag @t|n|s ::note > duedate 
```
- `t` : create todo
- `tm` : create todo with clipboard contents as a note

- Syntax
	- #tag : tag
	- Focus : default location is 'Inbox'
		- @t : @Today 
		- @n : @Next
		- @s : @Someday
	- ::note : note
	- > duedate
		- > : today
		- > 2d : two days after
		- > fri : next friday 
		- > -1d : one day before 
		- > 11/23 : November 23

### Version History 

#### 1.16 - Nov 29, 2016

- fix a bug in v1.15

#### 1.15 - Nov 25, 2016

- fix parsing error containing '>' (for example, '1->2 test >1d')


#### 1.14 - Nov 17, 2016

- unicode tag support

#### 1.13 - Nov 16, 2016

- add Focus syntax - @t|n|s

#### 1.12 - Nov 16, 2016

- support previous day/week/month like '-3d'
- support month for duedate such as '2m'
- '>' denotes 'today'

#### 1.1 - Nov 16, 2016

- change command to 't, tm'
- add `tm` command - create todo with clipboard contents as a note
- show item location after creation

#### 1.0 - Nov 15, 2016

- initial release
