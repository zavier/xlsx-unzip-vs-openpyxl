import re, sys, zipfile, datetime

EPOCH = datetime.date(1899, 12, 30)
z = zipfile.ZipFile(sys.argv[1])

# 1) sheet 名 → 文件：workbook.xml + rels 两层对照
rels = {}
for tag in re.findall(r"<Relationship [^>]*/>", z.read("xl/_rels/workbook.xml.rels").decode()):
    rels[re.search(r'Id="([^"]+)"', tag).group(1)] = re.search(r'Target="([^"]+)"', tag).group(1)
sheets = []
for m in re.finditer(r'<sheet name="([^"]+)"[^>]*r:id="([^"]+)"',
                     z.read("xl/workbook.xml").decode()):
    tgt = rels[m.group(2)]
    sheets.append((m.group(1), tgt.lstrip("/") if tgt.startswith("/") else "xl/" + tgt))

# 2) styles：样式下标 → 数字格式串
styles = z.read("xl/styles.xml").decode()
numfmts = {}
for tag in re.findall(r"<numFmt [^>]*/>", styles):
    numfmts[re.search(r'numFmtId="(\d+)"', tag).group(1)] = \
        re.search(r'formatCode="([^"]*)"', tag).group(1)
xfs = [re.search(r'numFmtId="(\d+)"', x).group(1)
       for x in re.findall(r"<xf [^>]*/?>", styles.split("<cellXfs")[1])]

def fmt_of(s):
    return numfmts.get(xfs[int(s)], "") if s else ""

def as_date(v, fmt):
    if any(k in fmt for k in ("y", "d", "m")):
        return (EPOCH + datetime.timedelta(days=int(v))).isoformat()
    return v

out = {}
for name, path in sheets:
    xml = z.read(path).decode()
    merges = [r for r in re.findall(r'<mergeCell ref="([^"]+)"', xml)]
    for m in re.finditer(r'<c r="([A-Z]+\d+)"(?:[^>]*s="(\d+)")?[^>]*>(.*?)</c>', xml):
        ref, s, inner = m.groups()
        t = re.search(r"<t[^>]*>([^<]*)</t>", inner)
        v = re.search(r"<v>([^<]*)</v>", inner)
        f = re.search(r"<f>([^<]*)</f>", inner)
        fmt = fmt_of(s)
        if f:
            val = "=" + f.group(1)          # 公式在文件里没有等号
        elif t:
            val = t.group(1)
        elif v:
            val = as_date(v.group(1), fmt)  # 日期是个数字，得换算
        else:
            val = ""
        out[(name, ref)] = (val, fmt)
    out[(name, "__merges__")] = merges

def col_row(ref):
    m = re.match(r"([A-Z]+)(\d+)", ref)
    return m.group(1), int(m.group(2))

def g(ref):
    if ("明细", ref) in out:
        return out[("明细", ref)][0]
    c, r = col_row(ref)                     # 不在文件里的格子：看它在不在合并区内
    for mrg in out[("明细", "__merges__")]:
        a, b = mrg.split(":")
        ca, ra = col_row(a); cb, rb = col_row(b)
        if ca <= c <= cb and ra <= r <= rb:
            return "空(合并进" + a + ")"
    return ""

print("C4日期:", g("C4"))
print("D4格式:", out[("明细", "D4")][1] or "常规")
print("B1的值:", g("B1") or "空(合并进A1)")
print("汇总B3日期:", out[("汇总", "B3")][0])
print("D9公式:", g("D9"))
m = out[("明细", "__merges__")][0]
print("合并区:", m, "共", (col_row(m.split(":")[1])[1] - col_row(m)[1] + 1) *
      (ord(col_row(m.split(":")[1])[0]) - ord(col_row(m)[0]) + 1), "个格子")
