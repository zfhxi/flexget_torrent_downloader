#!/bin/bash

# 你可能需要提前设好代理的环境变量
flexget -c config_opencd.yaml execute

# 下载完免费种子后，移入到qBittorrent的watch目录
# sudo mv downloads/opencd/* /qb/watch