#!/usr/bin/env python3
# 第一个 第 17 天 06:20 拷来给种树网页版用（原：第二个 第 17 天 05:20 给"只看网页"的生人玩雁阵网页版）。照 页11 的 看页.py 改：键不是方向键，是网页上按钮上的字。
# 每回把记录里攒的点法从头重放，再点这回给的，整页截成 屏.png。沙箱里起不了浏览器，所以只写 要.txt，由外面的 点页服.py 截图。
# 用法：python3 点页.py 记录.txt "按钮上的字" ["按钮上的字" ...]     不给字就是只看现在的画面
import sys, os, time, random
rec = os.path.abspath(sys.argv[1]); new = sys.argv[2:]
old = [x for x in open(rec, encoding='utf-8').read().split('\n') if x] if os.path.exists(rec) else []
d = os.path.dirname(rec); tok = str(random.random())
with open(os.path.join(d, '要.tmp'), 'w', encoding='utf-8') as f: f.write(tok + '\n' + str(len(new)) + '\n' + '\n'.join(old + new))
os.replace(os.path.join(d, '要.tmp'), os.path.join(d, '要.txt'))
ok = os.path.join(d, '好.txt')
for _ in range(240):
    time.sleep(0.5)
    if os.path.exists(ok):
        got = open(ok, encoding='utf-8').read().split('\n')
        if got[0].strip() == tok:
            bad = got[1].strip() if len(got) > 1 else ''
            if bad:
                print('没点成：画面上没有写着"' + bad + '"的按钮（这一下和它后面的都没算）。画面在 ' + os.path.join(d, '屏.png') + '，看清按钮上的字再点。'); sys.exit(1)
            with open(rec, 'w', encoding='utf-8') as f: f.write('\n'.join(old + new) + '\n')
            print('画面在 ' + os.path.join(d, '屏.png') + '（打开这张图看）。这回点了：' + (' / '.join(new) or '（没点）') + '；一共点过 ' + str(len(old + new)) + ' 下。'); sys.exit(0)
print('等了两分钟没出画面，再调一次试试。'); sys.exit(1)
