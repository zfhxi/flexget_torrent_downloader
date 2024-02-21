# flexget_torrent_downloader

## 说明
基于[madwind/flexget_qbittorrent_mod](https://github.com/madwind/flexget_qbittorrent_mod)删改后的免费种下载器。  
**只有下载免费种子到本地的功能！**

### 适用场景
可能受以下条件限制，需要下载免费种子到本地：
- 不会刷流
- vt不支持某些站点刷流
- 想拉取某个站点的免费种子到本地

**目前适配站点及种子下载条件**:
- opencd
    - 种子状态非做种期（没被下载过）
    - 种子具有`Free`、`2xFree`标记
    - 种子免费期与当前时间大于某个阈值（2 hours）

## 使用
1. 你可能需要提前设好代理的环境变量
```bash
flexget -c opencd_config.yaml execute
```
2. 下载完免费种子后，移入到qBittorrent的watch目录
```bash
sudo mv downloads/opencd/* /qb/watch
```

## 参考
包含不限于：
- https://github.com/madwind/flexget_qbittorrent_mod
- https://forevertime.site/flexget-auto-retrive-free-seed/
- https://github.com/allonli/flexget-nexusphp
- https://wiki.ukenn.top/seedbox-wiki-1/untitled-1
- https://flexget.com/Plugins/if
