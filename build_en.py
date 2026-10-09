#!/usr/bin/env python3
"""Generate website/en.html from website/index.html:
1) ordered longest-first Chinese->English replacements (incl. JS strings),
2) wholesale swap of each <template id="tut-..."> with English tutorial,
3) <html lang> + language cross-link fix."""
import re

SRC = "website/index.html"
DST = "website/en.html"

EN_TUTS = {
"q1a": """<div class="tutorial">
<h3>Q1(a) from zero: PIP exhaustive enumeration (beginner-friendly)</h3>
<p><b>Reader:</b> first encounter with integer programming (IP). This is a pure IP (PIP): all variables are integers.</p>
<table><tr><th>中文</th><th>English</th></tr>
<tr><td>窮舉法</td><td>exhaustive enumeration</td></tr>
<tr><td>可行解／可行域</td><td>feasible solution / feasible region</td></tr>
<tr><td>最優解／最優值</td><td>optimal solution / optimal value</td></tr>
<tr><td>純整數規劃</td><td>pure integer programming (PIP)</td></tr></table>
<p class="cite">Lecture notes: IP definition, LN Ch.1, p.1:14-1:15; why rounding fails, LN Ch.2, p.2:12-2:19; enumeration and Example 2.8, LN Ch.2, p.2:20-2:22.</p>
<ol>
<li><b>Candidate box:</b> 2x1 &le; 7 gives x1 &le; 3; 2x2 &le; 7 gives x2 &le; 3. Check only x1,x2 in {0,1,2,3}: 16 points.</li>
<li><b>Check the three constraints per point:</b> e.g. (2,1): 2&middot;2+2&middot;1=6 &le; 7; 2&middot;2+1=5 &le; 5; 2+1=3 &ge; 1, feasible with z = 6.5&middot;2+5&middot;1 = 18.</li>
<li><b>Counter-example:</b> (3,0) gives 2&middot;3+0 = 6 &gt; 5, violating (2): infeasible, even though z = 19.5 is higher.</li>
<li><b>Compare z over the 8 feasible points:</b> the maximum is 18 at (2,1): the optimal solution.</li>
</ol>
<p><b>Common mistakes:</b> forgetting x1+x2 &ge; 1 (wrongly admitting (0,0)); treating (1,3) as feasible (2+6=8 &gt; 7); picking (3,0) with z=19.5 as optimal.</p>
<details class="quiz"><summary><b>Self-test (click to check yourself)</b></summary>
<p>1. Why skip x1 = 4? 2. Why is (0,0) infeasible? 3. If minimizing, what is optimal?</p>
<p><b>Answers:</b> 1. 2&middot;4 = 8 &gt; 7 violates (1). 2. It violates (3) x1+x2 &ge; 1. 3. Minimum feasible z is 5 at (0,1).</p></details>
</div>""",
"q1b": """<div class="tutorial">
<h3>Q1(b) from zero: PIP branch-and-bound (beginner-friendly)</h3>
<p><b>Reader:</b> you know LP relaxation and want to learn the three steps: branching, bounding, fathoming.</p>
<table><tr><th>中文</th><th>English</th></tr>
<tr><td>分枝定界法</td><td>branch-and-bound (B&amp;B)</td></tr>
<tr><td>LP 鬆弛／上界</td><td>LP relaxation / upper bound</td></tr>
<tr><td>分枝／淘汰／保留解</td><td>branching / fathoming / incumbent</td></tr>
<tr><td>作圖法</td><td>graphical method</td></tr></table>
<p class="cite">Lecture notes: the three B&amp;B steps, LN Ch.2, p.2:25-2:30; algorithm flow, LN Ch.2, p.2:31-2:35; full 2-D PIP example, LN Ch.2, p.2:36-2:45.</p>
<ol>
<li><b>Initialization:</b> incumbent z* = -inf. LP0 gives (1.5,2), z = 19.75 (bound); x1 fractional, no fathoming test passes.</li>
<li><b>Branch x1:</b> since 1 &lt; 1.5 &lt; 2, add x1 &le; 1 (LP1) and x1 &ge; 2 (LP2). LP2 is the integer point (2,1), z = 18: fathomed (test 3), z* = 18.</li>
<li><b>Branch x2:</b> LP1 = (1,2.5) has fractional x2: LP3 (x2 &le; 2) gives (1,2), z = 16.5 (integer but &le; z*, fathomed); LP4 (x2 &ge; 3) gives (0.5,3), z = 18.25 &gt; 18, continue.</li>
<li><b>Branch x1:</b> LP5 (x1 &le; 0) gives (0,3.5), z = 17.5 &le; 18, fathomed by test 1; LP6 (x1 = 1, x2 &ge; 3) is infeasible, fathomed by test 2.</li>
<li><b>No remaining subproblems: the incumbent (2,1), z* = 18 is optimal.</b></li>
</ol>
<p><b>Graph-paper + ruler steps (same for every LP relaxation, LP0 as example):</b></p>
<ol>
<li><b>Axes:</b> x1 horizontal 0-4, x2 vertical 0-4, one unit per square.</li>
<li><b>Lines (two points + ruler):</b> (1) 2x1+2x2 = 7 through (3.5, 0), (0, 3.5); (2) 2x1+x2 = 5 through (2.5, 0), (0, 5); (3) x1+x2 = 1 through (1, 0), (0, 1).</li>
<li><b>Sides + shading:</b> (1)(2) take the origin side (&le;), (3) the far side (&ge;); the feasible region is the pentagon (1,0)-(2.5,0)-(1.5,2)-(0,3.5)-(0,1): shade it.</li>
<li><b>Isoprofit line + slide ruler:</b> pick any z (e.g. z = 13 through (2, 0), (0, 2.6)) and shift it parallel (slope -1.3) up-right until it last touches the region: (1.5, 2).</li>
<li><b>Read + decide:</b> read the intersection (1.5 needs half-square estimation), z = 19.75; x1 fractional: branch x1 (1 &lt; 1.5 &lt; 2).</li>
<li><b>Subproblems:</b> just add one vertical/horizontal line (e.g. x1 &le; 1) and repeat steps 3-5; a new line missing the region means infeasible (e.g. LP6: x1 = 1 forces x2 &le; 2.5, contradicting x2 &ge; 3).</li>
</ol>
<p><b>Your graph-paper photo, element by element (your Q5 photo → draw this for Q1(b)):</b></p>
<table><tr><th>中文</th><th>English</th></tr>
<tr><td>相入面嘅樣 → 係咩意思 → Q1(b) 照畫</td><td>Photo element → meaning → draw this for Q1(b)</td></tr>
<tr><td>橫軸 x1／縱軸 x2（手畫箭嘴）→ 座標軸</td><td>Draw axes: x1 horizontal 0-4, x2 vertical 0-4</td></tr>
<tr><td>斜線＋頂部標 22.5 → 原限制線：兩點＋ruler 畫，標截距</td><td>(1) through (3.5,0),(0,3.5); (2) through (2.5,0),(0,5)</td></tr>
<tr><td>對角線 → 原限制線</td><td>(3) through (1,0),(0,1)</td></tr>
<tr><td>線旁小箭嘴 → 可行一側（≤ 近原點，≥ 遠原點）</td><td>(1)(2) arrows toward origin; (3) outward</td></tr>
<tr><td>垂直線 x1=5、6；水平線 x2=5、6 → 分枝加的限制</td><td>LP1: x1=1 vertical; LP4: add x2=3 horizontal; LP5: x1=0; LP6: x1=1</td></tr>
<tr><td>交點圈起標 (5.5,6) → 圖上讀 LP 最優（半格估讀）＋計 z</td><td>LP0 ring (1.5,2) z=19.75; LP1 (1,2.5); LP4 (0.5,3); LP5 (0,3.5); LP2/LP3 ring integer points</td></tr>
<tr><td>（相無，記得加）等利潤線 → 證明點解呢點最優</td><td>Dashed slope -1.3 line through optimum (copy canvas orange line); write z + verdict beside it</td></tr></table>
<p class="cite">LP6 drawing: the sheet shows the x1 = 1 vertical line, but the x2 &ge; 3 region never meets (1) 2+2x2 &le; 7 (which forces x2 &le; 2.5): contradiction, so write Infeasible &rarr; Fathomed (test 2).</p>
<p><b>Common mistakes:</b> branching the wrong variable (use the first fractional variable in natural order); stopping at the first integer solution without clearing nodes whose bounds are &le; z*; forgetting to update the incumbent.</p>
<details class="quiz"><summary><b>Self-test (click to check yourself)</b></summary>
<p>1. Why is the LP4 bound 18.25 not the answer? 2. Why is LP5 fathomed? 3. Which test fathoms LP6?</p>
<p><b>Answers:</b> 1. (0.5,3) is fractional: only a bound. 2. Test 1: 17.5 &le; z* = 18. 3. Test 2: its LP relaxation is infeasible.</p></details>
</div>""",
"q2a": """<div class="tutorial">
<h3>Q2(a) from zero: BIP exhaustive enumeration (beginner-friendly)</h3>
<p><b>Reader:</b> first binary integer programming (BIP) / 0-1 programming problem.</p>
<table><tr><th>中文</th><th>English</th></tr>
<tr><td>二元變數</td><td>binary variable</td></tr>
<tr><td>窮舉法</td><td>exhaustive enumeration</td></tr>
<tr><td>限制式左端值</td><td>constraint left-hand side (LHS)</td></tr></table>
<p class="cite">Lecture notes: BIP definition, LN Ch.2, p.2:3; assignment example, LN Ch.2, p.2:4-2:6; 2^n enumeration complexity, LN Ch.2, p.2:23-2:24.</p>
<ol>
<li><b>2^5 = 32 points:</b> n = 5 binary variables, each 0/1: 32 combinations.</li>
<li><b>Three numbers per point:</b> (1) LHS = x1+2x2-3x4-x5 (need &le; 0); (2) LHS = -15x1+30x2-35x3+45x4+45x5 (need &ge; 50); z = 3x1+3x2+5x3-2x4-x5.</li>
<li><b>Example (1,1,1,1,1):</b> (1) LHS = 1+2-3-1 = -1 &le; 0; (2) LHS = -15+30-35+45+45 = 70 &ge; 50; z = 8.</li>
<li><b>Counter-example (1,1,1,0,0):</b> highest z = 11 but (2) LHS = -20 &lt; 50: infeasible. High z does not imply feasibility.</li>
<li><b>Among 9 feasible points the max z is 8: the unique optimum.</b></li>
</ol>
<p><b>Common mistakes:</b> reading (2) as &le;; dropping negative coefficients (-2x4, -x5); calling the z = 11 point optimal while ignoring feasibility.</p>
<details class="quiz"><summary><b>Self-test (click to check yourself)</b></summary>
<p>1. Is (0,0,0,1,1) feasible? Its z? 2. How many feasible points? 3. Why is (0,1,0,0,1) infeasible?</p>
<p><b>Answers:</b> 1. Feasible, z = -3. 2. Nine. 3. (1) LHS = 0+2-0-1 = 1 &gt; 0 violates (1).</p></details>
</div>""",
"q2b": """<div class="tutorial">
<h3>Q2(b) from zero: BIP branch-and-bound (beginner-friendly)</h3>
<p><b>Reader:</b> you can enumerate BIP and want to learn fixing binary variables plus reading LP-solver printouts.</p>
<table><tr><th>中文</th><th>English</th></tr>
<tr><td>固定變數</td><td>variable fixing (x = 0 / 1)</td></tr>
<tr><td>電腦輸出</td><td>computer printout (LP solver output)</td></tr>
<tr><td>最佳界／最新子問題</td><td>best bound / most recent subproblem</td></tr></table>
<p class="cite">Lecture notes: B&amp;B algorithm, LN Ch.2, p.2:31-2:35; full BIP example (fixing, printouts), LN Ch.2, p.2:74-2:93.</p>
<ol>
<li><b>Rewrite + relax:</b> xj in {0,1} equals 0 &le; xj &le; 1 plus integrality; dropping integrality gives LP0. Solver printout: (1,1,1,0.7222,0.8333), z = 8.7222.</li>
<li><b>Branch x4:</b> the first fractional variable in natural order is x4 = 0.7222: fix x4 = 0 (BIP1) and x4 = 1 (BIP2). Subproblem choice: best bound or most recent; both lead to BIP2 first here.</li>
<li><b>BIP2:</b> printout (1,1,1,1,0.5556), z = 8.4444, x5 fractional: fix x5 = 0 (BIP3) and x5 = 1 (BIP4).</li>
<li><b>BIP4:</b> integer point (1,1,1,1,1), z = 8: fathomed by test 3, new incumbent z* = 8.</li>
<li><b>Re-check:</b> BIP1 bound 1.9286 &le; 8 (test 1); BIP3 bound 5.4286 &le; 8 (test 1). Nothing remains: (1,1,1,1,1) is optimal.</li>
</ol>
<p><b>Common mistakes:</b> using xj &le; floor / &ge; floor+1 on binary variables (fix 0/1 directly); stopping at the integer solution without clearing the rest via test 1; mistaking an LP bound for an integer answer.</p>
<details class="quiz"><summary><b>Self-test (click to check yourself)</b></summary>
<p>1. Why branch x4 instead of x1 in LP0? 2. Why no further branching on BIP3? 3. If BIP1 bound were 8.5, what next?</p>
<p><b>Answers:</b> 1. x1 = 1 is already integer; x4 is the first fractional variable. 2. Bound 5.4286 &le; z* = 8: fathomed by test 1. 3. 8.5 &gt; 8: keep branching (on x2 or x3).</p></details>
</div>""",
}

REPLACEMENTS = [
("SEEM3440 作業一 詳解 HW1-2 Solutions", "SEEM3440 Assignment 1 Solutions HW1-2"),
("SEEM3440 作業一 HW1-2 詳解 | Assignment 1 Solutions", "SEEM3440 Assignment 1 Solutions HW1-2"),
("整數規劃 Integer Programming：窮舉法 exhaustive enumeration ＋ 分枝定界法 branch-and-bound", "Integer Programming: exhaustive enumeration + branch-and-bound"),
("答案 PDF Answers PDF", "Answers PDF"),
("答案 PDF", "Answers"),
("英文答案（只有答案，沒有推導過程）English answers only, no derivations.", "English answers only, no derivations."),
("⬇ 下載／新分頁開啟 PDF", "Download / open PDF in new tab"),
("Q1(a) 窮舉法 exhaustive enumeration（25 分）", "Q1(a) Exhaustive enumeration (25 marks)"),
("Q1(b) PIP 分枝定界法 branch-and-bound（25 分）", "Q1(b) PIP branch-and-bound (25 marks)"),
("Q2(a) BIP 窮舉法 exhaustive enumeration（25 分）", "Q2(a) BIP exhaustive enumeration (25 marks)"),
("Q2(b) BIP 分枝定界法 branch-and-bound（25 分）", "Q2(b) BIP branch-and-bound (25 marks)"),
("Q1(a) 窮舉", "Q1(a) Enumeration"),
("Q1(b) PIP 分枝定界", "Q1(b) PIP B&B"),
("Q2(a) 窮舉", "Q2(a) Enumeration"),
("Q2(b) BIP 分枝定界", "Q2(b) BIP B&B"),
("題目 recap：", "Problem recap: "),
("用 PIP Branch-and-Bound 解 Q1，並畫出分枝定界樹 B&B tree；每個子問題的 LP 鬆弛以作圖法求解 LP relaxation solved graphically。",
 "Solve Q1 by PIP branch-and-bound and draw the B&B tree; each subproblem LP relaxation solved graphically."),
("用 PIP Branch-and-Bound 解 Q1，並畫出分枝定界樹 B&amp;B tree；每個子問題的 LP 鬆弛以作圖法求解 LP relaxation solved graphically。",
 "Solve Q1 by PIP branch-and-bound and draw the B&B tree; each subproblem LP relaxation solved graphically."),
("互動小工具：分枝定界樹＋LP 可行域 B&B tree + LP feasible region",
 "Widget: B&B tree + LP feasible region"),
("互動小工具：分枝定界樹＋LP 可行域 B&amp;B tree + LP feasible region",
 "Widget: B&B tree + LP feasible region"),
("用 BIP Branch-and-Bound 解 Q2，每個子問題的 LP 鬆弛用 LP 求解器解（附電腦輸出 show computer printouts）。",
 "Solve Q2 by BIP branch-and-bound; each subproblem LP relaxation solved by an LP solver (computer printouts shown)."),
("答案 Answer：", "Answer: "),
("候選整數點共 16 個（x1,x2 ∈ {0,1,2,3}），可行 8 個；", "16 candidate integer points (x1,x2 in {0,1,2,3}), 8 feasible; "),
("最優解 optimal (x1*,x2*) = (2,1)，z* = 18", "optimal (x1*,x2*) = (2,1), z* = 18"),
("最優解 optimal (1,1,1,1,1)，z* = 8（唯一 unique）", "optimal (1,1,1,1,1), z* = 8 (unique)"),
("最優 (2,1)，z* = 18", "optimum (2,1), z* = 18"),
("最優 (1,1,1,1,1)，z* = 8", "optimum (1,1,1,1,1), z* = 8"),
("LP0 (1.5,2) z=19.75 → 分枝 x1；LP1 (1,2.5) z=19 → 分枝 x2；LP2 (2,1) z=18 整數，z*=18；LP3 (1,2) z=16.5 淘汰；LP4 (0.5,3) z=18.25 → 分枝 x1；LP5 (0,3.5) z=17.5 ≤ 18 淘汰；LP6 不可行淘汰。",
 "LP0 (1.5,2) z=19.75: branch x1; LP1 (1,2.5) z=19: branch x2; LP2 (2,1) z=18 integer, z*=18; LP3 (1,2) z=16.5 fathomed; LP4 (0.5,3) z=18.25: branch x1; LP5 (0,3.5) z=17.5 <= 18 fathomed; LP6 infeasible, fathomed."),
("LP0 (1,1,1,0.7222,0.8333) z=8.7222 → 分枝 x4；x4=0 支 LP1 z=1.9286（後被 z*=8 淘汰）；x4=1 支 LP2 z=8.4444 → 分枝 x5；LP3 (x5=0) z=5.4286 淘汰；LP4 (x5=1) = (1,1,1,1,1) 整數 z=8。",
 "LP0 (1,1,1,0.7222,0.8333) z=8.7222: branch x4; x4=0 branch LP1 z=1.9286 (later fathomed by z*=8); x4=1 branch LP2 z=8.4444: branch x5; LP3 (x5=0) z=5.4286 fathomed; LP4 (x5=1) = (1,1,1,1,1) integer, z=8."),
("32 個二元點中 9 個可行；", "9 of 32 binary points feasible; "),
("互動小工具：可行性檢查器 feasibility checker", "Widget: feasibility checker"),
("互動小工具：分枝定界樹＋LP 可行域 B&B tree + LP feasible region", "Widget: B&B tree + LP feasible region"),
("互動小工具：二元點檢查器 binary-point checker", "Widget: binary-point checker"),
("互動小工具：節點電腦輸出 LP-solver printouts", "Widget: node computer printouts"),
("拖動滑桿選擇整數點，檢查每條限制是否成立 check each constraint：", "Drag sliders to pick an integer point and check each constraint:"),
("點選節點查看 LP 鬆弛結果 click a node for LP relaxation result：", "Click a node for its LP relaxation result:"),
("作圖法示意：陰影為 LP 可行域 feasible region；綠點可行整數點，紅點不可行；大圓圈為所選節點 LP 最優解。Graphical-method sketch.",
 "Graphical-method sketch: shaded LP feasible region; green = feasible integer points, red = infeasible; orange ring = selected node LP optimum."),
("作圖法示意：陰影為 LP 可行域 feasible region；綠點可行整數點，紅點不可行；大圓圈為所選節點 LP 最優解；橙色虛線為等利潤線 isoprofit line（經 LP 最優點，ruler 沿此斜率平移）。Graphical-method sketch.",
 "Graphical-method sketch: shaded LP feasible region; green = feasible integer points, red = infeasible; orange ring = selected node LP optimum; orange dashed line = isoprofit line (through the LP optimum: slide the ruler along this slope)."),
("手稿格式（照 past exam Question 5 格式）", "Hand-written format (following past exam Question 5)"),
("每格左邊 (IPn) 寫子問題：原題＋外加限制＋當時保留解 z*；右邊 (LPn) 寫手作圖結果：圖上最優＋z＋判決。格之間係分枝標籤。z* 由 −∞ 開始，見到整數解先更新。",
 "Each box: left (IPn) states the subproblem (original + added constraints + current incumbent z*); right (LPn) states the hand-drawn result (graph optimum + z + verdict). Branch labels sit between boxes. z* starts at −∞ and updates only on integer solutions."),
("外加：無", "added: none"),
("外加：", "added: "),
("保留解 z* = ", "incumbent z* = "),
("x1,x2 ≥ 0 整數", "x1,x2 ≥ 0 integer"),
("圖上最優", "graph optimum"),
("x1 非整數 → 分枝 x1", "x1 fractional → branch x1"),
("x2 非整數 → 分枝 x2", "x2 fractional → branch x2"),
("整數解 → 淘汰 (test 3)，保留解 z* = 18", "integer solution → fathomed (test 3), incumbent z* = 18"),
("整數但 16.5 ≤ 18 → 淘汰 (test 1)", "integer but 16.5 ≤ 18 → fathomed (test 1)"),
("17.5 ≤ 18 → 淘汰 (test 1)", "17.5 ≤ 18 → fathomed (test 1)"),
("x1 = 1 與 x2 ≥ 3 矛盾 → 無可行解 → 淘汰 (test 2)", "x1 = 1 contradicts x2 ≥ 3 → infeasible → fathomed (test 2)"),
("分枝：", "branch: "),
("分枝 (IP1)：", "branch (IP1): "),
("分枝 (IP4)：", "branch (IP4): "),
("（即 x1 = 1）", " (i.e. x1 = 1)"),
("；", "; "),
("無剩餘子問題 → 最優 (2,1)，z* = 18。", "No remaining subproblems → optimal (2,1), z* = 18."),
("照抄圖（7 張手繪答案圖）", "Copy-ready figures (7 hand-drawn answer plots)"),
("每張對應一格手稿：原限制線＋箭嘴＋陰影＋紅色分枝線＋圈起最優點＋z＋判決。照住畫上 graph paper 即可，撳圖放大／下載。",
 "Each plot matches one manuscript box: original lines + arrows + shading + red branch lines + ringed optimum + z + verdict. Copy onto graph paper; click to enlarge/download."),
("⬇ 下載 LP0", "Download LP0"),
("⬇ 下載 LP1", "Download LP1"),
("⬇ 下載 LP2", "Download LP2"),
("⬇ 下載 LP3", "Download LP3"),
("⬇ 下載 LP4", "Download LP4"),
("⬇ 下載 LP5", "Download LP5"),
("⬇ 下載 LP6", "Download LP6"),
("max <code class=\"k\">z = 6.5x1 + 5x2</code>，s.t. <code class=\"k\">2x1+2x2 ≤ 7</code> (1)，<code class=\"k\">2x1+x2 ≤ 5</code> (2)，<code class=\"k\">x1+x2 ≥ 1</code> (3)，<code class=\"k\">x1,x2 ≥ 0 整數 integer</code>。",
 "max <code class=\"k\">z = 6.5x1 + 5x2</code>, s.t. <code class=\"k\">2x1+2x2 ≤ 7</code> (1), <code class=\"k\">2x1+x2 ≤ 5</code> (2), <code class=\"k\">x1+x2 ≥ 1</code> (3), <code class=\"k\">x1,x2 ≥ 0 integer</code>."),
("max <code class=\"k\">z = 3x1+3x2+5x3−2x4−x5</code>，s.t. <code class=\"k\">x1+2x2−3x4−x5 ≤ 0</code> (1)，<code class=\"k\">−15x1+30x2−35x3+45x4+45x5 ≥ 50</code> (2)，<code class=\"k\">xj ∈ {0,1}</code>。",
 "max <code class=\"k\">z = 3x1+3x2+5x3−2x4−x5</code>, s.t. <code class=\"k\">x1+2x2−3x4−x5 ≤ 0</code> (1), <code class=\"k\">−15x1+30x2−35x3+45x4+45x5 ≥ 50</code> (2), <code class=\"k\">xj ∈ {0,1}</code>."),
("16 點窮舉表 enumeration table", "16-point enumeration table"),
("32 點窮舉表 enumeration table", "32-point enumeration table"),
("只看可行點 feasible only", "Feasible only"),
("看全部 show all", "Show all"),
("只看可行點", "Feasible only"),
("可行？Feasible?", "Feasible?"),
("可行？", "Feasible?"),
("(1) LHS ≤ 0?", "(1) LHS <= 0?"),
("(2) LHS ≥ 50?", "(2) LHS >= 50?"),
("SEEM3440 Operations Research II · Assignment 1 ·窮舉＋分枝定界 | Enumeration + Branch-and-Bound",
 "SEEM3440 Operations Research II · Assignment 1 · Enumeration + Branch-and-Bound"),
("✕ 關閉／返回", "Close / Back"),
("📖 詳細教學 tutorial", "Tutorial"),
("Q1(a) 詳細教學 tutorial", "Q1(a) Tutorial"),
("Q1(b) 詳細教學 tutorial", "Q1(b) Tutorial"),
("Q2(a) 詳細教學 tutorial", "Q2(a) Tutorial"),
("Q2(b) 詳細教學 tutorial", "Q2(b) Tutorial"),
("詳細教學", "Tutorial"),
("（外加 ", " (added "),
("）：LP 最優 ", "): LP optimum "),
("，z = ", ", z = "),
("★ 最優 optimal", "optimal"),
("（可行，但 z < 18，非最優）", " (feasible but z < 18, not optimal)"),
("（可行，但 z < 8，非最優）", " (feasible but z < 8, not optimal)"),
("可行 feasible", "feasible"),
("不可行 infeasible", "infeasible"),
("LP0：無外加限制，(1.5,2)，z=19.75，上界；x1 非整數 → 分枝 x1。Branch x1 (1≤x1≤2 split).",
 "LP0: no added constraint, (1.5,2), z=19.75, upper bound; x1 fractional: branch x1."),
("LP1：(1,2.5)，z=19；x2 非整數 → 分枝 x2。Branch x2.", "LP1: (1,2.5), z=19; x2 fractional: branch x2."),
("LP2：整數點 (2,1)，z=18 → 檢驗3淘汰，保留解 incumbent z*=18。",
 "LP2: integer point (2,1), z=18: fathomed by test 3, incumbent z*=18."),
("LP3：整數點 (1,2)，z=16.5 ≤ 18 → 淘汰 fathomed，保留解不變。",
 "LP3: integer point (1,2), z=16.5 <= 18: fathomed, incumbent unchanged."),
("LP4：(0.5,3)，z=18.25 > 18 → 分枝 x1。Branch x1.", "LP4: (0.5,3), z=18.25 > 18: branch x1."),
("LP5：(0,3.5)，z=17.5 ≤ 18 → 檢驗1淘汰 fathomed by test 1。",
 "LP5: (0,3.5), z=17.5 <= 18: fathomed by test 1."),
("LP6：x1=1 與 x2≥3 下 2+2x2≤7 要求 x2≤2.5，矛盾 → 無可行解，檢驗2淘汰 fathomed by test 2。",
 "LP6: x1=1 with x2>=3 forces x2<=2.5 from 2+2x2<=7, contradiction: infeasible, fathomed by test 2."),
("第一個非整數變數 x4 → 固定 x4=0 / x4=1。Branch x4.", "First fractional variable x4: fix x4=0 / x4=1."),
("界 1.9286 ≤ z*=8 → 檢驗1淘汰 fathomed by test 1。", "Bound 1.9286 <= z*=8: fathomed by test 1."),
("x5 非整數 → 固定 x5=0 / x5=1。Branch x5.", "x5 fractional: fix x5=0 / x5=1."),
("界 5.4286 ≤ z*=8 → 檢驗1淘汰 fathomed by test 1。", "Bound 5.4286 <= z*=8: fathomed by test 1."),
("全整數 all-integer → 檢驗3淘汰，新保留解 new incumbent z*=8。",
 "All-integer: fathomed by test 3, new incumbent z*=8."),
("（固定 ", " (fixed "),
("第一個非整數變數（自然順序）是 x4 = 0.7222 → 固定 x4 = 0（BIP1）與 x4 = 1（BIP2）。選子問題規則：最佳界 best bound 或最新建立其一，此處皆選 BIP2 先做亦可。",
 "placeholder-unused"),
("☀️ 淺色", "Light"),
("🌙 深色", "Dark"),
("<html lang=\"zh-Hant\">", "<html lang=\"en\">"),
("onclick=\"location.href='en.html'\">EN", "onclick=\"location.href='index.html'\">中文"),
("原題＋例題地圖", "Questions + example map"),
("原題要求＋例題地圖（跟住做）", "Original questions + example map (follow along)"),
("原題 HW1-2（Assignment 1，滿分 100 分，全部要答）：", "Original HW1-2 (Assignment 1, 100 marks, answer all):"),
("Q1（50 分）IP0：", "Q1 (50 marks) IP0:"),
("(a) 25 分 exhaustive enumeration；(b) 25 分 PIP Branch-and-Bound＋畫分枝定界樹，每個子問題的 LP 鬆弛用手作圖法（graph paper＋ruler）。",
 "(a) 25 marks exhaustive enumeration; (b) 25 marks PIP branch-and-bound + B&B tree, each subproblem LP relaxation solved graphically by hand (graph paper + ruler)."),
("Q2（50 分）BIP0：", "Q2 (50 marks) BIP0:"),
("(a) 25 分 exhaustive enumeration；(b) 25 分 BIP Branch-and-Bound＋畫分枝定界樹，每個子問題的 LP 鬆弛用 LP solver（附電腦輸出 computer printouts）。",
 "(a) 25 marks exhaustive enumeration; (b) 25 marks BIP branch-and-bound + B&B tree, each subproblem LP relaxation by LP solver (computer printouts attached)."),
("例題對照表（每題跟邊個例題做）", "Example cross-reference (which worked example each question follows)"),
("功課題", "Question"),
("，s.t. ", ", s.t. "),
("(1)，", "(1), "),
("(2)，", "(2), "),
("(3)，", "(3), "),
("xj ≥ 0 整數</code>。", "xj ≥ 0 integer</code>."),
("xj binary</code>。", "xj binary</code>."),
("跟嘅例題（做法一樣）", "Worked example to follow (same method)"),
("講義位置", "Lecture location"),
("Example 2.8：定整數 box → 逐點驗證 → 窮舉表 → 比 z",
 "Example 2.8: fix integer box → check point by point → enumeration table → compare z"),
("ch02-3.pdf pp.20–22（投影片 2:20–2:22）；另見點解唔可以四捨五入 pp.12–19",
 "ch02-3.pdf pp.20–22 (slides 2:20–2:22); why rounding fails: pp.12–19"),
("2-D PIP 完整例：Init z*=−∞ → LP bound → 三個 fathoming 檢驗 → 分第一個非整數變數 → 畫樹",
 "2-D PIP full example: init z*=−∞ → LP bound → three fathoming tests → branch first fractional variable → draw tree"),
("ch02-3.pdf pp.36–45（投影片 2:36–2:45）；算法總綱 pp.31–35",
 "ch02-3.pdf pp.36–45 (slides 2:36–2:45); algorithm overview pp.31–35"),
("BIP 定義＋2ⁿ 複雜度＋Example 2.8 表格式：32 點逐點驗兩條式",
 "BIP definition + 2ⁿ complexity + Example 2.8 table format: check both constraints for each of 32 points"),
("ch02-3.pdf p.3（2:3）、pp.23–24（2:23–2:24）、pp.20–22",
 "ch02-3.pdf p.3 (2:3), pp.23–24 (2:23–2:24), pp.20–22"),
("BIP 完整例：binary 改寫 0≤xj≤1＋整數 → LP 鬆弛 → 固定 0/1 分枝 → 讀 printout → test 1 回頭淘汰",
 "BIP full example: rewrite binary as 0≤xj≤1 + integrality → LP relaxation → fix 0/1 branching → read printout → test-1 sweep"),
("ch02-3.pdf pp.74–93（投影片 2:74–2:93）", "ch02-3.pdf pp.74–93 (slides 2:74–2:93)"),
("用法：喺自己電腦開 ch02-3.pdf（第 N 頁＝投影片 2:N），對住上表頁碼逐步跟。下面每題另有「跟住例題做」對應步驟。講義 PDF 只留本機、不上傳 GitHub。",
 "How to use: open ch02-3.pdf on your own computer (page N = slide 2:N) and follow the pages above step by step. Each question below has its own follow-the-example steps. Lecture PDFs stay local and are not uploaded to GitHub."),
("跟住例題做（對照 Example 2.8，ch02-3.pdf pp.20–22）：", "Follow the example (cf. Example 2.8, ch02-3.pdf pp.20–22):"),
("例題先定 box；本題由 2x1 ≤ 7、2x2 ≤ 7 得 x1,x2 ∈ {0,1,2,3}。",
 "The example fixes a box first; here 2x1 ≤ 7, 2x2 ≤ 7 give x1,x2 ∈ {0,1,2,3}."),
("例題逐點驗限制＋計 z；本題逐點驗 (1)(2)(3)＋計 z（下表 Feasible? 欄 N 後括號註明違反邊條）。",
 "The example checks each point and computes z; here check (1)(2)(3) + z per point (table Feasible? column marks violated constraints in brackets after N)."),
("例題比 z 取最大；本題 8 個可行點比 z，(2,1) 的 18 最大。",
 "The example compares z for the max; here compare z over 8 feasible points, (2,1) with 18 is max."),
("交功課照例題表格式列 16 點（x1, x2, Feasible?, z）。",
 "For submission list all 16 points in the example table format (x1, x2, Feasible?, z)."),
("跟住例題做（對照 2-D PIP 例，ch02-3.pdf pp.36–45；算法總綱 pp.31–35）：",
 "Follow the example (cf. 2-D PIP example, ch02-3.pdf pp.36–45; overview pp.31–35):"),
("初始化 z* = −∞，解原問題 LP 鬆弛得 bound（例題 LP0 23.75；本題 LP0 (1.5,2) 19.75）。",
 "Initialize z* = −∞ and solve the original LP relaxation for a bound (example LP0 23.75; here LP0 (1.5,2) 19.75)."),
("三個 fathoming 檢驗逐一試（照例題 p.2:38 寫法：Test 1／2／3 passed／failed 都要寫）。",
 "Try all three fathoming tests one by one (as in example p.2:38: write down Test 1/2/3 passed/failed)."),
("分枝永遠揀第一個非整數變數（自然順序），加 xj ≤ floor／xj ≥ floor+1（例題 x1 = 3.75 → x1 ≤ 3／x1 ≥ 4；本題 x1 = 1.5 → x1 ≤ 1／x1 ≥ 2）。",
 "Always branch the first fractional variable (natural order), adding xj ≤ floor / xj ≥ floor+1 (example x1 = 3.75 → x1 ≤ 3 / x1 ≥ 4; here x1 = 1.5 → x1 ≤ 1 / x1 ≥ 2)."),
("整數解出現即 fathomed（test 3）並更新 incumbent；最後用 test 1 回頭淘汰其餘節點，無剩餘即最優。",
 "An integer solution is fathomed (test 3) at once and updates the incumbent; finish with a test-1 sweep over remaining nodes — none left means optimal."),
("畫樹格式照例題 p.2:45：每個節點寫 LP 鬆弛解＋z bound，另行寫當時 incumbent。",
 "Draw the tree as in example p.2:45: each node shows the LP relaxation solution + z bound, plus the current incumbent."),
("跟住例題做（對照 BIP 定義 p.3、2ⁿ 複雜度 pp.23–24、Example 2.8 表格式 pp.20–22）：",
 "Follow the example (cf. BIP definition p.3, 2ⁿ complexity pp.23–24, Example 2.8 table pp.20–22):"),
("n = 5 個 binary → 2⁵ = 32 點（例題 2.9 講窮舉點解會爆炸，但 n = 5 先做得到）。",
 "n = 5 binary variables → 2⁵ = 32 points (Example 2.9 explains why enumeration explodes, but n = 5 is doable)."),
("每點計三個數：(1) LHS（要 ≤ 0）、(2) LHS（要 ≥ 50，唔好睇錯方向）、z。",
 "Compute three numbers per point: (1) LHS (need ≤ 0), (2) LHS (need ≥ 50, watch the direction), z."),
("反例警惕：z 最高唔等於最優 —— (1,1,1,0,0) z = 11 但 (2) LHS = −20，不可行。",
 "Warning: highest z is not optimal — (1,1,1,0,0) has z = 11 but (2) LHS = −20, infeasible."),
("交功課列 32 點（x, z, Feasible?），可行 9 點，最優 (1,1,1,1,1) z = 8 唯一。",
 "For submission list all 32 points (x, z, Feasible?); 9 feasible, optimum (1,1,1,1,1) z = 8 unique."),
("跟住例題做（對照 BIP 完整例，ch02-3.pdf pp.74–93）：",
 "Follow the example (cf. BIP full example, ch02-3.pdf pp.74–93):"),
("先改寫：xj binary 等價於 0 ≤ xj ≤ 1 加整數限制（例題 pp.75–76），刪整數限制得 LP0。",
 "First rewrite: xj binary equals 0 ≤ xj ≤ 1 plus integrality (example pp.75–76); dropping integrality gives LP0."),
("分枝唔用 floor 式，直接固定 x = 0／x = 1（例題 pp.78–79；本題先分 x4 再分 x5）。",
 "Branch by fixing x = 0 / x = 1 directly, not floor splits (example pp.78–79; here branch x4 then x5)."),
("每個節點保留 solver printout：x＋z bound（本題 LP0 8.7222、LP2 8.4444、LP1 1.9286、LP3 5.4286、LP4 整數 8）。",
 "Keep the solver printout per node: x + z bound (here LP0 8.7222, LP2 8.4444, LP1 1.9286, LP3 5.4286, LP4 integer 8)."),
("整數解（test 3）更新 z* = 8 後，用 test 1 回頭淘汰 BIP1／BIP3（照例題 p.92 做法）。",
 "After the integer solution (test 3) updates z* = 8, fathom BIP1/BIP3 with test 1 (as in example p.92)."),
("畫樹格式照例題 p.93：BIP0 → {BIP1, BIP2}；BIP2 → {BIP3, BIP4}。",
 "Draw the tree as in example p.93: BIP0 → {BIP1, BIP2}; BIP2 → {BIP3, BIP4}."),
]

def main():
    h = open(SRC, encoding="utf-8").read()
    for src, dst in sorted(REPLACEMENTS, key=lambda p: -len(p[0])):
        if src in h:
            h = h.replace(src, dst)
    for tid, body in EN_TUTS.items():
        pat = re.compile(r'<template id="tut-%s">.*?</template>' % tid, re.S)
        h, n = pat.subn("<template id=\"tut-%s\">\n%s\n</template>" % (tid, body), h)
        assert n == 1, tid
    open(DST, "w", encoding="utf-8").write(h)
    print("Wrote", DST)

if __name__ == "__main__":
    main()
