# Quick Start Guide

## First Time Setup (5 minutes)

### 1. Install Dependencies
```bash
pip install twikit pandas transformers torch tqdm
```

### 2. Export Your Twitter Cookies

**For Firefox:**
1. Install [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)
2. Go to [x.com](https://x.com) and log in
3. Click the Cookie Quick Manager icon
4. Click "Export" 
5. Select "Export as JSON"
6. Save as `cookies.json` in this folder

**For Chrome:**
1. Install [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
2. Go to [x.com](https://x.com) and log in
3. Click the Cookie Editor icon
4. Click "Export" → "JSON"
5. Save as `cookies.json` in this folder

### 3. Run the Script
```bash
python main.py
```

That's it! The script will:
- ✅ Test your connection
- 📥 Download all bookmarks
- 🤖 Categorize them with AI
- 📖 Create organized README files

## Output Files

After running, you'll have:

```
README_Categories/
├── README.md              ← Start here! Main index
├── robotics.md           ← Each category gets its own file
├── ml_and_deep_learning.md
└── ...

total_bookmarks.csv        ← All your bookmarks (raw)
bmk_organised.csv          ← Categorized version
```

## Customization

### Change Categories

Edit `CATEGORIES` in [main.py](main.py):

```python
CATEGORIES = [
    "Your Topic 1",
    "Your Topic 2",
    "Another Interest",
]
```

Then run `python main.py` again.

### Re-run Anytime

The script is **idempotent** - run it whenever you want to:
- Add new bookmarks
- Update existing organization
- Refresh categories

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "cookies.json not found" | Export cookies from browser (see step 2 above) |
| "Session invalid" | Cookies expired - export fresh ones |
| "Rate limit hit" | Wait 15 minutes, then run again |
| "Module not found" | Run `pip install twikit pandas transformers torch tqdm` |

## Tips

💡 **Bookmark a lot?** Run this weekly to stay organized

💡 **Want different categories?** Customize the `CATEGORIES` list

💡 **Share your organized bookmarks?** The README_Categories folder is perfect for GitHub repos

💡 **Privacy:** Don't commit `cookies.json` or `config.ini` - they're in .gitignore

## Advanced Usage

### Run Individual Steps

```python
import asyncio
from main import test_connection, scrape_all_bookmarks, categorize_bookmarks

# Test only
asyncio.run(test_connection())

# Scrape only
asyncio.run(scrape_all_bookmarks())

# Categorize existing data
categorize_bookmarks()
```

### Use the Jupyter Notebook

For interactive exploration:
```bash
jupyter notebook scrapper.ipynb
```

## Need Help?

- Check the main [README.md](README.md) for detailed docs
- Review error messages - they usually explain what's needed
- Make sure you're logged into Twitter before exporting cookies
- Ensure cookies.json is in the project root directory

---

Happy organizing! 🎉
