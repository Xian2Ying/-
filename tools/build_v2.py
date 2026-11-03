# -*- coding: utf-8 -*-
"""
体检 v2 生成器：以 Desktop 当前原型为「对照组」(已复制到 workspace/src/proto/ 冻结不动)，
生成「实验组」v2 文件：
  - control-group.v2.html  : 仅把发音换成三级回退(本地mp3→在线TTS→合成)
  - roguelike.v2.html      : 同上
  - battle-template.v2.html: 用 control-group 的真实词库+四档难度引擎，套上「词=怪」战斗皮肤 + 三级发音
  - index.compare.html     : 对照组 vs 实验组 同屏对比入口
原文件(对照组)一律不修改。
"""
import io, os
ROOT = "C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest/src/proto"

# ---- 三级发音回退（复刻主游戏 src/index.html 的 voiceSrc/voiceFor/speak，去掉 save 依赖）----
AUDIO_JS = r'''/* ===== 三级发音回退：本地mp3 → 在线TTS(有道) → 设备合成 =====
   原型词库词汇无本地mp3，故手机实际路径走在线TTS；本地文件若存在也优先 */
var SHARE_Q=(function(){var m=(location.search||"").match(/[?&]sharecode=[^&]*/);return m?m[0].replace(/^&/,"?"):"";})();
var voiceCache={},voiceFail=0,voiceResult="",sharedAudio=null,audioUnlocked=false;
function ensureAudio(){try{if(!sharedAudio)sharedAudio=new Audio();}catch(e){}}
function unlockVoice(){if(audioUnlocked)return;audioUnlocked=true;try{if(!sharedAudio)sharedAudio=new Audio();sharedAudio.onplaying=function(){voiceFail=0;voiceResult="ok";};sharedAudio.src="data:audio/wav;base64,UklGRiQAAABXQVZFZm10IBAAAAABAAEAgD4AAAB9AAACABAAZGF0YQAAAAA=";var p=sharedAudio.play();if(p&&p.catch)p.catch(function(){});}catch(e){}}
function voiceSrc(text,stage){if(stage===0)return "audio/"+encodeURIComponent(text)+".mp3"+SHARE_Q;if(stage===1)return "https://dict.youdao.com/dictvoice?audio="+encodeURIComponent(text)+"&type=2";return "";}
function voiceFor(text){var a=voiceCache[text];if(a)return a;a=new Audio();a.preload="auto";a.dataset.stage="0";a.onplaying=function(){voiceFail=0;voiceResult="ok";};a.onerror=function(){var st=parseInt(a.dataset.stage||"0",10);if(st<2){var nx=voiceSrc(text,st+1);a.dataset.stage=String(st+1);if(nx){a.src=nx;return;}}voiceFail++;voiceResult="fail";speakNative(text);};a.src=voiceSrc(text,0);voiceCache[text]=a;return a;}
function speakNative(text){if(!window.speechSynthesis)return false;try{window.speechSynthesis.cancel();var u=new SpeechSynthesisUtterance(text);u.lang="en-US";u.rate=1;u.volume=1;window.speechSynthesis.speak(u);return true;}catch(e){return false;}}
function playShared(text){try{if(!sharedAudio)return false;sharedAudio.src=voiceSrc(text,0);var p=sharedAudio.play();if(p&&p.catch)p.catch(function(){voiceResult="fail";speakNative(text);});return true;}catch(e){return false;}}
function speak(text){if(!text)return;unlockVoice();if(voiceFail<3){var a;try{a=voiceFor(text);}catch(e){a=null;}if(a){for(var k in voiceCache){if(k!==text){try{voiceCache[k].pause();voiceCache[k].currentTime=0;}catch(e){}}}try{window.speechSynthesis&&window.speechSynthesis.cancel();}catch(e){}try{a.pause();a.currentTime=0;}catch(e){}var p=a.play();if(p&&p.catch){p.catch(function(err){if(err&&err.name==="AbortError")return;if(playShared(text))return;voiceFail++;voiceResult="fail";speakNative(text);});}return;}}speakNative(text);}
["pointerdown","touchstart","click"].forEach(function(ev){document.addEventListener(ev,function(){unlockVoice();ensureAudio();},{once:true,passive:true});});'''

BATTLE_CSS = r'''
/* ===== 词怪战斗皮肤(v2) 追加 ===== */
.topbar .combo{margin-left:auto;font-weight:700;color:var(--gold);min-height:18px;transition:transform .15s;font-size:15px;}
.topbar .combo.pop{transform:scale(1.5);}
.monster{display:flex;flex-direction:column;align-items:center;margin:4px 0 12px;}
.mob{font-size:58px;line-height:1;transition:transform .25s,opacity .25s;filter:drop-shadow(0 6px 10px rgba(0,0,0,.4));}
.mob.hit{transform:translateY(40px) scale(.4) rotate(12deg);opacity:0;}
.mob.attack{animation:shake .4s;}
.mob.boss{font-size:72px;filter:drop-shadow(0 0 12px var(--red));}
@keyframes shake{0%,100%{transform:translateX(0)}20%{transform:translateX(-10px)}40%{transform:translateX(10px)}60%{transform:translateX(-7px)}80%{transform:translateX(7px)}}
.mobname{margin-top:6px;font-size:14px;color:var(--gold);}
.mobname.boss{color:var(--red);}
.stage.flash-ok{box-shadow:0 0 0 3px var(--green) inset;}
.stage.flash-bad{box-shadow:0 0 0 3px var(--red) inset;}'''

BATTLE_LOGIC = r'''
/* ===== 词怪战斗逻辑(v2) ===== */
let combo=0,actx;
function blip(freq,dur,type){try{if(!actx)actx=new (window.AudioContext||window.webkitAudioContext)();if(actx.state==="suspended")actx.resume();var o=actx.createOscillator(),g=actx.createGain();o.type=type||"sine";o.frequency.value=freq;o.connect(g);g.connect(actx.destination);var t=actx.currentTime;g.gain.setValueAtTime(.0001,t);g.gain.exponentialRampToValueAtTime(.2,t+.01);g.gain.exponentialRampToValueAtTime(.0001,t+dur);o.start(t);o.stop(t+dur);}catch(e){}}
function bumpCombo(){var c=document.getElementById("combo");if(!c)return;c.textContent=combo>=2?("🔥 连击 x"+combo):"";c.classList.add("pop");setTimeout(function(){c.classList.remove("pop");},150);}
var BATTLE_FLAVOR={
 easy:{mobs:["🎒","📚","🌸","🎀","✏️","📖","🖍️","🎓","📝","🧸"],names:["走神怪","瞌睡怪","迟到怪","单词小怪","橡皮怪","书虫怪","铅笔怪","学霸怪","作业怪","午睡怪"]},
 normal:{mobs:["🎸","🥁","🎹","🎤","🎶","🎵","🪕","📯","🎷","🎺"],names:["吉他怪","贝斯怪","鼓手怪","键盘怪","主唱怪","谱面怪","和弦怪","节拍怪","管乐怪","返场怪"]},
 hard:{mobs:["🎭","⭐","🎪","🌹","🎀","🩰","🎟️","🎆","💃","🎻"],names:["舞台少女怪","聚光怪","华之怪","revue怪","安可怪","芭蕾怪","门票怪","烟火怪","独舞怪","弦乐怪"]},
 hell:{mobs:["💀","🔥","🎭","⭐","👹","🕯️","⛓️","🌋","🩸","🪦"],names:["词魔","深渊词魔","终幕词魔","华击词魔","安可词魔","烛火词魔","锁链词魔","熔岩词魔","血色词魔","墓园词魔"]}
};
var BOSS_MOBS={easy:"👑",normal:"🌟",hard:"🎭",hell:"💀"};
function monsterHTML(isBoss,mob,mobName){return `<div class="monster"><div class="mob${isBoss?" boss":""}" id="mob">${mob}</div><div class="mobname${isBoss?" boss":""}">${mobName}</div></div>`;}'''

MONSTER_CALL = "monsterHTML(isBoss,mob,mobName)+"

def repl(src, old, new, label):
    if old not in src:
        raise SystemExit("ANCHOR NOT FOUND: " + label)
    return src.replace(old, new, 1)

SPEAK_OLD = 'function speak(t){try{const u=new SpeechSynthesisUtterance(t);u.lang="en-US";speechSynthesis.cancel();speechSynthesis.speak(u);}catch(e){}}'

# ---- control-group.v2 : audio only ----
c = io.open(os.path.join(ROOT,"control-group.html"),encoding="utf-8").read()
c = repl(c, SPEAK_OLD, AUDIO_JS, "control speak")
io.open(os.path.join(ROOT,"control-group.v2.html"),"w",encoding="utf-8").write(c)

# ---- roguelike.v2 : audio only ----
r = io.open(os.path.join(ROOT,"roguelike.html"),encoding="utf-8").read()
r = repl(r, SPEAK_OLD, AUDIO_JS, "rogue speak")
io.open(os.path.join(ROOT,"roguelike.v2.html"),"w",encoding="utf-8").write(r)

# ---- battle-template.v2 : control engine + combat skin + audio ----
b = io.open(os.path.join(ROOT,"control-group.html"),encoding="utf-8").read()
b = repl(b, '<title>词勇者 · 对照组（四级+六级 真实词库 · 四难度基线）</title>',
            '<title>词勇者 · 词怪战斗 v2（真实词库 · 三级发音 · 对照组升级版）</title>', "battle title")
b = repl(b, '</style>', BATTLE_CSS + '\n</style>', "battle css")
b = repl(b, '  <div class="topbar"><div id="prog"></div><div id="tiername"></div></div>',
            '  <div class="topbar"><div id="prog"></div><div id="tiername"></div><div id="combo" class="combo"></div></div>', "battle topbar")
b = repl(b, '  <div id="stage"></div>', '  <div id="stage" class="stage"></div>', "battle stage")
b = repl(b, SPEAK_OLD, AUDIO_JS + BATTLE_LOGIC, "battle speak+logic")
b = repl(b, 'const sl=stageLabel(t,level);',
            'const sl=stageLabel(t,level);var bf=BATTLE_FLAVOR[t.key];var mob=isBoss?(BOSS_MOBS[t.key]||"👹"):bf.mobs[(level-1)%bf.mobs.length];var mobName=isBoss?"词魔王":bf.names[(level-1)%bf.names.length];', "battle mob vars")
b = repl(b, 'const stage=$("stage"); stage.className="";', 'const stage=$("stage"); stage.className="stage";', "battle stage class")
SPK_OLD = "'<button class=\"speak\" id=\"speak\">🔊 听发音</button>'+"
SPK_NEW = MONSTER_CALL + "'<button class=\"speak\" id=\"speak\">🔊 听发音</button>'+"
b = repl(b, SPK_OLD, SPK_NEW, "battle monster html")
b = repl(b, "'<button class=\"next\" id=\"next\" disabled>下一关 →</button>';", "'<button class=\"next\" id=\"next\" disabled>继续深入 →</button>';", "battle next text")
b = repl(b, '$("fb").textContent="正确";$("fb").className="feedback ok";',
            '$("mob").classList.add("hit");$("stage").classList.add("flash-ok");combo++;bumpCombo();$("fb").textContent=combo>=3?("击退！🔥 连击 x"+combo):"击退！";$("fb").className="feedback ok";blip(660,.12,"triangle");setTimeout(function(){blip(880,.12,"triangle");},90);', "battle choose correct")
b = repl(b, '$("fb").textContent="错误，正确答案已标出";$("fb").className="feedback bad";',
            '$("mob").classList.add("attack");$("stage").classList.add("flash-bad");combo=0;bumpCombo();$("fb").textContent="怪反击了！正确答案已标出";$("fb").className="feedback bad";blip(150,.2,"sawtooth");', "battle choose wrong")
io.open(os.path.join(ROOT,"battle-template.v2.html"),"w",encoding="utf-8").write(b)

# ---- comparison hub ----
HUB = '''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>词勇者 · 原型版本对比（对照组 vs 实验组 v2）</title>
<style>
:root{--bg:#15121f;--panel:#262038;--gold:#f4c75b;--txt:#f3eefb;--dim:#a89fc0;}
*{box-sizing:border-box;} body{margin:0;background:radial-gradient(circle at 50% 0%,#241d39,#15121f 70%);color:var(--txt);font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;padding:18px;}
h1{font-size:20px;text-align:center;margin:6px 0 4px;} .sub{text-align:center;color:var(--dim);font-size:13px;margin-bottom:18px;}
table{width:100%;max-width:760px;margin:0 auto;border-collapse:collapse;}
th,td{border:1px solid #3a3358;padding:10px 12px;font-size:14px;vertical-align:top;}
th{background:var(--panel);color:var(--gold);} tr:nth-child(even) td{background:rgba(255,255,255,.03);}
a{color:var(--gold);text-decoration:none;} a:hover{text-decoration:underline;}
.tag{display:inline-block;font-size:11px;padding:1px 8px;border-radius:10px;background:#3a1d1d;color:var(--red);font-weight:700;margin-left:6px;}
.note{text-align:center;color:var(--dim);font-size:12px;margin-top:16px;max-width:760px;margin-left:auto;margin-right:auto;line-height:1.6;}
</style></head><body>
<h1>⚔️ 词勇者 · 原型版本对比</h1>
<div class="sub">「对照组」= 原始文件（冻结不动）　|　「实验组 v2」= 体检修复版</div>
<table>
<tr><th>玩法</th><th>对照组（原始）</th><th>实验组 v2（体检）</th><th>v2 关键改动</th></tr>
<tr><td>📋 平铺基线</td><td><a href="control-group.html">control-group.html</a></td><td><a href="control-group.v2.html">control-group.v2.html</a></td><td>发音改三级回退（在线TTS 解决手机无声）</td></tr>
<tr><td>🎲 单词肉鸽</td><td><a href="roguelike.html">roguelike.html</a></td><td><a href="roguelike.v2.html">roguelike.v2.html</a></td><td>同上（发音修复）</td></tr>
<tr><td>🗡️ 词怪战斗<span class="tag">A/B 关键</span></td><td><a href="battle-template.html">battle-template.html</a><br><small style="color:var(--dim)">v0：仅3个写死单词</small></td><td><a href="battle-template.v2.html">battle-template.v2.html</a><br><small style="color:var(--dim)">接真实词库+四档难度+战斗皮肤</small></td><td>接入真实词库/难度，使与对照组成为有效 A/B；发音修复；去掉开发备注</td></tr>
</table>
<div class="note">对照组文件全程未修改，仅作对照基准。v2 为新增独立文件，可逐项对比验证「游戏是壳、AI 是核」的演进。</div>
</body></html>'''
io.open(os.path.join(ROOT,"index.compare.html"),"w",encoding="utf-8").write(HUB)

print("OK: built control-group.v2.html, roguelike.v2.html, battle-template.v2.html, index.compare.html")
# quick sanity
for f in ["control-group.v2.html","roguelike.v2.html","battle-template.v2.html"]:
    s=io.open(os.path.join(ROOT,f),encoding="utf-8").read()
    assert "function speak(text)" in s and "voiceSrc" in s, f+" missing audio"
    print(f, "-> audio OK,", len(s), "bytes")
assert "BATTLE_FLAVOR" in io.open(os.path.join(ROOT,"battle-template.v2.html"),encoding="utf-8").read()
print("battle BATTLE_FLAVOR OK")
