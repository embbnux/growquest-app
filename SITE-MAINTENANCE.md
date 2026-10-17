# GrowQuest 网站维护

## 2026-10-17：1.5 内容与页面更新

- 维持 GitHub Pages / Jekyll，不更换域名或托管方式；`CNAME` 为 `growquest.xyz`。
- `/`、`/README.{zh,zh-Hant,ja,ko,es,fr,de,pt}.html`、`/privacy`、`/privacy.html` 保留；额外提供 `/privacy/`，无需修改 App Store Connect 已登记 URL。语言页原有简介标题锚点也保留。
- 页面内容在 `_data/content.json`，布局在 `_layouts/`，样式在 `assets/site.css`。九语言首页共用布局，六语言截图共用对应本地化资源。
- 内容来源：App 仓库 `docs/app-review/release-1.5.0.md`、六语言商店文案和 `src/i18n/*.ts`。1.5 仍在提交准备，因此标为即将推出；学习伙伴说明为 1.4 既有功能，不宣传尚未发布的限期活动或未实现的周报。
- 简体中文营销文案遵守 D3，不宣传 AI；隐私政策仍完整披露实际数据处理。法/德/葡网站翻译明确使用英文截图，App 本身支持六语言，隐私政策明确回退英文。
- 六语言隐私政策直接取自 App `privacyPolicy.content`，将 Markdown 粗体章节转换为语义标题，并按用户要求将网站联系邮箱统一改为 `support@growquest.xyz`；其余正文与 App 来源一致，保留其 2026-10-05 政策日期。本次网站同步日期为 2026-10-17。
- 图片来源：App 的 `docs/app-review/screenshots/iphone/{locale}/{home,plans,library,pet}.png`，等比例缩小为 WebP；图标来自 App `assets/icon.png`。没有对真实界面作生成或改绘。

## 构建与校验

```sh
bundle install
bundle exec jekyll build
python3 tools/validate.py _site
```

`tools/validate.py` 检查稳定路径、内部链接和锚点、下载与反馈地址、图片尺寸与替代文字、九语言发布标签、简体中文文案边界及隐私旧文回归。无需 JavaScript、第三方字体或追踪脚本。

本地验收：Jekyll 3.10 构建通过，16 个 HTML 页面链接校验通过；九语言分别在 320、390、1440 宽度下检查，共 27 组无水平溢出。浏览器检查了语言切换、FAQ 展开与隐私页链接。证据可保存于被忽略的 `qa/`。

## 发布

GitHub Pages 沿用 `main` 分支根目录自动发布，域名为 `growquest.xyz`，启用 HTTPS。提交并推送后，需等待对应提交的 Pages 部署成功，再检查 `https://growquest.xyz/`、`https://growquest.xyz/privacy`、`https://growquest.xyz/privacy.html` 及原有语言页，确认线上新内容后，才可勾选 App 1.5 发布清单的网站隐私政策项。

App 1.5 正式可下载后，再更新九语言 `soon` 和 `release_note`，同时调整相应校验；不要在网站先行宣称版本已经发布。
