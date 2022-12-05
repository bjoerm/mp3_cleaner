[![Build, Lint and Pytest](https://github.com/bjoerm/mp3_cleaner/actions/workflows/build_lint_test.yml/badge.svg)](https://github.com/bjoerm/mp3_cleaner/actions/workflows/build_test_lint.yml)

# MP3 Cleaner
Beautifies ID3 tags, filenames and foldernames of MP3 audio files.

Main features:
* Removes unwanted ID3 tags like the comment tag.
* Cleans and beautifies ID3 tags for artist, track and album name. Same for track and disc numbers and the record year.
* Beautifies the file names and folders.
* Removes unwanted filetypes from album.

Details:
* Unifying capitalization that also deals with special cases.
* Moves any featuring information from artist to end of track name.
* Checks "fallback" fields, if main field does not have sufficient
* Special handling of foldernames for scores and soundtracks (if their album tag ends with (Score) or (Soundtrack)).
* Sorts suffixes like "(Feat. ...)" and (Live) uniformly.



## How-to
1. Open the [config.toml](/src/config.toml) and adjust input and output paths.
1. Run the [mp3_cleaner](/src/mp3_cleaner.py).

A test MP3 file can be found under [data](/data/wikimedia_commons/warnsignal_train_with_some_tags.mp3). It is from [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:BVG_Warnsignal_U-Bahn.mp3).
