Changelog
=========

1.3.2
-----
* [ENHANCEMENT] Include filename exclusion patterns in profiles
* [FIX] Minor UI bugfixes and code cleanup

1.3.1
-----
* [FIX] Add "one per line" notation to filename exclusion patterns label

1.3.0
-----
* [NEW] Remember file/directory/batch mode settings for next startup (issue #5)
* [NEW] Ability to set input path via clipboard paste or drag-and-drop (issues #6)
* [NEW] Increase maximum piece size to 64MB (issue #7)
* [NEW] Add support for filename exclusion pattern in dottorrent 1.8.0 (issue #9)

1.2.2
-----
* [FIX] window resizing behavior

1.2.1
-----
* [CHANGE] Update file menu item text 
* [FIX] error when importing source string from tracker configuration file
* [FIX] Tweak default window sizing

1.2.0
-----
* Add optinal source string field
* Add "Auto" piece size option
* Save most recently used input and output directories
* Fix crash when encountering empty subdirectories in batch mode
* Improve error handling during torrent creation
* Add F1 shortcut for About window
* Minor bugfixes


1.1.3
-----
* Fix output torrent filename generation in directory mode

1.1.2
-----
* Bump dottorrent dependency to 1.5.3

1.1.1
-----
* Use humanfriendly.format_size() in binary mode
* Update dependencies

1.1.0
-----
* Restore last used values for trackers/web seeds and private flag
* Minor tweaks

1.0.0
-----
* Initial release
