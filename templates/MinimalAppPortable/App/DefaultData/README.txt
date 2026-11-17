DefaultData holds the files that belong in the package's Data folder on
first run. The launcher copies this content into Data when Data is empty
or missing.

Mirror the structure Data should have. For example, if the app's
settings folder is redirected from Data\AppNameConfig, place the default
settings under DefaultData\AppNameConfig\.

This placeholder file itself is harmless: it will be copied into Data on
first run. Delete it in a real package if you ship actual defaults, or
leave the folder out entirely if the app creates its own defaults.
