from pathlib import Path
import cairosvg
from PIL import Image, ImageEnhance, ImageFilter
import random, math

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'assets'/'source'
PRE=ROOT/'assets'/'previews'
SRC.mkdir(parents=True,exist_ok=True); PRE.mkdir(parents=True,exist_ok=True)
W,H=2048,1365

def distress_layer(seed=1775, opacity=.18):
    r=random.Random(seed)
    elems=[]
    for _ in range(90):
        x=r.randint(10,W-10); y=r.randint(10,H-10); rx=r.randint(8,100); ry=r.randint(3,40)
        a=r.uniform(.03,opacity)
        elems.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="#3a2c1a" opacity="{a:.3f}" transform="rotate({r.randint(0,179)} {x} {y})"/>')
    for _ in range(25):
        x=r.randint(20,W-20); y=r.randint(20,H-20); rw=r.randint(5,45); rh=r.randint(2,12)
        a=r.uniform(.05,.22)
        elems.append(f'<rect x="{x}" y="{y}" width="{rw}" height="{rh}" fill="#fff5b0" opacity="{a:.3f}" transform="rotate({r.randint(0,179)} {x} {y})"/>')
    return '\n'.join(elems)

def worn_mask(seed=44):
    r=random.Random(seed)
    holes=[]
    for side in ('l','r','t','b'):
        for _ in range(12):
            if side in ('l','r'):
                x=0 if side=='l' else W; y=r.randint(0,H); rx=r.randint(8,55); ry=r.randint(8,90)
            else:
                y=0 if side=='t' else H; x=r.randint(0,W); rx=r.randint(8,90); ry=r.randint(8,55)
            holes.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="black"/>')
    for _ in range(38):
        x=r.randint(80,W-80); y=r.randint(80,H-80); rx=r.randint(2,16); ry=r.randint(2,11)
        holes.append(f'<ellipse cx="{x}" cy="{y}" rx="{rx}" ry="{ry}" fill="black" transform="rotate({r.randint(0,179)} {x} {y})"/>')
    return '<mask id="wear"><rect width="100%" height="100%" fill="white"/>'+''.join(holes)+'</mask>'

def modern_svg(worn=False):
    mask = worn_mask(2026) if worn else ''
    maskattr=' mask="url(#wear)"' if worn else ''
    grime=distress_layer(2026, .15 if worn else .06)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{mask}</defs>
<g{maskattr}>
<rect width="{W}" height="{H}" fill="#e5c200"/>
<rect width="{W}" height="{H}" fill="#fff04a" opacity=".20"/>
{grime}
<path d="M430 910 C540 850 660 870 760 895 C860 852 1000 865 1105 905 C1210 855 1360 872 1560 930 C1440 948 1325 950 1190 942 C1040 965 870 960 690 944 C585 952 505 945 430 910Z" fill="#15371e" opacity=".90"/>
<path d="M560 780 C575 650 765 590 1010 605 C1255 620 1455 700 1445 825 C1435 948 1245 1004 1018 984 C790 965 545 900 560 780Z" fill="#171717" stroke="#080808" stroke-width="26"/>
<path d="M700 790 C750 700 900 675 1035 690 C1170 705 1288 752 1305 815 C1322 884 1225 918 1075 914 C925 910 770 875 700 790Z" fill="#dfc900"/>
<path d="M690 610 C706 490 880 442 1085 455 C1284 468 1402 535 1389 637 C1376 744 1218 778 1040 758 C858 738 675 704 690 610Z" fill="#171717" stroke="#080808" stroke-width="24"/>
<path d="M812 602 C850 530 958 516 1075 526 C1198 536 1270 568 1284 620 C1297 670 1207 694 1093 687 C978 681 862 656 812 602Z" fill="#dfc900"/>
<path d="M798 445 C810 351 930 309 1088 322 C1245 335 1332 394 1318 476 C1304 559 1196 585 1062 569 C927 553 785 522 798 445Z" fill="#171717" stroke="#080808" stroke-width="22"/>
<path d="M904 438 C933 385 1008 376 1092 385 C1180 394 1229 417 1238 455 C1246 493 1184 506 1101 498 C1015 491 941 470 904 438Z" fill="#dfc900"/>
<path d="M1040 365 C1010 292 1022 219 1090 160 C1145 113 1212 93 1278 73 C1260 112 1228 135 1198 154 C1262 145 1319 127 1368 107 C1329 157 1280 184 1215 204 C1260 213 1293 236 1309 264 C1266 257 1228 258 1202 276 C1188 286 1182 315 1173 345 C1160 388 1122 405 1086 400 C1064 397 1050 382 1040 365Z" fill="#171717" stroke="#080808" stroke-width="18"/>
<path d="M1276 150 L1372 128 L1287 181Z" fill="#171717"/>
<circle cx="1222" cy="183" r="9" fill="#dfc900"/>
<path d="M1430 825 C1540 812 1640 770 1697 713 C1715 696 1736 698 1742 715 C1748 734 1731 751 1714 765 C1635 834 1542 866 1433 878Z" fill="#171717"/>
<g fill="none" stroke="#d9bd00" stroke-width="9" opacity=".85">
<path d="M620 760 L735 660 L855 782 L730 902Z M790 650 L910 580 L1022 700 L914 790Z M990 618 L1112 594 L1210 708 L1088 785Z M1185 654 L1310 700 L1380 816 L1254 817Z"/>
<path d="M742 566 L846 480 L952 592 L850 690Z M930 468 L1040 435 L1135 540 L1030 620Z M1120 462 L1221 475 L1310 570 L1194 650Z"/>
<path d="M845 405 L940 335 L1033 428 L938 523Z M1020 332 L1115 330 L1203 410 L1107 492Z"/>
</g>
<g fill="#f0d64a" opacity=".9"><ellipse cx="1038" cy="771" rx="260" ry="45"/><ellipse cx="1054" cy="591" rx="190" ry="34"/><ellipse cx="1053" cy="440" rx="128" ry="26"/></g>
<g fill="none" stroke="#111" stroke-width="18" opacity=".95"><ellipse cx="1030" cy="800" rx="394" ry="166"/><ellipse cx="1040" cy="616" rx="310" ry="139"/><ellipse cx="1053" cy="446" rx="246" ry="110"/></g>
<text x="1024" y="1200" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="158" font-weight="700" letter-spacing="8" fill="#111">DON'T TREAD ON ME</text>
</g></svg>'''

def historical_svg(worn=False):
    mask = worn_mask(1775) if worn else ''
    maskattr=' mask="url(#wear)"' if worn else ''
    grime=distress_layer(1775, .18 if worn else .07)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
<defs>{mask}</defs>
<g{maskattr}>
<rect width="{W}" height="{H}" fill="#e0b82c"/>
<rect width="{W}" height="{H}" fill="#fff0a0" opacity=".14"/>
{grime}
<path d="M525 760 C550 615 755 536 1010 548 C1255 560 1460 640 1488 760 C1512 865 1380 942 1165 947 C934 952 705 900 590 830 C544 802 516 784 525 760Z" fill="#a35b1d" stroke="#5e2b16" stroke-width="28"/>
<path d="M710 775 C770 667 915 632 1065 643 C1215 654 1334 700 1356 774 C1373 830 1288 863 1150 864 C1002 865 832 834 710 775Z" fill="#e0b82c" stroke="#5e2b16" stroke-width="18"/>
<path d="M1000 626 C977 545 980 470 1018 405 C1062 328 1142 257 1246 198 C1301 166 1360 150 1428 143 C1390 181 1355 203 1320 220 C1374 214 1428 216 1484 228 C1440 247 1397 257 1353 262 C1396 284 1426 313 1439 348 C1398 332 1364 329 1334 340 C1301 352 1288 378 1276 410 C1254 469 1230 525 1195 576 C1155 635 1086 665 1033 650 C1018 646 1007 638 1000 626Z" fill="#a35b1d" stroke="#5e2b16" stroke-width="24"/>
<path d="M1470 800 C1573 803 1667 783 1746 744 C1786 724 1820 733 1834 760 C1845 783 1822 806 1782 820 C1689 854 1587 864 1470 850Z" fill="#a35b1d" stroke="#5e2b16" stroke-width="20"/>
<g fill="#f1dfad" stroke="#6b3a18" stroke-width="8"><path d="M1768 746 l45 -16 25 30 -34 32 -44 -14z"/><path d="M1812 732 l40 -10 24 28 -28 30 -37 -12z"/></g>
<circle cx="1360" cy="268" r="10" fill="#2b140d"/>
<g stroke="#633015" stroke-width="9" opacity=".78" fill="none">
<path d="M590 720 L760 900 M690 630 L920 930 M820 570 L1090 945 M980 555 L1245 936 M1140 572 L1392 900 M1288 616 L1470 840"/>
<path d="M630 900 L820 600 M800 932 L1000 557 M990 944 L1165 570 M1170 936 L1320 610 M1330 900 L1435 680"/>
<path d="M1030 576 L1220 300 M1082 626 L1305 235 M1140 610 L1390 205"/>
</g>
<path d="M585 910 C710 850 810 892 908 908 C1055 880 1230 893 1458 923 C1280 955 1097 963 902 946 C780 958 670 946 585 910Z" fill="#315a2d"/>
<text x="1024" y="1200" text-anchor="middle" font-family="Georgia, 'Times New Roman', serif" font-size="150" font-variant="small-caps" font-weight="700" letter-spacing="5" fill="#25150e">DON’T TREAD ON ME</text>
</g></svg>'''

variants={
 'historical-original': historical_svg(False),
 'historical-worn': historical_svg(True),
 'modern-clean': modern_svg(False),
 'modern-worn': modern_svg(True),
}
for name,svg in variants.items():
    (SRC/f'{name}.svg').write_text(svg,encoding='utf-8')
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(PRE/f'{name}.png'),output_width=2048,output_height=1365)
    cairosvg.svg2png(bytestring=svg.encode(),write_to=str(SRC/f'{name}-4096.png'),output_width=4096,output_height=2730)
print('generated',len(variants),'variants')
