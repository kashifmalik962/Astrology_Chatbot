import sqlite3
import os
import shutil
from datetime import datetime, timedelta, timezone
import platform

def get_recent_browser_history():
    minutes=15
    platform_os = platform.system().lower()
    browser_paths = {
        "chrome": {
            "linux": "~/.config/google-chrome/Default/History",
            "windows": os.path.expandvars(r"%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\History"),
            "darwin": "~/Library/Application Support/Google/Chrome/Default/History",
        },
        "brave": {
            "linux": "~/.config/BraveSoftware/Brave-Browser/Default/History",
            "windows": os.path.expandvars(r"%LOCALAPPDATA%\\BraveSoftware\\Brave-Browser\\User Data\\Default\\History"),
            "darwin": "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/History",
        },
        "edge": {
            "linux": "~/.config/microsoft-edge/Default/History",
            "windows": os.path.expandvars(r"%LOCALAPPDATA%\\Microsoft\\Edge\\User Data\\Default\\History"),
            "darwin": "~/Library/Application Support/Microsoft Edge/Default/History",
        },
        "firefox": {
            "linux": "~/.mozilla/firefox",
            "windows": os.path.expandvars(r"%APPDATA%\\Mozilla\\Firefox\\Profiles"),
            "darwin": "~/Library/Application Support/Firefox/Profiles",
        },
    }
    for browser in browser_paths.keys():
        if browser not in browser_paths:
            print(f"Unsupported browser: {browser}")
        if platform_os not in browser_paths[browser]:
            print(f"Unsupported platform: {platform_os}")
        try:
            if browser == "firefox":
                firefox_profile_dir = os.path.expanduser(browser_paths["firefox"][platform_os])
                profile_dirs = [d for d in os.listdir(firefox_profile_dir) if os.path.isdir(os.path.join(firefox_profile_dir, d))]
                history_db = None
                for profile in profile_dirs:
                    profile_path = os.path.join(firefox_profile_dir, profile, "places.sqlite")
                    if os.path.exists(profile_path):
                        history_db = profile_path
                        break
                if not history_db:
                    print("No valid Firefox profile with places.sqlite found.")
            else:
                history_db = os.path.expanduser(browser_paths[browser][platform_os])
            if not os.path.exists(history_db):
                print(f"History database not found at: {history_db}")
            copy_db = "temp_history"
            shutil.copy2(history_db, copy_db)
            connection = sqlite3.connect(copy_db)
            cursor = connection.cursor()
            try:
                now = datetime.now(timezone.utc)
                start_time = now - timedelta(minutes=minutes)
                
                if browser == "firefox":
                    start_timestamp = int(start_time.timestamp() * 1000000)  
                    end_timestamp = int(now.timestamp() * 1000000)
                    query = """
                    SELECT moz_places.url, moz_places.title, moz_places.last_visit_date 
                    FROM moz_places 
                    WHERE last_visit_date BETWEEN ? AND ?
                    ORDER BY last_visit_date DESC
                    """
                else:
                    start_timestamp = int((start_time - datetime(1601, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1e6)
                    end_timestamp = int((now - datetime(1601, 1, 1, tzinfo=timezone.utc)).total_seconds() * 1e6)
                    query = """
                    SELECT urls.url, urls.title, urls.last_visit_time 
                    FROM urls 
                    WHERE last_visit_time BETWEEN ? AND ?
                    ORDER BY last_visit_time DESC
                    """
                cursor.execute(query, (start_timestamp, end_timestamp))
                print(f"Recent URLs from the last {minutes} minutes:")
                for row in cursor.fetchall():
                    
                    if browser == "firefox":
                        url, title, visit_date = row
                        visit_time = datetime.fromtimestamp(visit_date / 1e6, tz=timezone.utc)
                    else:
                        url, title, last_visit_time = row
                        visit_time = datetime(1601, 1, 1, tzinfo=timezone.utc) + timedelta(microseconds=last_visit_time)
                    visit_time = visit_time.astimezone()
                    print(f"Visited URL: {url}\nTitle: {title}\nLast Visit: {visit_time}\nBrowser: {browser}")
                connection.close()
                os.remove(copy_db)
            except:
                    print(f"No URL Found")
        except Exception as e:
            print(f"Error: {e}")

get_recent_browser_history()