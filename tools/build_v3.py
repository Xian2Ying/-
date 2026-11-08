# -*- coding: utf-8 -*-
"""
v3 生成器（ADR-004 方案 A）：正式版 src/index.html 全程冻结不动，
以它为基准生成「v1.1 学习反馈增强版」game.v3.html：

  P0-2 例句卡：答对/答错都展示「词 + 词性 + 释义 + 英文例句 + 中文例句」
  P0-2 答错延长停留（850ms → 2.6s）并给一句话提示
  P1   T1 看词选义补 🔊 喇叭（主打发音的游戏，最该听音的题型不该没声音）
  额外 发音链路 onerror 换源后补 play()（与 v2.1 同一修复，避免"只加载不播放"）

输出：
  src/proto/game.v3.html   —— 仓库留档（可复现）
  word-quest-lab/game.v3.html —— 部署副本（附 WQ_SHARE_PATCH 分享口令补丁）
对照组 src/index.html 与 game.html 一律不改。
"""
import io, os, sys

REPO = "C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest"
LAB = "C:/Users/XIAN&YING/WorkBuddy/2026-10-31-22-18-46/word-quest-lab"
SRC = os.path.join(REPO, "src", "index.html")
OUT_REPO = os.path.join(REPO, "src", "proto", "game.v3.html")
OUT_LAB = os.path.join(LAB, "game.v3.html")

PATCH = """
<script>/* WQ_SHARE_PATCH: 部署平台分享口令透传（幂等，仅作用于测试站副本） */
(function(){
  var m=(location.search||"").match(/[?&]sharecode=[^&]*/);
  if(!m) return;
  var q=m[0].replace(/^[?&]/,"");
  Array.prototype.forEach.call(document.querySelectorAll("a[href]"),function(a){
    var h=a.getAttribute("href")||"";
    if(!h||/^(https?:|#|mailto:|javascript:|data:)/.test(h)) return;
    if(h.indexOf("sharecode=")!==-1) return;
    a.setAttribute("href", h+(h.indexOf("?")===-1?"?":"&")+q);
  });
})();
</script>
"""

V3_CSS = """  /* v3：例句卡 + T1 喇叭 + 答错强化反馈 */
  .excard{margin-top:12px;border:3px solid var(--edge);background:var(--bg2);padding:12px;animation:fade .18s ease-out}
  .excard .hw{font-size:16px;color:var(--gold);font-weight:bold;letter-spacing:.5px}
  .excard .pos{font-size:12px;color:var(--dim);margin-left:6px;font-weight:normal}
  .excard .zh{font-size:13px;margin:4px 0 8px}
  .excard .en{font-size:13px;line-height:1.6;border-left:3px solid var(--purple);padding-left:8px;color:#e6e1f5}
  .excard .zh2{font-size:12px;color:var(--dim);margin-top:3px;padding-left:11px}
  .excard .tip{margin-top:8px;font-size:12px;color:var(--gold);background:#3a2f14;border:2px solid var(--edge);padding:6px 8px}
  .spk-inline{margin-left:8px;font-size:15px;background:none;border:2px solid var(--edge);color:var(--ink);padding:2px 9px;cursor:pointer;font-family:inherit;vertical-align:middle}
  .spk-inline:active{transform:translateY(1px)}
"""

CARD_JS = """/* v3：例句卡（100 词 example / exampleZh 现成，此前从未展示） */
function tipFor(q, w){
  if(q.type === "T2") return "听音时先抓住首音节和重音，再对选项。";
  if(q.type === "T3") return "按音节拆开记：" + w.en + "，拼完再读一遍。";
  return "把上面的例句读两遍，" + w.en + " 就跟着句子住进脑子了。";
}
function appendExampleCard(q, w, ok){
  var card = document.createElement("div");
  card.className = "excard";
  var html = '<div class="hw">' + w.en + '<span class="pos">' + (w.pos || "") + '</span></div>' +
             '<div class="zh">' + w.zh + '</div>';
  if(w.example) html += '<div class="en">' + w.example + '</div>';
  if(w.exampleZh) html += '<div class="zh2">' + w.exampleZh + '</div>';
  if(!ok) html += '<div class="tip">💡 ' + tipFor(q, w) + '</div>';
  card.innerHTML = html;
  $("q-body").appendChild(card);
  try{ card.scrollIntoView({block:"nearest", behavior:"smooth"}); }catch(e){}
}
function judge(ok, chosen, btn){"""


def repl(src, old, new, label):
    if old not in src:
        raise SystemExit("ANCHOR NOT FOUND: " + label)
    return src.replace(old, new, 1)


def build():
    with io.open(SRC, encoding="utf-8") as f:
        s = f.read().replace("\r\n", "\n")

    # 1) 例句卡样式
    s = repl(s,
             ".blanks{font-size:26px;letter-spacing:6px;color:var(--gold);margin:14px 0}",
             ".blanks{font-size:26px;letter-spacing:6px;color:var(--gold);margin:14px 0}\n" + V3_CSS,
             "v3 css")

    # 2) 本地 mp3 缺失记忆表
    s = repl(s,
             "var voiceCache = {};         // 单词 -> 预加载的 <audio>",
             "var voiceCache = {};         // 单词 -> 预加载的 <audio>\n"
             "var noLocal = {};            // 本地 mp3 缺失过的词，下次直接走在线源（减少 404 与首击静默）",
             "v3 noLocal decl")

    # 3) onerror 换源后补 play()
    s = repl(s, """  a.dataset.stage = "0";
  a.onplaying = function(){ voiceFail = 0; voiceResult = "ok"; };
  a.onerror = function(){
    var st = parseInt(a.dataset.stage || "0", 10);
    if(st < 2){
      var next = voiceSrc(text, st + 1);
      a.dataset.stage = String(st + 1);
      if(next){ a.src = next; return; }   // 本地文件缺失就换在线，在线也失败才放弃
    }
    voiceFail++; voiceResult = "fail";
    speakNative(text);
  };
  a.src = voiceSrc(text, 0);""",
             """  var st0 = noLocal[text] ? 1 : 0;   // 已知缺本地 mp3 的词，直接走在线源
  a.dataset.stage = String(st0);
  a.onplaying = function(){ voiceFail = 0; voiceResult = "ok"; };
  a.onerror = function(){
    var st = parseInt(a.dataset.stage || "0", 10);
    if(st === 0) noLocal[text] = 1;
    if(st < 2){
      var next = voiceSrc(text, st + 1);
      a.dataset.stage = String(st + 1);
      if(next){
        try{ a.src = next; }catch(e){}
        var p2 = a.play();               // 换源后必须重新 play()，否则只加载不播放
        if(p2 && p2.catch) p2.catch(function(){});
        return;
      }
    }
    voiceFail++; voiceResult = "fail";
    speakNative(text);
  };
  a.src = voiceSrc(text, st0);""",
             "v3 voiceFor")

    # 4) 音源全部失败时直接走合成音，避免对着空 src 重复 play
    s = repl(s,
             """    if(a){
      // 只留一个声音在放，避免快速连点叠音""",
             """    if(a){
      var st = parseInt(a.dataset.stage || "0", 10);
      if(st >= 2){ voiceFail++; voiceResult = "fail"; speakNative(text); return; }
      // 只留一个声音在放，避免快速连点叠音""",
             "v3 speak guard")

    s = repl(s,
             """          if(err && err.name === "AbortError") return;   // 换 src 引起的中断，不算失败
          if(playShared(text)) return;   // 自动播放被拦，换已解锁元素再来一次""",
             """          if(err && err.name === "AbortError") return;   // 换 src 引起的中断，不算失败
          if(parseInt(a.dataset.stage || "0", 10) < 2) return;   // 交给 onerror 继续回退
          if(playShared(text)) return;   // 自动播放被拦，换已解锁元素再来一次""",
             "v3 speak catch")

    # 5) T1 看词选义补喇叭
    s = repl(s,
             """      ? '<div class="word">' + q.word.en + '</div><div class="phon">' + q.word.phonetic + '</div><div class="ask">选出正确的中文释义</div>'""",
             """      ? '<div class="word">' + q.word.en + '<button class="spk-inline" id="spk1" title="听发音">🔊</button></div><div class="phon">' + q.word.phonetic + '</div><div class="ask">选出正确的中文释义</div>'""",
             "v3 t1 head")

    s = repl(s,
             """    if(q.type === "T2"){ $("spk2").onclick = function(){ speak(q.word.en); }; speak(q.word.en); }""",
             """    if(q.type === "T2"){ $("spk2").onclick = function(){ speak(q.word.en); }; speak(q.word.en); }
    if(q.type === "T1"){ $("spk1").onclick = function(){ speak(q.word.en); }; }""",
             "v3 t1 bind")

    # 6) 例句卡 + 停留时长
    s = repl(s, "function judge(ok, chosen, btn){", CARD_JS, "v3 card fn")

    s = repl(s,
             """  setTimeout(function(){
    run.i++;
    if(run.i >= run.qs.length) finish();
    else renderQ();
  }, q.type === "T3" ? 1100 : 850);""",
             """  // v3：答对答错都弹例句卡，把「做题」变成「学词」
  appendExampleCard(q, w, ok);

  setTimeout(function(){
    run.i++;
    if(run.i >= run.qs.length) finish();
    else renderQ();
  }, ok ? (q.type === "T3" ? 1600 : 1500) : 2600);""",
             "v3 judge card")

    # 7) 版本标识 + 口语镇口径
    s = repl(s, "词勇者 v0.1.3 · 声音修复版 · 词库 100 词",
             "词勇者 v1.1 · 例句卡版 · 词库 100 词", "v3 footer")
    s = repl(s,
             'alert("口语镇还在建造中 🏗️\\n预计 11 月中旬开放：可以跟 NPC 用英语随便聊，不会打分。");',
             'alert("🏗️ 口语镇正在建造中\\n它是路线图里的下一站：跟 NPC 用英语随便聊，AI 不打分只陪你练。\\n本版先打磨「例句卡 + 发音反馈」。");',
             "v3 kouyu alert")

    # 写仓库留档（LF，无补丁）
    with io.open(OUT_REPO, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)
    # 写部署副本（附分享口令补丁）
    with io.open(OUT_LAB, "w", encoding="utf-8", newline="\n") as f:
        f.write(s.rstrip("\n") + "\n" + PATCH + "\n")

    print("OK: game.v3.html")
    print("  repo:", OUT_REPO, os.path.getsize(OUT_REPO), "bytes")
    print("  lab :", OUT_LAB, os.path.getsize(OUT_LAB), "bytes")
    for probe in ["excard", "spk1", "noLocal", "appendExampleCard", "v1.1"]:
        assert probe in s, "missing " + probe
    print("  probes OK:", "excard/spk1/noLocal/appendExampleCard/v1.1")


if __name__ == "__main__":
    sys.exit(build() or 0)
