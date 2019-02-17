# alfred-bookmark

[Alfred 3 workflow](https://www.alfredapp.com/workflows/) to manage Browser's bookmark.
It is tested on Google Chrome and Safari.

## Install 

To install, download the latest file and double-click to open in Alfred 3. 

## Setup & Keys

![](https://cl.ly/5ffd060608d0/Screenshot%20of%20Alfred%20Preferences%20(2-8-19,%2011-56-21%20AM).jpg)

- Add Bookmark (Configurable: **F5**)
- Search Bookmark - Supports Incremental search (Configurable: **F1**)

- Edit Bookmark (mod:`Ctrl` in search mode, `Enter` in add mode)
- Delete Bookmark (mod:`Option`)
- Copy Bookmark (mod:`Command`)
- Open Bookmark in Google Chrome Incognito mode (mod:`Shift`)
- Quick Look URL (`Shift`)

## Usage

### Search Bookmark (F1)

![](https://cl.ly/f5fd62635794/search.png)

### Add Bookmark (F5)

![](https://cl.ly/edac6d3969fc/add.png)

#### Search terms

You can search any terms (order does *not* matter).

####  Bookmark Sort order

- Accessed, launch count, registered time (default)     

#### Sync between several machines 
You can sync bookmark database through several machine via DropBox.

```
mv '~/Library/Application Support/Alfred 3/Workflow Data/com.jmjeong.alfred-bookmark/pinboard.db' ~/Dropbox/Apps
ln -s ~/Dropbox/Apps/pinboard.db '~/Library/Application Support/Alfred 3/Workflow Data/com.jmjeong.alfred-bookmark/'
```
