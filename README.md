# MOBIDownloader

用于从 [魔笔小说](https://mobinovels.com/) 下载轻小说的脚本

## 设置

`main.py` 中第八行和第九行为下载设置

```
PASSCODE = 6195
FORMAT = "MOBI" # MOBI/EPUB
```

其中 `PASSCODE` 为ctfile密码，默认为6195(网站公告有标)

`FORMAT` 为下载格式，在MOBI和EPUB里面二选一，我要塞到Kindle里面所以选了MOBI

## 使用方法

下载一个系列

```
python3 main.py "https://mobinovels.com/mushoku-tensei/"
```

下载多个系列

将多个链接丢进 `lists.txt`, 一行一个,比如

```
https://mobinovels.com/mushoku-tensei/
https://mobinovels.com/classroom-of-the-elite/
https://mobinovels.com/gj-club/
https://mobinovels.com/aria-the-scarlet-ammo/
```

然后执行

```
python3 main.py
```

## Links

[Matrix Group](https://matrix.to/#/#kagari306-official:matrix.org)