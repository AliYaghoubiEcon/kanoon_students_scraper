# Kanoon Students Scraper

This project scrapes student data from [Kanoon website](https://www.kanoon.ir) using **Selenium** and saves it into structured Excel files.

---

## ✨ Features

- Scrapes students' information for all cities
- Handles multiple tabs per city
- Extracts:
  - Name (`نام`)
  - School (`مدرسه`)
  - Major (`رشته`)
  - Description (`توضیحات`)
  - City (`شهر`)
  - Tab (`دسته‌بندی`)
- Saves one Excel per city
- Optionally, merge all Excel files later

---

## 📂 Project Structure

---


data/ # Input files (if any)
results/
├── per_city/ # Excel per city
├── merged_all.xlsx # All data merged
scrape_students.py # Main script
README.md
requirements.txt




---


---

## 🚀 Usage

1. Install dependencies:

```bash
pip install -r requirements.txt

```
2. Run the scraper
```bash
python scrape_students.py

