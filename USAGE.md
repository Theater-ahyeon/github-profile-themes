# 使用与维护

## 给 Theater-ahyeon 切换主页

1. 从根目录图库选择主题，打开对应 `themes/<主题名>/README.md`。
2. 复制 **Raw 源文**，替换 `Theater-ahyeon/Theater-ahyeon` 仓库的根 `README.md`。
3. 提交后主页会采用新主题。图片使用本合集的绝对地址，不需要搬运图片。

本次只建立主题合集，没有切换当前个人主页。默认仍是 Q 版菲比手账。

## 主题结构

每套主题包含完整 README，以及深浅各六张图片：横幅、分隔线、统计、开源协作、按项目汇总、页脚。PNG 预览是制作时的截图；SVG 数据卡和 README 会每日更新。

README 使用 GitHub 支持的 `<picture>` 与媒体条件选择深浅素材。所有 SVG 内嵌位图，不依赖外部字体、脚本或嵌套网络图片。SVG 中的文字可以编辑，原始素材在 `sources/`。

## 本地重建

需要 Python 3.12+，基本生成不需要额外 Python 包。

```powershell
python scripts/build.py
```

已登录 GitHub CLI 后刷新真实统计：

```powershell
python scripts/build.py --refresh
```

GitHub Actions 每天 01:41 UTC 自动刷新，使用仓库提供的 `GITHUB_TOKEN`。失败时不会提交新结果。数据是 Theater-ahyeon 的公开数据：已合并 PR 必须有 `mergedAt`，排除本人仓库、私有仓库和 fork 仓库，支持完整分页。

## 更新预览

安装 Playwright 并准备 Chromium 后：

```powershell
npm install --no-save --package-lock=false playwright
npx playwright install chromium
python scripts/build.py
node scripts/preview.cjs
```

该脚本生成 14 张完整深浅预览、14 张横幅预览，并检查 390px 移动宽度下图片加载与横向溢出。

## 为其他账号改造

这些是 Theater-ahyeon 的个人主页模板，直接复制不会自动变成其他账号的数据。请同步修改 `scripts/build.py` 的 `REPO`、姓名和联系方式，以及工作流的 `GH_LOGIN`，重新生成后再使用。菲比历史横幅的文字位于对应 SVG 中；若要改这些横幅，请直接编辑 SVG 文本。

素材来源与使用边界见 [SOURCES.md](SOURCES.md)。
