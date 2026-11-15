# Kainuwa Store Admin

## One time setup
1. Add every file from this zip to the repo 245stdstr (keep the same paths).
2. Repo Settings > Pages > Source: Deploy from a branch > main > / (root) > Save.
3. Your page will be at https://iam4all26.github.io/245stdstr/admin/
4. Create a token: GitHub > Settings > Developer settings > Fine-grained tokens > only repo 245stdstr > Repository permissions > Contents: Read and write.
   Paste it into the page once. It stays only in your browser. Never share it with anyone.

## Daily use
- Upload tab: choose type, type a category, select many files, edit name/tags/description/premium for each, Publish.
- Manage tab: search, rename, change category (moves the file), tags, premium, description, or delete, then Save changes.
- Everything goes in one commit and catalog.json is updated by the page itself.

## Backup method (no token)
Upload a zip with folders such as fonts/Display/MyFont.ttf into the incoming folder on GitHub.
