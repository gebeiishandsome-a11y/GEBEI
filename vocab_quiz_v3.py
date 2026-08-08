import streamlit as st
import random
import json
import os

# 从同目录下的 vocab.json 加载单词库
VOCAB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "vocab.json")

def load_vocab():
    """从外部 JSON 文件加载单词库"""
    try:
        with open(VOCAB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        st.error(f"找不到单词库文件：{VOCAB_FILE}\n请确保 vocab.json 和本脚本在同一目录下。")
        st.stop()
    except json.JSONDecodeError:
        st.error("单词库文件格式错误，请检查 vocab.json 是否为合法 JSON。")
        st.stop()

VOCAB = load_vocab()


def get_options(correct_meaning, all_meanings, n=4):
    """生成4个选项：1个正确答案 + 3个干扰项"""
    distractors = [m for m in all_meanings if m != correct_meaning]
    selected = random.sample(distractors, min(3, len(distractors)))
    options = selected + [correct_meaning]
    random.shuffle(options)
    return options


def init_quiz():
    """初始化一组10个单词的测验"""
    words = list(VOCAB.keys())
    selected = random.sample(words, 10)
    st.session_state.quiz_words = selected
    st.session_state.current_idx = 0
    st.session_state.score = 0
    st.session_state.answers = []  # 记录每题对错 [(word, correct, chosen, is_right), ...]
    st.session_state.finished = False
    st.session_state.started = True

    # 清除上一轮留下的选项缓存和单选状态，防止选项与单词不匹配
    keys_to_delete = [k for k in st.session_state.keys()
                      if k.startswith("options_") or k.startswith("choice_")]
    for k in keys_to_delete:
        del st.session_state[k]


def go_previous():
    """回到上一题，并撤销上一题的得分与记录"""
    if st.session_state.current_idx <= 0:
        return

    # 撤销上一题的记录
    if st.session_state.answers:
        last = st.session_state.answers.pop()  # (word, correct, chosen, is_right)
        if last[3]:  # 如果上一题是对的，扣回分数
            st.session_state.score = max(0, st.session_state.score - 1)

    st.session_state.current_idx -= 1
    st.session_state.finished = False  # 如果从结果页返回，取消结束状态


def main():
    st.set_page_config(
        page_title="高中英语单词小测验",
        page_icon="📚",
        layout="centered"
    )

    # 自定义样式，更适合小朋友
    st.markdown("""
    <style>
    .main-title {
        text-align: center;
        color: #2c3e50;
        font-size: 2.2rem;
        margin-bottom: 0.3rem;
    }
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        font-size: 1.1rem;
        margin-bottom: 1.5rem;
    }
    .word-display {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #2980b9;
        padding: 1.2rem;
        background: linear-gradient(135deg, #e8f4fd, #f0f7ff);
        border-radius: 16px;
        margin: 1rem 0;
        letter-spacing: 2px;
    }
    .score-box {
        text-align: center;
        font-size: 1.8rem;
        padding: 1.5rem;
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
        border-radius: 16px;
        margin: 1rem 0;
    }
    .stRadio > label {
        font-size: 1.15rem !important;
    }
    div[data-testid="stRadio"] > div {
        gap: 0.6rem;
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<p class="main-title">📚 高中英语单词小测验 v1.0</p>', unsafe_allow_html=True)    
    st.markdown('<p class="subtitle">每组 10 个单词，选出正确的中文意思吧！</p>', unsafe_allow_html=True)

    # 初始化 session state
    if "started" not in st.session_state:
        st.session_state.started = False
        st.session_state.finished = False

    if not st.session_state.started:
        st.info("👋 你好呀小朋友！准备好挑战高中英语单词了吗？点击下面的按钮开始吧～")
        st.caption(f"当前单词库共有 {len(VOCAB)} 个单词（来自 vocab.json）")
        if st.button("🚀 开始测验", use_container_width=True, type="primary"):
            init_quiz()
            st.rerun()
        return

    if st.session_state.finished:
        # 结果显示页
        score = st.session_state.score
        total = 10
        percent = int(score / total * 100)

        st.markdown(f'<div class="score-box">🎉 测验完成！<br>你的得分：<b>{score} / {total}</b>（{percent}%）</div>', unsafe_allow_html=True)

        if percent == 100:
            st.success("太棒了！全部正确！你是单词小达人！🌟")
        elif percent >= 80:
            st.success("很优秀！继续保持哦～👍")
        elif percent >= 60:
            st.warning("还不错，再多练习一下会更好！💪")
        else:
            st.error("加油！多记几个单词，下次一定进步！📖")

        # 错题回顾
        wrong = []
        for i, (word, correct, chosen, is_right) in enumerate(st.session_state.answers):
            if not is_right:
                wrong.append((word, correct, chosen))

        if wrong:
            st.subheader("❌ 错题回顾")
            for word, correct, chosen in wrong:
                st.markdown(f"- **{word}**  → 正确答案：**{correct}**（你选了：{chosen}）")
        else:
            st.balloons()

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("⬅️ 返回最后一题修改", use_container_width=True):
                go_previous()
                st.rerun()
        with col_b:
            if st.button("🔄 再来一组新题", use_container_width=True, type="primary"):
                init_quiz()
                st.rerun()
        return

    # 答题进行中
    idx = st.session_state.current_idx
    word = st.session_state.quiz_words[idx]
    correct_meaning = VOCAB[word]
    all_meanings = list(VOCAB.values())

    # 为当前题生成选项（用 session 缓存，避免刷新时选项乱跳）
    # 把单词本身也加入 key，彻底避免上一轮残留选项导致错位
    option_key = f"options_{idx}_{word}"
    if option_key not in st.session_state:
        st.session_state[option_key] = get_options(correct_meaning, all_meanings)

    options = st.session_state[option_key]

    st.progress((idx) / 10, text=f"第 {idx + 1} / 10 题")

    st.markdown(f'<div class="word-display">{word}</div>', unsafe_allow_html=True)
    st.markdown("**请选择这个单词的正确中文意思：**")

    choice = st.radio(
        "选项",
        options,
        key=f"choice_{idx}_{word}",
        label_visibility="collapsed"
    )

    # 三个按钮：上一题 / 提交 / 跳过
    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        # 第一题时禁用「上一题」
        prev_disabled = (idx == 0)
        if st.button("⬅️ 上一题", use_container_width=True, disabled=prev_disabled):
            go_previous()
            st.rerun()

    with col2:
        if st.button("提交答案", use_container_width=True, type="primary"):
            is_correct = (choice == correct_meaning)
            if is_correct:
                st.session_state.score += 1
            st.session_state.answers.append((word, correct_meaning, choice, is_correct))

            if idx + 1 >= 10:
                st.session_state.finished = True
            else:
                st.session_state.current_idx += 1
            st.rerun()

    with col3:
        if st.button("跳过本题", use_container_width=True):
            st.session_state.answers.append((word, correct_meaning, "（跳过）", False))
            if idx + 1 >= 10:
                st.session_state.finished = True
            else:
                st.session_state.current_idx += 1
            st.rerun()

    st.caption("提示：仔细看选项，选出最准确的意思哦～ 点错了可以按「上一题」重做。")


if __name__ == "__main__":
    main()
