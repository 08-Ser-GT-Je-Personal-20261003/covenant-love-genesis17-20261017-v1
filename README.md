# 主与我们建立爱的关系

创世记17章 · 海德堡要理问答主日27 · 欧陆改革宗讲章与研读网站

日期：2026-10-17｜版本：v1.0.0

## 三个入口

- GitHub Pages：https://08-ser-gt-je-personal-20261003.github.io/covenant-love-genesis17-20261017-v1/
- Surge：https://covenant-love-genesis17-20261017-v1.surge.sh
- 源代码仓库：https://github.com/08-Ser-GT-Je-Personal-20261003/covenant-love-genesis17-20261017-v1

## 内容

15个学习章节，四段完整讲章，12组附答案分析的讨论题，救赎历史与圣约神学闭环，历史与地图、对照表、思维导图、复习卡及三份古代信经干净阅读版。支持可隐藏目录、目录筛选、讲章专注模式、配色切换、系统语音、打印和逐段背诵。手机无需下载外部字体和界面框架。

四字提纲：**源、血、家、信**——出于神，由宝血印证，包括我们的儿女，呼召我们凭信心回应。

## 继续开发

构建结果已提交在 `dist/`，GitHub Pages 直接发布静态成品。

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 4173 --directory dist
```

`content.html` 为原创正文；`data.json` 为讨论题和记忆卡；`style.css` 与 `app.js` 为界面与交互；`scripts/build.py` 生成入口和三份信经阅读页。`sources/used-texts.json` 保存构建使用的指定来源快照，离线构建不需要重新下载。原文核对摘要在 `sources/verification.json`。

如需重新抓取指定来源：`python scripts/fetch-creeds.py`，再构建并运行检查。来源更新应人工审阅后提交，不自动接受远端文字变化。

## 发布与运维

推送 `main` 后 `.github/workflows/pages.yml` 发布 `dist/` 到 GitHub Pages。Surge 手动执行 `surge ./dist covenant-love-genesis17-20261017-v1.surge.sh`，使用本机登录状态。没有在源码、公开文件或 README 中保存任何账号密码或发布令牌。

Surge 持续部署已配置：仓库 Actions Secrets 中保存 `SURGE_LOGIN`、`SURGE_TOKEN`；`surge.yml` 在推送后发布，凭证不出现在源码中。需要轮换时，在 GitHub Secrets 更新即可。

## 来源与解释边界

三份信经中文正文及联合信条引文均提取自 https://ccifellowship.org ，没有改用其他中文译本。正文保留标点与字词，去掉脚注上标并调整布局。指定来源中文译文与古代原稿语言并非同一概念。引用来源及适用范围在网页中列明。

讲章为本项目独立撰写。采用三项联合信条与古代三大信经框架，区分记号与实体、可见归属与实际得救。没有将洗礼视为自动重生，没有把全家受洗经文推断成明确列出婴孩。历史年代与地图的不确定性已标明。未声称已经阅读指定网站的所有内容；未核实的延伸网站仅作为学习入口。

诗歌保留用户给定编号；诗集版本不明的两首圣诗没有猜写曲名、歌词或音频。系统语音取决于浏览器和设备；不依赖外部音频服务。

## 验证

`scripts/check.py` 检查本地链接、章节、讨论题与三份信经逐段文字一致性。`scripts/verify-browser.mjs` 使用 Playwright 在360、390、768、1024、1440、1920像素屏宽检查页面溢出及主要交互（开发环境需要安装 Playwright）。表格允许容器内横向滚动，页面整体不应产生横向溢出。尊重系统减少动态效果偏好。

外部信经译文与资料的权利属于原来源；本项目不声称拥有其版权。地图与封面 SVG 为原创示意视觉。
