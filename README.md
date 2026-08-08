# 高中英语核心词汇测验  
**GaoKao Vocab Quiz**

一个专为中学生设计的**高中英语核心词汇练习小程序**，通过选择题形式帮助快速记忆高考高频单词。

支持手机和电脑浏览器使用，可部署到 Streamlit Community Cloud 免费在线运行。

---

## ✨ 主要功能

- **随机抽题**：从 2600+ 个高考核心词汇中随机抽取 10 个单词
- **四选一**：每个单词给出 4 个中文选项，选择正确意思
- **上一题重做**：答错后可以返回上一题修改，分数会自动调整
- **即时评分**：做完 10 题后显示得分和正确率
- **错题回顾**：自动列出做错的单词及正确答案
- **单词库独立**：词汇存放在 `vocab.json`，方便自行增删改
- **界面友好**：专为小朋友/中学生设计，操作简单

---

## 📁 文件说明

| 文件 | 说明 |
|------|------|
| `vocab_quiz.py` | 主程序（Streamlit 应用） |
| `vocab.json` | 单词库（英文单词 → 中文释义） |
| `requirements.txt` | Python 依赖 |
| `vocab_quiz_说明.md` | 代码详细说明（适合有 BASIC 基础的读者） |
| `README.md` | 本说明文件 |

---

## 🚀 本地运行

1. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

2. 运行程序：
   ```bash
   streamlit run vocab_quiz.py
   ```

3. 浏览器会自动打开，即可开始练习。

---

## ☁️ 部署到 Streamlit Community Cloud（推荐）

1. 把本仓库上传到你的 GitHub（Public 仓库）
2. 打开 [https://share.streamlit.io](https://share.streamlit.io)
3. 用 GitHub 账号登录
4. 点击 **New app**
5. 填写：
   - Repository：选择本仓库
   - Branch：`main`
   - Main file path：`vocab_quiz.py`
6. 点击 **Deploy**

部署成功后会得到一个在线网址，手机和电脑都可以直接访问使用。

---

## 📚 单词库管理

单词存放在 `vocab.json` 中，格式如下：

```json
{
  "abandon": "放弃；遗弃",
  "ability": "能力；才能",
  "congratulate": "祝贺"
}
```

**添加新单词**：直接在 `vocab.json` 中增加键值对即可。  
**删除单词**：删除对应行。  
修改后重新运行或重新部署即可生效。

当前词库包含约 **2600+** 个高考核心高频词汇，覆盖 A–Z。

---

## 🛠️ 技术栈

- Python 3
- Streamlit（网页界面）
- JSON（单词数据存储）

---

## 📖 代码说明

详细的代码逻辑解释（用 BASIC 编程思维对照讲解）请查看：

👉 [vocab_quiz_说明.md](vocab_quiz_说明.md)

---

## 📌 使用建议

- 每天坚持做 2～3 组，效果更好
- 错题可以反复练习，直到熟练
- 家长可陪同孩子一起使用，增加互动

---

## 👨‍💻 开发者

- 昵称：歌呗
- 邮箱：gebeiishandsome@gmail.com

欢迎反馈问题和建议！

---

## 📄 License

本项目仅供学习交流使用，单词释义来源于公开的高考词汇资料整理，欢迎自由修改和分享。

---

**祝你学习进步，高考顺利！** 📚✨
