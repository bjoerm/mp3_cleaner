# TODO
* _deal_with_special_words_and_bands should create brackets, so it should make "Artist - Title Live" to "Artist - Title (Live)". Same for "Remix" and "Feat.". This will be a bit complicated for cases like "Live in London", "Remix by" and of course "Feat.".
* Add a pydantic class for the folder that has a list (with at least one entry of tagsexported class). That would also detect errors.
* What happens in the ID3 class if the file has both an id3v1 and id3v2 tag? Is the id3v2 tag always chosen?
* Add unittests with artificial ID3 classes, so that the FileTags class can be tested further.
* Add proper logging. Also replace old print statements...
* Deal with case where only capitation changed in the filename. E.g. file.mp3 which should be File.mp3. That case currently doesn't change.