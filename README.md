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

**条件**  
包含不限于：
- 使用者具有对应pt站
- 主机具有Python环境

## 使用
1. 安装依赖，参照`setup_env.sh`;
2. 你可能需要提前设好代理的环境变量;
3. 修改`_variables_站点.yaml`中的`cookie`、`passkey`、`download_path`等信息;
4. 修改`站点_config.yaml`中的`urls`列表以及灵活修改你自己的条件;
5. 下载种子：
    ```bash
    flexget -c opencd_config.yaml execute
    ```
6. 下载完免费种子后，移入到qBittorrent的watch目录
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
