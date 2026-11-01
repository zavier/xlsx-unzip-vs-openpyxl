import re, sys, zipfile, tempfile, os

def cells(path):
    z = zipfile.ZipFile(path)
    out = {}
    for name in ("xl/worksheets/sheet1.xml", "xl/worksheets/sheet2.xml"):
        xml = z.read(name).decode("utf-8")
        for m in re.finditer(r'<c r="([A-Z]+\d+)"[^>]*>(.*?)</c>', xml):
            ref, inner = m.group(1), m.group(2)
            t = re.search(r'<t[^>]*>([^<]*)</t>', inner)
            v = re.search(r"<v>([^<]*)</v>", inner)
            f = re.search(r"<f>([^<]*)</f>", inner)
            out[ref] = f.group(1) if f else (t.group(1) if t else (v.group(1) if v else ""))
    return out

d = cells(sys.argv[1])
print("C4日期:", d.get("C4"))
print("D4格式:", "")  # xml 里看不出格式
print("B1的值:", d.get("B1", ""))
print("汇总B3日期:", d.get("B3"))
print("D9公式:", d.get("D9"))
print("合并区:", "没看到合并单元格")
