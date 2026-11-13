# Kainuwa Studio Store

Items that Kainuwa Studio can download. Keep this repository public.

Folders: fonts/ (ttf or otf), backgrounds/ (jpg or png), previews/ (small jpg or png, about 400 px wide).

catalog.json lists every item. Example with one font and one background:

{
  "version": 1,
  "items": [
    { "id": "font-poppins-bold", "type": "font", "name": "Poppins Bold",
      "file": "fonts/Poppins-Bold.ttf", "preview": "previews/poppins-bold.png", "sizeKb": 150 },
    { "id": "bg-gold-wave", "type": "background", "name": "Gold Wave",
      "file": "backgrounds/gold-wave.jpg", "preview": "previews/gold-wave.jpg", "sizeKb": 400 }
  ]
}

Rules: each id must be unique and never change after you publish it. Paths are relative to this repository root.
The app reads https://raw.githubusercontent.com/Iam4all26/245stdstr/main/catalog.json
