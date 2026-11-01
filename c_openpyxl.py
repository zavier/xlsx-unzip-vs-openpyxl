import sys, datetime
from openpyxl import load_workbook

wb = load_workbook(sys.argv[1], data_only=False)
ws, ws2 = wb["明细"], wb["汇总"]
fmt = ws["D4"].number_format
merges = next(iter(ws.merged_cells.ranges))
print("C4日期:", ws["C4"].value.date().isoformat())
print("D4格式:", fmt)
print("B1的值:", "空(合并进A1)" if ws["B1"].value is None else ws["B1"].value)
print("汇总B3日期:", ws2["B3"].value.date().isoformat())
print("D9公式:", ws["D9"].value)
print("合并区:", str(merges).replace("A1:E1", "A1:E1"), "共", merges.max_row * merges.max_col, "个格子")
