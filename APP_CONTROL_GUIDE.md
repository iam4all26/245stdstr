# Kainuwa Studio remote control

Upload `app_control.json` to the ROOT of the store repository (Iam4all26/245stdstr, branch main) with K-Git Studio. Every installed app reads it from
https://raw.githubusercontent.com/Iam4all26/245stdstr/main/app_control.json
(GitHub may take a few minutes to serve a new version). The app checks 5 seconds after it opens, when it returns to the front after an hour, and from Settings > Check for updates. Offline phones use the last copy they saved.

Versions use the pubspec version name, for example 1.2.0. The build number after the plus sign is ignored. Before every release change `version:` in pubspec.yaml (for example 1.1.0+2).

## Fields
- latest_version: newest release. Phones with an older version see "Update available" with Later and Update (asks again the next day).
- min_version: oldest version allowed. Phones older than this see "Update required" that cannot be closed until they install a newer version.
- update_url: where Update opens (a download link or release page). Leave a real link here before using min_version.
- update_notes: optional text shown in both update dialogs.
- maintenance.on: true shows a blocking "Back soon" message with Try again to everyone. Set back to false to open the app again.
- messages: a list of notices. Each one needs a unique id.
  - enabled: false hides it. start and end (YYYY-MM-DD) set when it shows; end includes that whole day.
  - min_version and max_version: show only to those versions (empty = everyone).
  - once: true shows it one time per phone (change the id to show a new one). false shows it at every check.
  - dismissible: false makes a notice that must be answered with its link.
  - link and link_label: optional button that opens a web page.

## Examples
Force everyone below 1.2.0 to update: set "min_version": "1.2.0", "latest_version": "1.2.0".
Announce a feature to everyone: add a message with a new id.
Tell only old versions: add "max_version": "1.1.9".
