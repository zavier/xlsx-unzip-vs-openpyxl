# xlsx-unzip-vs-openpyxl

博客《Agent 走的，是它看得见的那条路》（[zhengw-tech.com](https://zhengw-tech.com)）第三节「病例一：它自己解了 zip」的复现代码。

背景：agent 因为 `PATH` 里没有装了 openpyxl 的 python，选择了把 xlsx 当压缩包解开、自己解析 XML 的路。这个仓库把那条路和「用库」放在同一张表上量了一遍。

## 怎么跑

```bash
python3 -m venv .venv
.venv/bin/pip install openpyxl
.venv/bin/python gen.py      # 生成 sales.xlsx（也可直接用仓库里附带的那份，两者一致）
.venv/bin/python check.py    # 跑三条路并判分
```

## 三条路

| 脚本 | 做法 | 行数 | 答对 |
| --- | --- | --- | --- |
| `a_manual.py` | 随手解压读，模拟一个赶时间的 agent | 22 | **1/6** |
| `b_manual.py` | 同样自己解压，认真做到全对 | 76 | 6/6 |
| `c_openpyxl.py` | 用 openpyxl | 13 | **6/6** |

测试表（`sales.xlsx`）：1100 行、3 个 sheet，含合并单元格、日期、货币格式、公式。6 道题见 `check.py` 的 `EXPECTED`。

## 两个值得注意的结果

**A 的错全是静默的。**6 道题只对 1 道，而且对的那道（B1 的值是空）是碰巧——那个格子压根不在文件里。错的输出看起来都像对的：

```text
C4 的日期        期望 2025-07-15   实际 45853      （日期在文件里是个数字）
汇总表 B3 的日期  期望 2025-09-30   实际 45930      （同上）
D4 的货币格式     期望 $#,##0.00    实际 空          （格式存在另一个文件里）
D9 的公式        期望 =SUM(D4:D8)  实际 SUM(D4:D8)  （公式没有开头的等号）
合并区           期望 A1:E1 共 5 格  实际 没看到合并单元格
```

**B 的 76 行是修了四轮才全对的。**四轮分别是：括号笔误、rels 对照表两个属性的顺序看反、路径多拼了一层、格式表的键值写反。四个错没有一个报过异常，全是靠对照期望输出排出来的——这就是手写解析真正的成本：不在跑一次，在跑到对。

## 说明

- `a_manual.py` 按「随手写」的风格原样保留（包括没用到的 import），未做美化；它的行数就是文中引用的行数。
- `gen.py` 用固定随机种子生成测试表，重新生成与仓库附带的 `sales.xlsx` 一致。
- 生成测试表与判分依赖 openpyxl 3.1.5；`a_manual.py`、`b_manual.py` 本身只用标准库。

## License

MIT
