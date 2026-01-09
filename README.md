# 🐦 Twitter Bookmarks Organizer

> An intelligent tool to scrape, categorize, and organize your Twitter/X bookmarks using AI-powered classification.

## 📋 Overview

This tool helps you manage thousands of Twitter bookmarks by:
- **Scraping** all your bookmarks without needing Twitter API access
- **Categorizing** them automatically using ML-based zero-shot classification
- **Organizing** them into beautiful, searchable README files by topic

Perfect for researchers, developers, and anyone who bookmarks tons of tweets but struggles to find them later!

## ✨ Features

- 🔐 **No API Key Required** - Uses browser cookies for authentication
- 🤖 **AI-Powered Categorization** - Zero-shot classification with transformers
- 📊 **Multiple Categories** - Automatically sorts into your custom topics
- 📖 **Beautiful Output** - Generates Awesome-style README tables
- 🔄 **Incremental Updates** - Re-run anytime to refresh your organized bookmarks
- ⚡ **Rate Limit Handling** - Respects Twitter's limits automatically

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Twitter/X account with bookmarks
- Firefox or Chrome browser (for exporting cookies)

### Installation

1. **Clone or download this repository**

2. **Install dependencies:**
   ```bash
   pip install twikit pandas transformers torch tqdm
   ```

3. **Export your cookies:**
   
   Install a cookie export extension:
   - **Firefox**: [Cookie Quick Manager](https://addons.mozilla.org/en-US/firefox/addon/cookie-quick-manager/)
   - **Chrome**: [Cookie Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)
   
   Steps:
   1. Log into [Twitter/X](https://x.com) in your browser
   2. Open the cookie export extension
   3. Export cookies for `x.com` or `twitter.com`
   4. Save as `cookies.json` in this project folder

4. **Run the organizer:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
.
├── main.py                    # Main script - scrapes, categorizes, generates
├── generate_readmes.py        # Creates organized README files
├── cookies.json              # Your Twitter session cookies (you provide)
├── config.ini                # Optional: Twitter credentials (legacy)
│
├── total_bookmarks.csv       # Raw scraped bookmarks
├── bmk_organised.csv         # Categorized bookmarks
│
└── README_Categories/        # Generated organized READMEs
    ├── README.md            # Main index
    ├── robotics.md          # Category-specific README
    ├── ml_and_deep_learning.md
    └── ...
```

## 🔧 Configuration

### Custom Categories

Edit the `CATEGORIES` list in [main.py](main.py) to match your interests:

```python
CATEGORIES = [
    "Robotics",
    "HPC, GPU Programming and ML Optimisations",
    "ML and Deep Learning",
    "Personal Growth and Research Career",
    "Electronics",
    "Books and Study Materials"
]
```

### cookies.json Format

The cookies should be exported as JSON from your browser extension. Example structure:

```json
[
  {
    "name": "auth_token",
    "value": "your_auth_token_here",
    "domain": ".x.com"
  },
  {
    "name": "ct0",
    "value": "your_ct0_token_here",
    "domain": ".x.com"
  }
]
```

**Important:** The `cookies.json` file contains sensitive authentication data. Keep it private!

### config.ini (Optional - Legacy)

If you want to use username/password login instead of cookies:

```ini
[X]
username = your_username
email = your_email@example.com
password = your_password
```

**Note:** Cookie-based auth is recommended as it's more reliable and doesn't require storing passwords.

## 🎯 Usage

### Full Pipeline

Run everything at once:

```bash
python main.py
```

This will:
1. ✅ Test your Twitter connection
2. 📥 Scrape all your bookmarks
3. 🤖 Categorize them with AI
4. 📖 Generate organized README files

### Step-by-Step (Advanced)

You can also run individual steps:

```python
# Test connection only
import asyncio
from main import test_connection
asyncio.run(test_connection())

# Just scrape bookmarks
from main import scrape_all_bookmarks
asyncio.run(scrape_all_bookmarks())

# Just categorize existing data
from main import categorize_bookmarks
categorize_bookmarks()

# Just generate READMEs
from main import generate_readmes
generate_readmes()
```

<!-- ### Using the Notebook

For interactive exploration, use [scrapper.ipynb](scrapper.ipynb):
- Run cells individually
- Test different categories
- Experiment with the ML model -->

## 📊 Output Format

Each category README contains a table:

| # | Summary | Link | Date |
|---|---------|------|------|
| 1 | Interesting robotics paper about... | [Link](https://x.com/...) by [@username](https://x.com/username) | January 04, 2026 |
| 2 | GPU optimization technique for... | [Link](https://x.com/...) by [@expert](https://x.com/expert) | January 03, 2026 |

Features:
- ✅ Latest bookmarks appear first
- ✅ Clean summaries (150 chars max)
- ✅ Direct links to tweets and authors
- ✅ Human-readable dates

## 🛠️ Troubleshooting

### "cookies.json not found"
- Export your cookies from the browser extension
- Save as `cookies.json` in the project root
- Make sure you're logged into Twitter/X before exporting

### "Session invalid or forbidden"
- Your cookies may have expired
- Log into Twitter/X again
- Scroll through your feed a bit
- Re-export fresh cookies

### "Rate limit hit"
- Twitter limits how fast you can fetch data
- Wait 15 minutes and try again
- Your progress is automatically saved!

### Unicode/Encoding Errors
- The script handles UTF-8 automatically
- If issues persist, check your terminal encoding
- On Windows: `chcp 65001` before running

### ML Model Issues
- First run downloads ~280MB model
- Requires internet connection
- If download fails, try again with stable internet
- Model is cached after first download

## 🔒 Privacy & Security

- **cookies.json** contains your authentication - keep it private!
- Add to `.gitignore` if using version control
- Never share or commit this file
- Cookies expire - you'll need to refresh them periodically

## 🤝 Contributing

Want to improve this tool? Ideas:
- Add more ML models for better categorization
- Support for other social platforms
- Web UI for browsing bookmarks
- Export to other formats (Notion, Obsidian, etc.)

## 📝 License

MIT License - feel free to use and modify!

## 🙏 Acknowledgments

- [twikit](https://github.com/d60/twikit) - Twitter API client
- [transformers](https://huggingface.co/transformers/) - ML models
- Inspired by all the Awesome lists on GitHub

---

**Made with ❤️ for bookmark hoarders everywhere**

Need help? Found a bug? Open an issue!
