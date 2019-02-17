# alfred-bookmark

[Alfred 3 workflow](https://www.alfredapp.com/workflows/) to manage Browser's bookmark.
It is tested on Google Chrome and Safari.

## Install 

To install, download [the latest file](https://github.com/jmjeong/alfred-extension/raw/master/alfred-bookmark/alfred-bookmark.alfredworkflow) and double-click to open in Alfred 3. 

## Setup & Keys

<img src="https://cl.ly/31bb608680b5/download/Screenshot%20of%20Alfred%20Preferences%20(2-18-19,%202-24-43%20AM).png" width="720px"> 

- Add Bookmark (Configurable: **F5**)
- Search Bookmark - Supports Incremental search (Configurable: **F1**)

- Edit Bookmark (mod:`Ctrl` in search mode, `Enter` in add mode)
- Delete Bookmark (mod:`Option`)
- Copy Bookmark (mod:`Command`)
- Open Bookmark in Google Chrome Incognito mode (mod:`Shift`)
- Quick Look URL (`Shift`)

## Usage

### Search Bookmark (F1)

<img src="https://cl.ly/f5fd62635794/search.png" width="640px">

### Add Bookmark (F5)

<img src="https://cl.ly/edac6d3969fc/add.png" width="640px">

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
