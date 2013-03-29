## Manage Alfred Extension ([Download](https://raw.github.com/jmjeong/alfred-extension/master/managealfredextension/ManageAlfredExtension.alfredworkflow))

Search and manage the installed extension

![Demo screenshot](https://raw.github.com/jmjeong/alfred-extension/master/managealfredextension/screenshot.png)

###  Usage

```
 alf                :: display the installed extensions
 alf <search>       :: search extension by title, author name, and keyword

 enter              :: Browse the installed folder in Alfred
 ctrl               :: Reveal the installed folder in Finder
 shift              :: Execute extension with the first keyword
 cmd                :: Open terminal in the installed folder
 shift              :: Export the extension for distribusion (need export.json file)
```

### export.json 

The file format is as follows:

```json
{
    "workflow-export" :
	    {"directory" : "~/git/alfred-extension/managealfredextension",
		 "enable": true},
    "source-export":
		{"directory" : "~/git/alfred-extension/managealfredextension",
		 "enable": false}
}
```

*'workflow-export'* specifies the directory where <extension>.alfredworkflow is exported.
*'source-export'* specifies the directory where extension source is copied.  

To publish and share the extension, this feature can be used. To export the selected extension, *'export.json'* file is created in that directory.


### Version History 

#### 2.0 - March 29, 2013

- Export feature
- Open terminal 
- Support Alleyoop's auto update plugin
- Display 'disabled' extension

#### 1.x - March 28, 2013

- Initial version

 

