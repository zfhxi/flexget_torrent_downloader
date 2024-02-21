#!/bin/bash

# 参考：https://forevertime.site/flexget-auto-retrive-free-seed/
conda create -n flexget python=3.10
conda activate flexget
pip install flexget chardet deluge-client python-telegram-bot==12.8 baidu-aip pillow pandas matplotlib fuzzywuzzy python-Levenshtein
flexget check