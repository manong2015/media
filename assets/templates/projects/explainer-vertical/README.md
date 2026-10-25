# 科普讲解竖屏组件模板（explainer-vertical）

按 `brand/explainer-visual-style.md` 实现的 HyperFrames 模板，1080 × 1920。
`index.html` 是样张合成（18.2s，4 个场景 + 结尾关注卡），用于确认样式；新视频复制本目录后替换文案即可。

## 组件

| 文件 | 组件 | 样张时段 |
|---|---|---|
| `compositions/chapter-card.html` | 章节卡（序号 + 大字 + 强调短线） | 0–3s |
| `compositions/arch-diagram.html` | 架构色块逐层搭建 + 连线光点 + 牛同学情绪位 + 气泡 + 字幕 | 3–8s |
| `compositions/typing-compare.html` | 关键词逐字打出 + 以前/现在对比卡 + 字幕 | 8–11s |
| `compositions/screen-window.html` | 录屏窗口 + 下划线标注 + 窗口内 punch-in + 字幕 | 11–15s |
| `compositions/outro-follow.html` | 结尾关注卡：牛同学竖大拇指视频 → 定格，「+ 关注」按钮 + @牛同学不上班（无声） | 15–18.2s |
| `styles/explainer.css` | 色板 Token、字体、字幕条、色块、情绪位等共享样式 | — |

## 使用

1. 复制本目录到 `videos/YYYY-MM-DD-topic-slug/`。
2. 改文案：直接编辑各 `compositions/*.html` 中的文字；同一组件多次使用时复制文件并改 `data-composition-id`（宿主、模板根、`window.__timelines` 三处一致）。
3. 录屏：把 `screen-window.html` 中 `#sw-body` 换成 `<video>`。
4. 检查：`npm run check`，再 `npx hyperframes snapshot --at <各场景中点>` 看画面。

## 素材

- `assets/fonts/`：Noto Sans SC（思源黑体同源）与 JetBrains Mono，均为 SIL OFL，许可证随附；源文件在根目录 `assets/fonts/`。
- `assets/images/niu-classmate-front-cutout.png`：牛同学正面抠图，源自 `assets/images/characters/niu-classmate-front-cutout.png`。
- `assets/videos/niu-thumbsup-outro.mp4`：结尾动作片段，取自 `assets/videos/characters/niu-classmate-talk-welcome-v01.mp4` 的 3.917–5.04s（第 95 帧起，避开 3.58s 处的镜头推近），已去音轨；`assets/images/niu-thumbsup-outro-last.png` 为其最后一帧，用于定格。
- 渲染器只读取工程目录内文件，所以字体和角色图需复制进工程，不能引用工程外路径。

## 已知事项

- Noto Sans SC 可变字体约 17MB，check 偶发“fonts still loading after 5000 ms”提示；正式工程可按用字做子集以加快加载。
