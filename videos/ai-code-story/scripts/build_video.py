"""Build editable HyperFrames HTML from the anonymized shot plan."""

from __future__ import annotations

import html
import json
from collections import OrderedDict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = json.loads((ROOT / "shot-plan.json").read_text(encoding="utf-8"))
AUDIO_META = ROOT / "audio_meta.json"
SCENES = OrderedDict()


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def duration(shot: dict) -> float:
    if AUDIO_META.exists():
        metadata = json.loads(AUDIO_META.read_text(encoding="utf-8"))
        voices = {item["id"]: item for item in metadata.get("voices", [])}
        if shot["id"] in voices:
            return round(float(voices[shot["id"]]["duration_s"]) + 0.45, 2)
    return round(max(6.4, len(shot["voice"]) / 4.5 + 1.2), 2)


for idx, shot in enumerate(PLAN, 1):
    shot["id"] = f"shot{idx:02d}"
    shot["duration"] = duration(shot)
    SCENES.setdefault(shot["scene"], []).append(shot)


def visual(shot: dict) -> str:
    kind = shot["kind"]
    if kind == "hook":
        return '<div class="big-number">99<span>%</span></div><div class="question">你敢上线吗？</div>'
    if kind == "statement":
        return '<div class="stamp yes">敢</div><div class="stamp later">后来才敢</div>'
    if kind == "manual":
        return '<div class="flow-step">聊天框提问</div><div class="flow-arrow">↓</div><div class="flow-step">复制到项目</div><div class="flow-arrow">↓</div><div class="flow-step warn">自己改到能用</div>'
    if kind == "debate":
        return '<div class="debate-card">保守派 <span>AI 写一点，人写一点</span></div><div class="debate-card selected">激进派 <span>主要开发交给 AI</span></div>'
    if kind == "debate_detail":
        return '<div class="choice-old">手写代码</div><div class="choice-arrow">→</div><div class="choice-new">AI 主写</div><div class="micro">方向定了。工具还没学会。</div>'
    if kind == "learn":
        return '<div class="week">' + ''.join(f'<span>{i}</span>' for i in range(1, 8)) + '</div><div class="flow-step">研究工具</div><div class="flow-step">动手做 demo</div>'
    if kind == "lesson":
        return '<div class="chat user">这个改好了吗？</div><div class="chat ai">改好了，完全没问题。</div><div class="chat result">实际打开：还有问题</div>'
    if kind in {"prototype", "client", "mismatch"}:
        if kind == "mismatch":
            return '<div class="mock-row"><div class="mock mini"><i></i><b></b><em></em></div><div class="mock mini off"><i></i><b></b><em></em></div><div class="mock mini missing"><i></i><b></b><em></em></div></div><div class="micro">风格跑偏　·　修改遗漏</div>'
        bubble = '<div class="speech">这么快，还这么好看？</div>' if kind == "client" else ''
        return f'{bubble}<div class="mock"><i></i><b></b><em></em><small></small><small></small></div>'
    if kind == "skill":
        return '<div class="document"><div class="doc-head">prototype/SKILL.md</div><div class="doc-rule">01　统一视觉规范</div><div class="doc-rule">02　固定输出要求</div><div class="doc-rule">03　核对修改范围</div></div>'
    if kind == "framework":
        return '<div class="stack-card">前端 <strong>成熟组件库</strong></div><div class="stack-card">后端 <strong>现有 Java 框架</strong></div><div class="micro">成熟的东西，继续复用</div>'
    if kind == "architecture":
        return '<div class="document"><div class="doc-head">architecture/SKILL.md</div><div class="tree">├─ frontend / 页面与组件</div><div class="tree">├─ backend / 接口与服务</div><div class="tree">└─ conventions / 项目规范</div></div>'
    if kind == "two_skills":
        return '<div class="stack-card">原型 Skill <strong>统一原型</strong></div><div class="stack-card">架构 Skill <strong>搭建骨架</strong></div><div class="micro">一次整理，反复使用</div>'
    if kind == "checklist":
        return '<div class="task checked">需求与原型 <span>✓</span></div><div class="task checked">开发清单 <span>✓</span></div><div class="task active">讨论方案 <span>→</span></div><div class="task">AI 实施 <span>○</span></div>'
    if kind == "loop":
        return '<div class="chat user">还有问题吗？</div><div class="chat ai">有。</div><div class="rounds">第 1 轮　→　第 12 轮　→　第 27 轮…</div><div class="chat ai">还有。</div>'
    if kind == "boundary":
        return '<div class="boundary-q">会影响这次上线吗？</div><div class="boundary-yes">会 → 现在修</div><div class="boundary-no">不会 → 记录下来</div>'
    if kind == "severity":
        return '<div class="stack-card must">必须修 <strong>功能 / 数据 / 性能</strong></div><div class="stack-card">可记录 <strong>偏好 / 低收益优化</strong></div>'
    if kind == "testing":
        return '<div class="task checked">AI：数据、接口、并发 <span>✓</span></div><div class="task active">人：真实流程 <span>✓</span></div><div class="task active">人：关键结果 <span>✓</span></div>'
    if kind == "deploy":
        return '<div class="terminal"><div>$ deploy --production</div><div>SERVER=••••••</div><div>SECRET=••••••</div><div class="terminal-warning">权限与密钥要管清楚</div></div>'
    if kind == "takeaway":
        return '<div class="takeaway">把规范做成 Skill</div><div class="takeaway">给审查设边界</div><div class="takeaway">由人做最终验收</div>'
    if kind == "final":
        return '<div class="final-answer">要。</div><div class="final-line">看懂 AI　判断风险　负责上线</div>'
    raise ValueError(kind)


SCENE_STYLE = """
@font-face{font-family:YaHei;src:local('Microsoft YaHei');font-weight:400}
@font-face{font-family:YaHei;src:local('Microsoft YaHei Bold');font-weight:700}
*{box-sizing:border-box}
#root{position:absolute;inset:0;overflow:hidden;font-family:YaHei,sans-serif;color:#151515}
.shot{position:absolute;inset:0;background:#F5F5F2;overflow:hidden}
.shot:nth-of-type(even){background:#ECEDEA}
.shot:after{content:'';position:absolute;left:0;right:0;top:1390px;height:530px;background:#E4E6E2;border-top:2px solid #D0D3CE}
.shot:before{content:'';position:absolute;right:0;bottom:0;width:210px;height:75px;background:#F15A3C;z-index:1}
.topline{position:absolute;left:82px;top:205px;font-size:31px;font-weight:700;letter-spacing:.06em;color:#5E615D}
.topline:before{content:'';display:inline-block;width:23px;height:23px;margin-right:16px;background:#F15A3C;vertical-align:0}
.headline{position:absolute;left:78px;top:325px;width:920px;font-size:82px;font-weight:700;letter-spacing:-.045em;line-height:1.18}
.accentline{position:absolute;left:82px;top:510px;width:915px;font-size:70px;font-weight:700;color:#D94125;line-height:1.18}
.visual{position:absolute;left:82px;top:650px;width:916px;height:465px;overflow:hidden}
.subline{position:absolute;left:82px;top:1125px;width:916px;font-size:38px;color:#4B4E4B;line-height:1.3}
.big-number{font-family:YaHei,sans-serif;font-weight:700;font-size:330px;line-height:1;color:#151515;letter-spacing:-.08em}
.big-number span{font-size:180px;color:#F15A3C}
.question{font-size:84px;font-weight:700;color:#D94125}
.stamp{position:absolute;border:6px solid #151515;border-radius:20px;padding:16px 50px;font-weight:700;transform:rotate(-5deg)}
.stamp.yes{font-size:170px;left:70px;top:20px}
.stamp.later{font-size:70px;right:35px;top:255px;border-color:#F15A3C;color:#D94125;transform:rotate(5deg)}
.flow-step,.stack-card,.task,.debate-card,.takeaway{width:100%;background:#FFF;border:2px solid #151515;border-radius:13px;padding:24px 28px;font-size:47px;font-weight:700;margin-bottom:17px}
.flow-step.warn,.debate-card.selected,.task.active,.stack-card.must{border-color:#D94125;background:#FFF1EB}
.flow-arrow{font-size:41px;text-align:center;height:48px}
.debate-card{height:170px}
.debate-card span{display:block;font-size:37px;font-weight:400;margin-top:12px}
.choice-old,.choice-new{display:inline-block;padding:26px 35px;border:3px solid #151515;font-size:60px;font-weight:700;margin-top:80px}
.choice-new{background:#F15A3C;color:#fff;border-color:#F15A3C}
.choice-arrow{display:inline-block;font-size:75px;padding:0 15px}
.micro{font-size:37px;color:#555;margin-top:28px}
.week{display:flex;gap:8px;margin:28px 0 42px}
.week span{display:grid;place-items:center;width:116px;height:100px;background:#151515;color:#fff;font-size:48px;font-weight:700}
.week span:last-child{background:#F15A3C}
.chat{border-radius:20px;padding:22px 28px;font-size:42px;margin-bottom:20px;max-width:790px}
.chat.user{background:#151515;color:#fff;margin-left:105px}
.chat.ai{background:#fff;border:2px solid #151515}
.chat.result{background:#FFF1EB;border:2px solid #D94125;color:#B5341D}
.mock{position:relative;width:590px;height:405px;margin:4px auto;background:#fff;border:5px solid #151515;border-radius:28px;padding:30px}
.mock i{display:block;width:43%;height:33px;background:#151515;border-radius:5px}
.mock b{display:block;width:100%;height:135px;background:#F15A3C;margin-top:22px;border-radius:12px}
.mock em{display:block;width:75%;height:21px;background:#D0D2CF;margin-top:24px;border-radius:3px}
.mock small{display:block;width:90%;height:14px;background:#D0D2CF;margin-top:19px;border-radius:3px}
.speech{position:absolute;z-index:2;right:10px;top:0;background:#151515;color:#fff;padding:20px 25px;border-radius:18px;font-size:36px;font-weight:700}
.speech+.mock{top:57px}
.mock-row{display:flex;gap:14px;margin-top:30px}
.mock.mini{width:290px;height:345px;padding:22px;border-width:3px}
.mock.mini b{height:115px}
.mock.mini.off b{background:#23607B}
.mock.mini.missing b{height:40px;background:#F15A3C}
.document{background:#fff;border:3px solid #151515;border-radius:14px;min-height:418px;padding:30px 34px;font-size:43px}
.doc-head{font-family:YaHei,sans-serif;font-size:35px;font-weight:700;background:#151515;color:#fff;padding:14px 18px;margin:-30px -34px 30px}
.doc-rule,.tree{border-bottom:2px solid #D2D5D0;padding:14px 0}
.stack-card strong{display:block;font-size:41px;font-weight:400;margin-top:7px}
.task{font-size:44px;padding:23px 26px;margin-bottom:12px}
.task span{float:right;color:#D94125}
.task.checked span{color:#23966C}
.rounds{font-size:37px;font-weight:700;margin:26px 0;color:#D94125}
.boundary-q{font-size:57px;font-weight:700;border-bottom:5px solid #151515;padding:25px 0;margin-bottom:22px}
.boundary-yes,.boundary-no{font-size:48px;padding:26px;margin:12px 0;background:#FDE7DF;border:2px solid #D94125}
.boundary-no{background:#fff;border-color:#151515}
.terminal{height:425px;background:#151515;color:#E6E8E5;border-radius:14px;padding:35px;font-family:YaHei,sans-serif;font-size:42px;line-height:1.8}
.terminal-warning{color:#FF8B72;font-weight:700;margin-top:20px}
.takeaway{font-size:48px;margin-bottom:17px;background:#151515;color:#fff}
.takeaway:nth-child(2){background:#F15A3C;border-color:#F15A3C}
.final-answer{font-size:340px;color:#D94125;font-weight:700;line-height:1}
.final-line{font-size:45px;margin-top:30px;border-top:5px solid #151515;padding-top:35px}
"""


def scene_html(scene_name: str, shots: list[dict]) -> str:
    markup = []
    local = 0.0
    for shot in shots:
        sid = shot["id"]
        markup.append(
            f'<div id="{sid}" class="clip shot" data-start="{local:.2f}" data-duration="{shot["duration"]:.2f}" data-track-index="1" data-beat="{esc(shot["kind"])}" {"data-hold" if shot["kind"] in {"hook", "final"} else ""}>'
            f'<div class="topline">{esc(shot["section"])} · 示意画面</div>'
            f'<div class="headline">{esc(shot["title"])}</div>'
            f'<div class="accentline">{esc(shot["accent"])}</div>'
            f'<div class="visual" data-layout-allow-overflow>{visual(shot)}</div>'
            f'<div class="subline">{esc(shot["sub"])}</div>'
            '</div>'
        )
        local += shot["duration"]
    body = "\n".join(markup)
    script = f"""
const tl = gsap.timeline({{ paused: true }});
document.querySelectorAll('[data-composition-id="{scene_name}"] .shot').forEach((shot) => {{
  const at = Number(shot.dataset.start);
  const length = Number(shot.dataset.duration);
  const accent = shot.querySelector('.accentline');
  const art = shot.querySelector('.visual');
  if (shot.id === 'shot01') return;
  tl.fromTo(art, {{y:35}}, {{y:0, duration:.4, ease:'power3.out'}}, at+.04);
  tl.fromTo(accent, {{opacity:0, x:50}}, {{opacity:1, x:0, duration:.34, ease:'power3.out'}}, at+1.1);
  const parts = [...art.querySelectorAll('.flow-step,.debate-card,.week,.chat,.doc-rule,.tree,.stack-card,.task,.boundary-q,.boundary-yes,.boundary-no,.takeaway,.mock b,.mock em,.mock small,.terminal div,.rounds,.final-line,.micro')];
  const limit = Math.min(4, parts.length);
  for (let i = 1; i < limit; i++) {{
    const cue = at + 2.2 + (i - 1) * Math.max(.9, (length - 5) / Math.max(1, limit - 1));
    tl.fromTo(parts[i], {{opacity:0, y:22}}, {{opacity:1, y:0, duration:.26, ease:'power3.out'}}, cue);
  }}
  tl.fromTo(shot.querySelector('.subline'), {{opacity:0}}, {{opacity:1, duration:.25}}, at + length - 3.1);
}});
window.__timelines["{scene_name}"] = tl;
"""
    return f'''<template>
<style>{SCENE_STYLE}</style>
<div id="root" data-composition-id="{scene_name}" data-width="1080" data-height="1920">{body}</div>
<script>{script}</script>
</template>
'''


def caption_chunks(text: str) -> list[str]:
    chunks = []
    current = ""
    for char in text:
        current += char
        if char in "，；。？！" or len(current) >= 18:
            if current.strip():
                chunks.append(current.strip())
            current = ""
    if current.strip():
        chunks.append(current.strip())
    return chunks


def captions_html() -> str:
    parts = []
    absolute = 0.0
    for shot in PLAN:
        chunks = caption_chunks(shot["voice"])
        total_weight = sum(max(1, len(chunk)) for chunk in chunks)
        start = absolute + .35
        usable = shot["duration"] - .55
        for j, chunk in enumerate(chunks):
            span = usable * max(1, len(chunk)) / total_weight
            parts.append(f'<div id="cap-{shot["id"]}-{j}" class="clip subtitle" data-start="{start:.2f}" data-duration="{span:.2f}" data-track-index="7" data-layout-allow-caption-zone>{esc(chunk)}</div>')
            start += span
        absolute += shot["duration"]
    return f'''<template>
<style>
@font-face{{font-family:YaHei;src:local('Microsoft YaHei');font-weight:400}}
#root{{position:absolute;inset:0;font-family:YaHei,sans-serif;pointer-events:none}}
.subtitle{{position:absolute;left:78px;top:1208px;width:884px;min-height:88px;padding:13px 24px;background:#151515;color:#fff;border-radius:12px;text-align:center;font-size:43px;line-height:1.28;font-weight:700}}
</style>
<div id="root" data-composition-id="captions" data-width="1080" data-height="1920">{''.join(parts)}</div>
<script>window.__timelines["captions"] = gsap.timeline({{paused:true}});</script>
</template>
'''


def index_html() -> str:
    hosts = []
    absolute = 0.0
    starts = {}
    for name, shots in SCENES.items():
        length = sum(s["duration"] for s in shots)
        hosts.append(f'<div id="{name}" class="clip" data-composition-id="{name}" data-composition-src="compositions/{name}.html" data-start="{absolute:.2f}" data-duration="{length:.2f}" data-track-index="1" data-track-kind="graphics" data-width="1080" data-height="1920"></div>')
        absolute += length
    at = 0.0
    for shot in PLAN:
        starts[shot["id"]] = at
        at += shot["duration"]
    voice = []
    if AUDIO_META.exists():
        meta = json.loads(AUDIO_META.read_text(encoding="utf-8"))
        voices = {x["id"]: x for x in meta.get("voices", [])}
        at = 0.0
        for shot in PLAN:
            item = voices.get(shot["id"])
            if item:
                src = Path(item["path"])
                try:
                    src = src.resolve().relative_to(ROOT.resolve())
                except ValueError:
                    pass
                voice.append(f'<audio id="voice-{shot["id"]}" src="{esc(src.as_posix())}" class="clip" data-start="{at:.2f}" data-duration="{float(item["duration_s"]):.2f}" data-track-index="8" data-volume="1"></audio>')
            at += shot["duration"]
    total = round(absolute, 2)
    bgm = f'<audio id="bgm" src="assets/audio/original-bed.mp3" class="clip" data-start="0" data-duration="{total:.2f}" data-track-index="9" data-volume="0.12" data-fade-in="1.2" data-fade-out="2"></audio>'
    cue_kinds = {"hook": "impact", "debate": "whoosh", "skill": "click", "architecture": "click", "loop": "impact", "boundary": "click", "deploy": "impact", "final": "whoosh"}
    sfx = []
    for shot in PLAN:
        cue = cue_kinds.get(shot["kind"])
        if cue:
            sfx.append(f'<audio id="sfx-{shot["id"]}" src="assets/sfx/{cue}.mp3" class="clip" data-start="{starts[shot["id"]]:.2f}" data-duration="{2.1 if cue == "impact" else .6 if cue == "whoosh" else .4}" data-track-index="10" data-volume="0.22"></audio>')
    return f'''<!doctype html>
<html lang="zh-CN" data-resolution="portrait" data-composition-variables='[{{"id":"accent","type":"color","label":"强调色","default":"#F15A3C"}}]'>
<head><meta charset="UTF-8"><meta name="viewport" content="width=1080,height=1920"><title>99% 的代码都让 AI 写，我们怎么敢上线？</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>*{{box-sizing:border-box}}html,body{{width:1080px;height:1920px;margin:0;overflow:hidden;background:#F5F5F2}}#root{{position:relative;width:1080px;height:1920px;overflow:hidden}}</style></head>
<body><div id="root" data-composition-id="main" data-start="0" data-duration="{total:.2f}" data-width="1080" data-height="1920">
{''.join(hosts)}
<div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html" data-start="0" data-duration="{total:.2f}" data-track-index="7" data-track-kind="captions" data-width="1080" data-height="1920"></div>
{''.join(voice)}
{bgm}{''.join(sfx)}
</div><script>window.__timelines["main"] = gsap.timeline({{paused:true}});</script></body></html>
'''


for name, shots in SCENES.items():
    (ROOT / "compositions").mkdir(exist_ok=True)
    (ROOT / "compositions" / f"{name}.html").write_text(scene_html(name, shots), encoding="utf-8")
(ROOT / "compositions" / "captions.html").write_text(captions_html(), encoding="utf-8")
(ROOT / "index.html").write_text(index_html(), encoding="utf-8")
(ROOT / "NARRATION.md").write_text("# 旁白稿（按镜头）\n\n" + "\n\n".join(f"{i}. {shot['voice']}" for i, shot in enumerate(PLAN, 1)) + "\n", encoding="utf-8")
print(f"Built {len(PLAN)} shots in {len(SCENES)} scenes, {sum(x['duration'] for x in PLAN):.2f}s")
