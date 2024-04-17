# Source of Text Content
Obtain the text from donamonya by downloading the articles from the mobile version of [Radio★kids](http://radioxxxkids.blog.fc2.com/).

# Usage
## Download Text within Specified Date Range to Specified Path
```python
# Download text within specified date range
main.py --start_date 20240101 --end_date 20240201 --path doya_text_download
```
## Using Default Values if Parameters Not Provided
```python
# main.py
```
1) If `--start_date` parameter is not provided, it will default to downloading from the earliest published content, automatically downloading until `--end_date`.
2) If `--end_date` parameter is not provided, it will automatically download until the latest content.
3) If `--path` does not exist, the default path will be `doya_text_download`.
4) If all parameters are default, it will automatically detect the latest downloaded article in the default path `doya_text_download` and download updates from Radio★kids after that.
5) Generally, setting all parameters to default values and scheduling the workflow to run once a week will ensure that the text backup stays up-to-date with the latest updates.