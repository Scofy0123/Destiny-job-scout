# opencli BOSS 高阶能力操作手册 (Advanced Commands)

> **注意：配合 `boss-job-scout` 使用，只有在用户明确下达了“打招呼”、“主动沟通”或“发面试邀请”等动作指令时，才允许检索阅读并执行本页操作！请勿在抓取环节主动进行打扰式触达！**

除了 `opencli boss search` 数据侦察抓取外，`opencli boss` 提供了完整的双向触达手段，用以辅助人才转化。以下是所有的命令总览及用法。

## 🤝 简历与沟通
如果你需要与候选人建联、查阅简历与交流，请使用以下命令集合：

```bash
# 查阅：使用这个命令能拉出候选人的完整简历
opencli boss resume <uid>          查看候选人简历

# 约聊起手式：跟打字一样给对方发动破冰
opencli boss greet <uid>           向候选人发招呼

# 海王模式：如果确定了条件，使用这个能群体广播
opencli boss batchgreet            批量发招呼

# 深入沟通：可以带文本继续给通过打招呼的沟通发起后续互动
opencli boss send <uid> <text>     发送消息

# 回顾沉淀：快速拉取对方发来的信息查阅聊天
opencli boss chatmsg <uid>         查看聊天记录
```

## 🧑‍💼 归档沉淀管理
若用户需要流转信息给别人，或者管理自己打出来的鱼塘：

```bash
# 进一步邀约
opencli boss invite <uid>          发面试邀请
opencli boss exchange <uid>        要求交换微信等联系方式

# CRM 标签管理
opencli boss mark <uid>            给候选人打标签，供沉淀筛选

# 我方统筹数据
opencli boss joblist               查看当前正在招聘列表
opencli boss chatlist              返回现存聊天列表
opencli boss stats                 查看全局招聘漏斗统计
```
