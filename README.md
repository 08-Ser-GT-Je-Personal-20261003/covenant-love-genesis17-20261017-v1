# 主与我们建立爱的关系

创世记17章 · 海德堡要理问答主日27 · 欧陆改革宗讲章与研读网站

日期：2026-10-17｜版本：v2.0.0

## 三个入口

- GitHub Pages：https://08-ser-gt-je-personal-20261003.github.io/covenant-love-genesis17-20261017-v2-GTser/
- Surge：https://covenant-love-genesis17-20261017-v2-gtser.surge.sh
- 源代码仓库：https://github.com/08-Ser-GT-Je-Personal-20261003/covenant-love-genesis17-20261017-v2-GTser

## 内容

主页面保留12个紧扣创17与主日27的章节：四段完整讲章、真实历史背景、经文结构、救赎历史与圣约神学闭环、12组讨论及答案分析、应用和来源。独立 `study.html` 提供三份古代信经深度比较及背诵入口，三份原文另有干净阅读页面。删去泛化的网站目录、无关宗派介绍和重复历史说明。

加入四点经文锚点、不同主题色、地图视角切换、救赎历史五步探索、思维导图、复习卡；保留可隐藏目录、目录筛选、讲章模式、配色、系统朗读与打印。网页使用本地静态资源，适配手机、平板与电脑。

四字提纲：**源、血、家、信**——出于神，由宝血印证，包括我们的儿女，呼召我们凭信心回应。

## 继续开发

构建结果已提交在 `dist/`。两个持续部署工作流都会重新构建并检查原文一致性，再发布静态成品。

```sh
python -m pip install -r requirements.txt
python scripts/build.py
python scripts/check.py
python -m http.server 4189 --directory dist
```

`content.html` 为讲章与研读正文；`study-content.html` 为独立信经学习；`data.json` 为讨论题和记忆卡；`style.css`、`v2.css` 与 `app.js` 为界面与交互。`scripts/build.py` 生成5个网页。`sources/used-texts.json` 保存构建使用的指定来源快照，离线构建不需要重新下载；来源摘要见 `sources/verification.json`。

如需重新抓取指定来源：`python scripts/fetch-sources.py`，再构建并运行检查。只抓取本课实际使用的来源，所有请求成功才更新快照；来源文字变化应审阅后提交。

## 发布与运维

推送 `main` 后 `.github/workflows/pages.yml` 构建、检查并发布 GitHub Pages。Surge 手动命令：`surge ./dist covenant-love-genesis17-20261017-v2-gtser.surge.sh`。没有在源码、公开文件或 README 中保存账号密码或令牌。

Surge 持续部署已配置：仓库 Actions Secrets 中保存 `SURGE_LOGIN`、`SURGE_TOKEN`；`surge.yml` 在推送后发布，凭证不出现在源码中。需要轮换时，在 GitHub Secrets 更新即可。

旧地址同步新版内容：

- https://08-ser-gt-je-personal-20261003.github.io/covenant-love-genesis17-20261017-v1/
- https://covenant-love-genesis17-20261017-v1.surge.sh

新仓库的 Surge 工作流同时发布新旧两个域名。原仓库同步源文件后，其 Pages 工作流更新旧 Pages 地址；原仓库不重复运行 Surge 发布。

## 来源与解释边界

三份信经中文正文及联合信条引文均提取自 https://ccifellowship.org ，没有改用其他中文译本。正文保留标点与字词，去掉脚注上标并调整布局。指定来源中文译文与古代原稿语言并非同一概念。引用来源及适用范围在网页中列明。

讲章采用三项联合信条与古代三大信经框架，区分记号与实体、可见归属与实际得救。没有将洗礼视为自动重生，没有把全家受洗推断成明确列出婴孩。历史年代与地图的不确定性已标明。仅保留本课直接相关的查考来源，不声称穷尽网站全部内容。

诗歌保留用户给定编号；诗集版本不明的两首圣诗没有猜写曲名、歌词或音频。系统语音取决于浏览器和设备；不依赖外部音频服务。

## 验证

`scripts/check.py` 检查链接、章节、讨论题、三份信经及7个信条引文块的逐字一致性。`scripts/verify-browser.mjs` 使用 Playwright 检查320、360、390、768、1024、1440、1920像素屏宽及全部5页，验证目录、答案、配色、讲章模式、地图、救赎历史探索和背诵，并生成打印PDF样张。开发检查需安装 Playwright 到 `.deploy/tools`。表格只在其容器内滚动；尊重系统减少动态效果偏好。

`python scripts/check-public.py` 核验新旧4个公开地址的8个核心文件，与本地发行版逐一比较（允许正常的换行符转换）。

外部信经译文与资料的权利属于原来源；本项目不声称拥有其版权。地图与封面 SVG 为原创示意视觉。
