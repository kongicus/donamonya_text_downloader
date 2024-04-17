# 文本内容来源
通过下载移动版 [Radio★kids](http://radioxxxkids.blog.fc2.com/) 的文章内容获取donamonya的文本
# 使用方式
## 下载指定日期区间内的文本到指定路径
```python
# 下载指定日期区间内的文本
main.py --start_date 20240101 --end_date 20240201 --path doya_text_download
```
## 如果不填写参数，使用默认值
```python
# main.py
```
1) 如果 `--start_date` 不填写参数，会默认从最早发布的一篇内容开始下载，自动下载至`--end_date` 。
2) 如果 `--end_date` 不填写参数，会自动下载至最新的内容。
3) 如果 `--path` 不存在，会默认路径为 `doya_text_download` 。
4) 如果所有参数都默认，会自动检测默认路径 `doya_text_download` 中最新下载的一篇，并下载这一篇之后 `Radio★kids` 的更新。
5) 一般来说，使所有参数为默认值，在workflow里每周定时运行一次，以保持文本备份更新到了最新状态。