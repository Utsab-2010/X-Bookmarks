#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Twitter Bookmarks Organizer
============================
A tool to scrape, categorize, and organize your Twitter bookmarks using AI.

This script:
1. Scrapes all your Twitter bookmarks using cookies (no API needed)
2. Categorizes them using zero-shot classification
3. Generates organized README files for each category
"""

import asyncio
import json
import csv
import os
import sys
import subprocess
from twikit import Client, TooManyRequests
import pandas as pd
from transformers import pipeline
import torch
from tqdm import tqdm


# Configuration
COOKIES_FILE = 'cookies.json'
BOOKMARKS_CSV = 'total_bookmarks.csv'
ORGANIZED_CSV = 'bmk_organised.csv'
ML_MODEL = "cross-encoder/nli-deberta-v3-small"

# Your research/interest categories - customize these!
CATEGORIES = [
    "Robotics",
    "HPC, GPU Programming and ML Optimisations",
    "ML and Deep Learning",
    "Personal Growth and Research Career",
    "Electronics",
    "Books and Study Materials"
]


async def test_connection():
    """
    Test if the Twitter session is valid using the cookies
    """
    print("\n" + "="*60)
    print("🔍 STEP 1: Testing Twitter Connection")
    print("="*60)
    
    client = Client(language='en-US')
    
    if not os.path.exists(COOKIES_FILE):
        print(f"❌ '{COOKIES_FILE}' not found.")
        print("\nPlease export your cookies using a browser extension.")
        return False

    try:
        with open(COOKIES_FILE, 'r') as f:
            raw_cookies = json.load(f)
        
        cleaned_cookies = {c['name']: c['value'] for c in raw_cookies}
        client.set_cookies(cleaned_cookies)
        print("✅ Cookies loaded successfully.")
    except Exception as e:
        print(f"❌ Cookie error: {e}")
        return False

    print("Verifying session with X.com...")
    try:
        bookmarks = await client.get_bookmarks()
        print("🎉 SUCCESS! Connection is active.")
        print(f"Found {len(bookmarks)} bookmarks on the first page.")
        
        if len(bookmarks) > 0:
            print(f"Latest bookmark: {bookmarks[0].text[:50]}...")
        return True
            
    except Exception as e:
        print(f"❌ Session invalid or forbidden.")
        print(f"Error: {e}")
        print("\n💡 Fix: Log into X on your browser, scroll a bit, then re-export cookies.json")
        return False


async def scrape_all_bookmarks():
    """
    Scrape all bookmarks from Twitter and save to CSV
    """
    print("\n" + "="*60)
    print("📥 STEP 2: Scraping All Bookmarks")
    print("="*60)
    
    client = Client(language='en-US')
    
    # Load cookies
    try:
        with open(COOKIES_FILE, 'r') as f:
            raw_cookies = json.load(f)
        cleaned_cookies = {c['name']: c['value'] for c in raw_cookies}
        client.set_cookies(cleaned_cookies)
        print("✅ Session initialized.")
    except Exception as e:
        print(f"❌ Cookie error: {e}")
        return False

    # Clear existing file for fresh scrape
    file_exists = os.path.isfile(BOOKMARKS_CSV)
    if file_exists:
        print(f"⚠️  Found existing {BOOKMARKS_CSV}. Backing up...")
        os.rename(BOOKMARKS_CSV, BOOKMARKS_CSV + '.backup')
        file_exists = False
    
    print("🚀 Starting collection (this might take a while)...")
    
    total_saved = 0
    try:
        bookmarks = await client.get_bookmarks()
        
        while bookmarks:
            batch = []
            for tweet in bookmarks:
                batch.append({
                    'Tweet_id': tweet.id,
                    'Username': tweet.user.screen_name,
                    'Text': tweet.text,
                    'Created_At': tweet.created_at,
                    'URL': f"https://x.com/i/status/{tweet.id}"
                })
            
            # Save batch to CSV
            if batch:
                keys = batch[0].keys()
                with open(BOOKMARKS_CSV, 'a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=keys)
                    if not file_exists:
                        writer.writeheader()
                        file_exists = True
                    writer.writerows(batch)
                
                total_saved += len(batch)
                print(f"📦 Collected {total_saved} bookmarks...")

            # Get next page
            try:
                await asyncio.sleep(3)  # Rate limiting
                bookmarks = await bookmarks.next()
            except Exception:
                print("🏁 No more bookmarks found.")
                break

    except TooManyRequests:
        print("\n⚠️  Rate limit hit! Twitter is asking us to slow down.")
        print("Try again in 15 minutes. Your data is saved.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

    print(f"\n✅ Scraping complete! {total_saved} bookmarks saved to {BOOKMARKS_CSV}")
    return True


def categorize_bookmarks():
    """
    Use ML to categorize bookmarks by topic
    """
    print("\n" + "="*60)
    print("🤖 STEP 3: Categorizing Bookmarks with AI")
    print("="*60)
    
    if not os.path.exists(BOOKMARKS_CSV):
        print(f"❌ {BOOKMARKS_CSV} not found. Run scraping first.")
        return False
    
    # Load data
    print(f"Loading bookmarks from {BOOKMARKS_CSV}...")
    df = pd.read_csv(BOOKMARKS_CSV, encoding='utf-8')
    print(f"✅ Loaded {len(df)} bookmarks")
    
    # Setup classifier
    print(f"\n🧠 Loading ML model: {ML_MODEL}")
    print("   (First run will download ~280MB model)")
    device = 0 if torch.cuda.is_available() else -1
    
    try:
        classifier = pipeline("zero-shot-classification", 
                            model=ML_MODEL, 
                            device=device)
        print("✅ Model loaded successfully")
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False
    
    # Categorization function
    def categorize(text):
        if not isinstance(text, str) or len(text) < 10:
            return "Misc"
        try:
            result = classifier(text, CATEGORIES, truncation=True)
            return result['labels'][0]
        except:
            return "Error"
    
    # Process with progress bar
    print(f"\n🏷️  Categorizing into {len(CATEGORIES)} topics...")
    tqdm.pandas()
    df['Category'] = df['Text'].progress_apply(categorize)
    
    # Save organized data
    df.to_csv(ORGANIZED_CSV, index=False, encoding='utf-8')
    print(f"\n✅ Categorization complete! Saved to {ORGANIZED_CSV}")
    
    # Show summary
    print("\n📊 Category Distribution:")
    print(df['Category'].value_counts().to_string())
    
    return True


def generate_readmes():
    """
    Generate organized README files for each category
    """
    print("\n" + "="*60)
    print("📖 STEP 4: Generating README Files")
    print("="*60)
    
    result = subprocess.run(
        [sys.executable, 'generate_readmes.py'],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    )
    
    print(result.stdout)
    if result.stderr:
        print("⚠️  Warnings:", result.stderr)
    
    return result.returncode == 0


async def main():
    """
    Main execution flow
    """
    print("\n" + "="*70)
    print("  🐦 TWITTER BOOKMARKS ORGANIZER")
    print("="*70)
    
    # Step 1: Test connection
    if not await test_connection():
        print("\n❌ Connection test failed. Please fix the issues above and try again.")
        return
    
    # Step 2: Scrape bookmarks
    if not await scrape_all_bookmarks():
        print("\n❌ Scraping failed. Check the errors above.")
        return
    
    # Step 3: Categorize
    if not categorize_bookmarks():
        print("\n❌ Categorization failed. Check the errors above.")
        return
    
    # Step 4: Generate READMEs
    if not generate_readmes():
        print("\n⚠️  README generation had issues, but your data is still organized.")
    
    print("\n" + "="*70)
    print("  ✅ ALL DONE! Your bookmarks are organized.")
    print("="*70)
    print(f"\n📁 Output files:")
    print(f"   • {BOOKMARKS_CSV} - Raw scraped bookmarks")
    print(f"   • {ORGANIZED_CSV} - Categorized bookmarks")
    print(f"   • README_Categories/ - Organized markdown files")
    print("\n💡 Tip: Run this script periodically to keep your bookmarks updated!")


if __name__ == "__main__":
    asyncio.run(main())