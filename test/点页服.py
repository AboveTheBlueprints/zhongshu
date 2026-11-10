#!/usr/bin/env python3
# 第一个 第 17 天 06:20 从第二个雁阵那份拷来，种树网页版用：每棵苗底下都有一样的四个按钮，所以'3号 浇'这种写法点 3 号底下那个。
# 原注：第二个 第 17 天 05:20：替 点页.py 截图（雁阵网页版）。照 页11 的 看页服.py 改：按按钮上的字点。
# 用法（后台跑）：python3 点页服.py 目录1 目录2 ...   每个目录里有 页/index.html。40 分钟没动静自己停。
import sys, os, asyncio, time
from playwright.async_api import async_playwright
dirs = [os.path.abspath(x) for x in sys.argv[1:]]
async def render(b, d):
    req = open(os.path.join(d, '要.txt'), encoding='utf-8').read().split('\n')
    tok, nnew, keys = req[0], int(req[1]), [x for x in req[2:] if x]
    pg = await b.new_page(viewport={'width': 900, 'height': 900})
    await pg.goto('file://' + os.path.join(d, '页', 'index.html')); await pg.wait_for_timeout(300)
    bad = ''
    for k in keys:
        k2 = k.strip().replace('　', ' ')
        exact = None
        import re
        m = re.match(r'^(\d+)\s*号\s*(.+)$', k2)
        if m:
            loc = pg.locator('#yard .plot').nth(int(m.group(1)) - 1).locator('button')
            if int(m.group(1)) >= 1 and int(m.group(1)) <= await pg.locator('#yard .plot').count():
                for i in range(await loc.count()):
                    if (await loc.nth(i).inner_text()).strip() == m.group(2).strip(): exact = loc.nth(i); break
        else:
            loc = pg.locator('button')
            for i in range(await loc.count()):
                if (await loc.nth(i).inner_text()).strip() == k2: exact = loc.nth(i); break
        if exact is not None and await exact.is_disabled(): exact = None
        if exact is None: bad = k; break
        await exact.click(); await pg.wait_for_timeout(60)
    await pg.wait_for_timeout(300)
    await pg.screenshot(path=os.path.join(d, '屏.png'), full_page=True)
    await pg.close()
    os.remove(os.path.join(d, '要.txt'))
    with open(os.path.join(d, '好.txt'), 'w', encoding='utf-8') as f: f.write(tok + '\n' + bad)
    print(time.strftime('%H:%M:%S'), os.path.basename(d), len(keys), bad, flush=True)
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(); last = time.time()
        while time.time() - last < 2400:
            for d in dirs:
                if os.path.exists(os.path.join(d, '要.txt')):
                    try: await render(b, d)
                    except Exception as e: print('出错', d, e, flush=True)
                    last = time.time()
            await asyncio.sleep(0.3)
        await b.close()
asyncio.run(main())
