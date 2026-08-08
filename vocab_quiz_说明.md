# vocab_quiz.py 代码详细说明

> 本说明专门写给**具备 BASIC 编程基础**的读者。  
> 我们会用 BASIC 里你熟悉的概念（变量、数组、IF...THEN、循环、子程序等）来对照解释 Python + Streamlit 代码。
>
> **最新更新**：  
> 1. 单词库已移到同目录下的独立文件 `vocab.json`（不再写在脚本内部）。  
> 2. 新增「上一题」功能：点错后可以返回上一题重做，分数会自动撤销。  
> 3. 结果页也可以「返回最后一题修改」。

---

## 一、这个程序整体在做什么？

这是一个**网页版英语单词测验小程序**：

1. 从外部文件 `vocab.json` 加载高中英语单词库，随机抽出 **10 个**。
2. 每次显示一个英文单词，下面给出 **4 个中文选项**（只有一个是对的）。
3. 小朋友选择后点「提交答案」或「跳过」；也可以点「上一题」返回重做。
4. 做完 10 题后，显示得分，并列出做错的题。
5. 可以再来一组新题，或返回最后一题修改。

整个程序用 **Streamlit** 做成网页，你不需要懂网页编程，只要会运行 Python 脚本就行。

---

## 二、BASIC 和 Python 的简单对应关系

| BASIC 概念              | Python / Streamlit 对应                  | 说明 |
|-------------------------|------------------------------------------|------|
| `LET A = 10`            | `a = 10`                                 | 变量赋值 |
| `DIM A(10)`             | `list` 或 `dict`                         | 数组 / 字典 |
| `PRINT "你好"`           | `st.write("你好")` 或 `st.markdown(...)` | 输出到屏幕（网页） |
| `INPUT A$`              | `st.radio(...)` / `st.button(...)`       | 用户输入（选择或点击） |
| `IF ... THEN ... ELSE`  | `if ... elif ... else:`                  | 条件判断 |
| `FOR I = 1 TO 10`       | `for i in range(10):` 或列表推导          | 循环 |
| `GOSUB 1000` / `RETURN` | `def 函数名():` + `return`                | 子程序（函数） |
| `RANDOMIZE` + `RND`     | `random.sample(...)` / `random.shuffle`  | 随机 |
| 全局变量                | `st.session_state.变量名`                 | 网页刷新后还记得的数据 |

**重要区别**：  
Streamlit 程序每点一次按钮，整个 `main()` 函数会**从头到尾再跑一遍**（像重新 RUN 一次）。  
所以必须把「当前做到第几题、得了多少分」等重要数据，存到 `st.session_state` 里，否则一刷新就丢了。

---

## 三、代码结构总览（从上到下）

```
1. 导入工具包
2. 定义单词库 VOCAB（一个大字典）
3. 定义函数 get_options()   —— 生成 4 个选项
4. 定义函数 init_quiz()     —— 开始新一轮测验
5. 定义函数 main()          —— 主程序（页面逻辑）
6. 程序入口：if __name__ == "__main__": main()
```

下面按顺序详细解释。

---

## 四、第 1 部分：导入工具包

```python
import streamlit as st
import random
```

- `import streamlit as st`  
  就像 BASIC 里 `LOAD "STREAMLIT"`，把网页显示功能引进来。  
  以后用 `st.xxx` 来显示文字、按钮、进度条等。

- `import random`  
  提供随机功能，相当于 BASIC 的 `RND`。

---

## 五、第 2 部分：单词库（已独立为 vocab.json）

现在单词库**不再写在脚本内部**，而是放在同目录下的 `vocab.json` 文件中。

脚本启动时会自动加载：

```python
VOCAB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.json")

def load_vocab():
    with open(VOCAB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

VOCAB = load_vocab()
```

`vocab.json` 内容格式示例：

```json
{
  "abandon": "放弃；遗弃",
  "ability": "能力；才能",
  "congratulate": "祝贺",
  ...
}
```

这是一个**字典**（Dictionary）。

- 在 BASIC 里你可以想象成两个平行数组：
  ```
  WORD$(1) = "abandon"   :  MEANING$(1) = "放弃；遗弃"
  WORD$(2) = "ability"   :  MEANING$(2) = "能力；才能"
  ```
- 在 Python 里写成一对一对的：`"英文" : "中文"`。
- 用 `VOCAB["abandon"]` 就能立刻查到它的中文意思（像查表）。
- `list(VOCAB.keys())` 取出所有英文单词。
- `list(VOCAB.values())` 取出所有中文释义。

**好处**：以后要添加/修改单词，只需编辑 `vocab.json`，不用改 Python 脚本。

---

## 六、第 3 部分：函数 get_options() —— 生成 4 个选项

```python
def get_options(correct_meaning, all_meanings, n=4):
    """生成4个选项：1个正确答案 + 3个干扰项"""
    distractors = [m for m in all_meanings if m != correct_meaning]
    selected = random.sample(distractors, min(3, len(distractors)))
    options = selected + [correct_meaning]
    random.shuffle(options)
    return options
```

**作用**：给一道题准备 4 个中文选项。

用 BASIC 思维理解：

```
SUB get_options(correct$, all_meanings$())
    ' 1. 找出所有「不是正确答案」的释义，放进干扰项数组
    ' 2. 从干扰项里随机抽 3 个
    ' 3. 把正确答案也加进去，变成 4 个
    ' 4. 把这 4 个顺序打乱
    ' 5. 返回这 4 个选项
END SUB
```

- `distractors = [m for m in all_meanings if m != correct_meaning]`  
  列表推导：遍历所有释义，只留下不等于正确答案的。  
  相当于 BASIC 的循环 + IF 判断。

- `random.sample(..., 3)`  
  随机抽出 3 个不重复的元素（像 `RND` 抽签）。

- `random.shuffle(options)`  
  把列表顺序打乱，防止正确答案总在同一个位置。

---

## 七、第 4 部分：函数 init_quiz() —— 初始化一轮测验

```python
def init_quiz():
    """初始化一组10个单词的测验"""
    words = list(VOCAB.keys())
    selected = random.sample(words, 10)
    st.session_state.quiz_words = selected
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answers = []  # 记录每题对错
    st.session_state.finished = False
    st.session_state.started = True

    # 清除上一轮留下的选项缓存和单选状态，防止选项与单词不匹配
    keys_to_delete = [k for k in st.session_state.keys()
                      if k.startswith("options_") or k.startswith("choice_")]
    for k in keys_to_delete:
        del st.session_state[k]
```

**作用**：开始新的一组 10 题。

对应 BASIC：

```
SUB init_quiz
    ' 从所有单词里随机抽 10 个，存到 quiz_words 数组
    ' 当前题号 = 0
    ' 得分 = 0
    ' 清空答题记录
    ' 标记：测验已开始，还没结束
    ' 重要：清除上一轮留下的选项缓存（options_xxx）和单选状态（choice_xxx）
    '      否则「再来一组」后会出现选项和单词对不上的 bug
END SUB
```

`st.session_state` 就像 BASIC 里的**全局变量**或**公共变量**，网页刷新后数据还在。

> **特别注意（已修复的问题）**：  
> 如果不清除旧的 `options_xxx` 缓存，点「再来一组」后，新抽到的单词会错误地使用上一轮的选项列表，导致正确答案根本不在 4 个选项里。现在代码已经在 `init_quiz()` 里主动删除这些旧缓存。

---

## 八、第 5 部分：主函数 main() —— 整个页面的逻辑

这是程序的核心，像 BASIC 的主程序从第 10 行开始往下跑。

### 8.1 设置页面标题和图标

```python
st.set_page_config(
    page_title="高中英语单词小测验",
    page_icon="📚",
    layout="centered"
)
```

设置浏览器标签页的标题和显示方式。

### 8.2 自定义网页样式（CSS）

中间有一大段 `st.markdown(""" <style> ... </style> """, ...)`  
这是给网页加颜色、字体大小、圆角等美化效果，可以暂时忽略，不影响逻辑理解。

### 8.3 显示标题

```python
st.markdown('<p class="main-title">📚 高中英语单词小测验</p>', ...)
st.markdown('<p class="subtitle">每组 10 个单词，选出正确的中文意思吧！</p>', ...)
```

相当于 BASIC 的 `PRINT "📚 高中英语单词小测验"`。

### 8.4 初始化 session 状态

```python
if "started" not in st.session_state:
    st.session_state.started = False
    st.session_state.finished = False
```

第一次运行时，给两个标志变量赋初值：  
- `started`：测验是否已经开始  
- `finished`：是否已经做完 10 题

### 8.5 三种主要页面状态（用 IF 判断）

程序根据两个标志，进入三种不同的显示模式：

#### 状态 1：还没开始（欢迎页）

```python
if not st.session_state.started:
    st.info("👋 你好呀小朋友！...")
    if st.button("🚀 开始测验", ...):
        init_quiz()
        st.rerun()
    return
```

- 显示欢迎语。
- 如果用户点了「开始测验」按钮，就调用 `init_quiz()`，然后 `st.rerun()`（重新运行整个程序，进入答题状态）。

#### 状态 2：已经做完 10 题（结果页）

```python
if st.session_state.finished:
    score = st.session_state.score
    total = 10
    percent = int(score / total * 100)
    
    # 显示得分
    # 根据分数高低说不同的鼓励话（IF-ELIF-ELSE）
    # 找出所有做错的题，列出来
    # 如果全对，放气球特效 st.balloons()
    # 提供「再来一组新题」按钮
    return
```

逻辑很清晰：

1. 计算百分比。
2. 用 `if percent == 100`、`elif percent >= 80` 等给出不同评价（像 BASIC 的多分支 IF）。
3. 遍历 `answers` 列表，把做错的收集起来显示。
4. 点「再来一组」就重新 `init_quiz()`。

#### 状态 3：正在答题中

```python
# 取出当前题号和单词
idx = st.session_state.current_idx
word = st.session_state.quiz_words[idx]
correct_meaning = VOCAB[word]
all_meanings = list(VOCAB.values())

# 生成（或取出已缓存的）4 个选项
# 把单词本身也加入 key，彻底避免上一轮残留选项导致错位
option_key = f"options_{idx}_{word}"
if option_key not in st.session_state:
    st.session_state[option_key] = get_options(correct_meaning, all_meanings)
options = st.session_state[option_key]

# 显示进度条
st.progress((idx) / 10, text=f"第 {idx + 1} / 10 题")

# 大字显示英文单词
st.markdown(f'<div class="word-display">{word}</div>', ...)

# 显示 4 个单选按钮（key 也带上单词，防止串号）
choice = st.radio("选项", options, key=f"choice_{idx}_{word}", ...)

# 两个按钮并排
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("提交答案", ...):
        is_correct = (choice == correct_meaning)
        if is_correct:
            st.session_state.score += 1
        st.session_state.answers.append((word, correct_meaning, choice, is_correct))
        
        if idx + 1 >= 10:
            st.session_state.finished = True   # 做完了
        else:
            st.session_state.current_idx += 1  # 下一题
        st.rerun()

with col2:
    if st.button("跳过本题", ...):
        # 把本题记为错误，然后跳到下一题或结束
        ...
```

**关键点解释：**

1. **当前题号 `idx`**  
   从 0 开始，每做完一题就 `+1`，到 9 就结束。

2. **选项缓存**  
   因为每次点击按钮程序都会重新运行，如果不把选项存起来，每次刷新选项顺序都会变。  
   所以用 `st.session_state[f"options_{idx}_{word}"]` 把这一题的选项记住（key 里带上单词，更安全）。  
   同时，在 `init_quiz()` 里会主动清除上一轮的所有 `options_xxx` 和 `choice_xxx`，避免「再来一组」后选项和单词对不上。

3. **`st.radio`**  
   显示单选按钮组，用户选一个后，`choice` 变量就拿到选中的文字。

4. **提交答案时的判断**  
   ```python
   is_correct = (choice == correct_meaning)   # 对不对？
   if is_correct:
       st.session_state.score += 1            # 得分 +1
   ```
   然后把本题的详细信息（单词、正确答案、你的选择、是否正确）存进 `answers` 列表，方便最后回顾。

5. **`st.rerun()`**  
   强制让程序重新跑一遍 `main()`，这样页面就会显示下一题或结果页。

---

## 九、程序入口

```python
if __name__ == "__main__":
    main()
```

这是 Python 的标准写法，意思是：「如果这个文件是被直接运行的（而不是被其他程序导入的），就执行 `main()`」。

相当于 BASIC 里最后一行的 `RUN` 或者主程序开始。

---

## 十、数据是怎么流动的？（用 BASIC 风格总结）

```
程序启动
    ↓
检查 started 标志
    ↓
【还没开始】→ 显示欢迎页 → 点「开始」→ 调用 init_quiz → 设 started=True → 重新运行
    ↓
【已开始且没结束】→ 显示第 idx 题 → 用户选择 → 点「提交」
        → 判断对错，更新 score 和 answers
        → idx = idx + 1
        → 如果 idx >= 10，设 finished=True
        → 重新运行
    ↓
【finished=True】→ 显示得分和错题 → 点「再来一组」→ 重新 init_quiz
```

所有重要状态都保存在 `st.session_state` 里，所以即使页面刷新，数据也不会丢。

---

## 十一、如何运行这个程序？

1. 确保安装了 Streamlit：
   ```bash
   pip install streamlit
   ```

2. 在命令行进入文件所在目录，运行：
   ```bash
   streamlit run vocab_quiz.py
   ```

3. 浏览器会自动打开一个网页，就可以开始测验了。

---

## 十二、总结（给 BASIC 学习者的一句话）

这个程序的核心逻辑其实很简单：

> **用一个大字典当题库 → 随机抽 10 个单词 → 循环显示题目并收答案 → 最后算分并显示错题。**

只是它把「屏幕输出」和「用户输入」都变成了网页上的按钮、单选框和文字，并且用 `session_state` 来记住当前进度。  
只要你理解 BASIC 里的变量、数组、IF 判断和子程序，就能看懂这个 Python 程序的绝大部分逻辑。

---

如果你对某一段代码还有疑问，可以指出具体行号或功能，我再单独解释。
