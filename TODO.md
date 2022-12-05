# TODO
* TODO Instead of having a single session log. Maybe have a global .parquet log file that is expanded after each run.
* TODO _deal_with_special_words_and_bands should create brackets, so it should make "Artist - Title Live" to "Artist - Title (Live)". Same for "Remix" and "Feat.". This will be a bit complicated for cases like "Live in London", "Remix by" and of course "Feat.".
* TODO Rename (Original Motion Picture Soundtrack) into (Score).
* Add logs maybe one logfile for old filename, one for new one. Same for folders. Than one could easily checks the diffs.
* Add a pydantic class for the folder that has a list (with at least one entry of tagsexported class). That would also detect errors.
