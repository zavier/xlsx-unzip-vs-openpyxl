"""构造一张仿真的季度销售表：3 个 sheet、合并单元格、日期、货币格式、公式。"""
import datetime as dt
import random

from openpyxl import Workbook
from openpyxl.styles import Alignment

random.seed(7)
wb = Workbook()

# sheet 1：明细，约 1100 行
ws = wb.active
ws.title = "明细"
ws.merge_cells("A1:E1")
ws["A1"] = "2025 Q3 销售明细"
ws["A1"].alignment = Alignment(horizontal="center")
ws.append([])  # 第 2 行留空
ws.append(["分公司", "产品", "日期", "金额", "备注"])  # 第 3 行表头
branches = ["华北", "华东", "华南", "西南", "东北"]
start = dt.date(2025, 7, 1)
for i in range(1100):
    d = start + dt.timedelta(days=i % 92)
    ws.append([branches[i % 5], f"P{i % 17:02d}", d, round(random.uniform(100, 9000), 2), None])
for r in range(4, 1104):
    ws[f"C{r}"].number_format = "yyyy-mm-dd"
    ws[f"D{r}"].number_format = "$#,##0.00"
# 第 4 行正好是 2025-07-15 附近的日期，保证题目 C4 可以对上
ws["C4"] = dt.date(2025, 7, 15)
ws["D4"].number_format = "$#,##0.00"
# 第 9 行放一个公式
ws["D9"] = "=SUM(D4:D8)"
ws["D9"].number_format = "$#,##0.00"

# sheet 2：汇总，放一个日期
ws2 = wb.create_sheet("汇总")
ws2["A1"] = "汇总"
ws2["B3"] = dt.date(2025, 9, 30)
ws2["B3"].number_format = "yyyy-mm-dd"

# sheet 3：区域拆分
ws3 = wb.create_sheet("区域")
ws3["A1"] = "区域"

wb.save("/tmp/xlsx-repro/sales.xlsx")
print("saved")
