# flexget_torrent_downloader

## 说明
基于[madwind/flexget_qbittorrent_mod](https://github.com/madwind/flexget_qbittorrent_mod)删改后的免费种下载器。  
**只有下载免费种子到本地的功能！**，可根据自己需求修改！

### 适用场景
可能受以下条件限制，需要下载免费种子到本地：
- 不会刷流
- vt不支持某些站点刷流
- 想拉取某个站点的免费种子到本地
- 想批量下载官种

**目前适配站点及种子下载条件**:  

- agsvpt(待修复，目前站免未做充分测试，接受所有没有截止日期的免费种)
    - 种子状态非做种期（没被下载过）
    - 种子具有`Free`标记
    <!-- - 种子免费剩余时间大于某个阈值（6 hours） -->
- hhclub
    - 种子状态非做种期（没被下载过）
    - 种子具有`免费`标记
    - 种子免费剩余时间大于某个阈值（6 hours）
- leavesred
    - 跳过付费种子
    - 种子状态非做种期（没被下载过）
    - 种子具有`免费`标记
    - 种子免费剩余时间大于某个阈值（5 hours）
- opencd
    - 种子状态非做种期（没被下载过）
    - 种子具有`Free`、`2xFree`标记
    - 种子免费剩余时间大于某个阈值（2 hours）
- pterclub
    - 种子状态非做种期（没被下载过）
    - 种子具有`Free`、`2xFree`标记
    - 种子免费剩余时间大于某个阈值（24 hours）
- ptvicomo
    - 种子状态非做种期（没被下载过）
    - 种子具有`免费`、`2X免费`标记
    - 种子免费剩余时间大于某个阈值（10 days）




**条件**  
包含不限于：
- 使用者具有对应pt站
- 主机具有Python环境

## 使用
1. 安装依赖，参照`setup_env.sh`;
2. 你可能需要提前设好代理的环境变量;
3. 新建`_variables_站点.yaml`并修改其中的`cookie`（建议开发者控制台里获取）、`passkey`等信息;
4. 新建`_template_global.yaml`并修改其中的`qBittorrent`下载器等信息;
5. 修改`站点_config.yaml`中的`urls`列表、`url_interval`（URL列表请求间隔）、`limited_new`（种子最大新增数量），以及灵活修改你自己的条件;
6. 下载种子：
    ```bash
    flexget -c config_agsvpt.yaml execute 
    # 或者执行配置文件中的选定任务
    flexget -c config_agsvpt.yaml execute --task agsvpt-official-free
    ```
7. ~~下载完免费种子后，移入到qBittorrent的watch目录；~~
8. 目前种子会被自动推送到qBittorrent里，需要手动取消暂停(可修改`_template_global.yaml`中的`add_paused`参数来关闭暂停)。手动取消暂停的好处是，可以在qBittorrent里将种子按大小排序，删除不必要的种子，防止拉取的官种过大。


## TODO

- [ ] 修复agsvpt非站免时的deadline提取
- [ ] 适配更多站点
- [ ] 排除H&R种子
- [ ] 应对站免时dom结构、css的变化

## 参考
包含不限于：
- https://github.com/madwind/flexget_qbittorrent_mod
- https://forevertime.site/flexget-auto-retrive-free-seed/
- https://github.com/allonli/flexget-nexusphp
- https://wiki.ukenn.top/seedbox-wiki-1/untitled-1
- https://flexget.com/Plugins/if
