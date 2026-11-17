The Data folder holds ALL user data and settings for the portable app.

In a distributed package this folder ships empty: the launcher fills it
from App\DefaultData on first run, and the app recreates it if it is
deleted. Never ship a developer's populated Data folder.

This README is only a placeholder so the folder exists in the template;
you may delete it in a real package.
