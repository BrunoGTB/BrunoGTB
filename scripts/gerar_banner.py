import math, random
random.seed(7)
W,H=36,42
P={'K':'#07040b','H':'#2a1816','h':'#4b2c27','S':'#c9775a','s':'#a35a45','L':'#e3a07f','G':'#121018',
   'W':'#f3ecff','E':'#140c16','M':'#2a1816','m':'#9c4f4a','p':'#d9d9e6','B':'#1a1420','b':'#2c2336',
   'V':'#8b5cf6','v':'#5b2f86','X':'#c4a5ff','n':'#d6967a'}
g=[[None]*W for _ in range(H)]
def put(x,y,c):
    if 0<=x<W and 0<=y<H: g[y][x]=c
# hair
for y in range(H):
    for x in range(W):
        if ((x-18)/15.5)**2+((y-12.5)/11.5)**2<=1 and y<=20: put(x,y,'H')
# curl bumps on the outline of hair
for cx,cy in [(5,9),(8,4),(13,1.5),(19,1),(25,2.5),(30,6),(32,11),(4,14),(32,16),(3,18)]:
    for y in range(H):
        for x in range(W):
            if (x-cx)**2+(y-cy)**2<=4.5: put(x,y,'H')
# face
for y in range(14,H):
    for x in range(W):
        if ((x-18)/10.5)**2+((y-22.5)/9.5)**2<=1: put(x,y,'S')
# fringe curls over forehead
for x,y in [(9,15),(10,15),(10,16),(13,15),(14,15),(14,16),(17,15),(18,15),(21,15),(22,15),(22,16),(25,15),(26,15),(26,16),(27,17),(9,17)]:
    put(x,y,'H')
# hair curl highlights
for y in range(H):
    for x in range(W):
        if g[y][x]=='H' and y<17 and ((x*5+y*3)%7==0 or (x*3+y*7)%11==0): g[y][x]='h'
# ear + earring
for x,y in [(29,21),(29,22),(29,23),(30,22),(30,23),(29,24)]: put(x,y,'S')
put(30,25,'p'); put(31,25,'p'); put(31,24,'p')
# face shading
for y in range(14,H):
    for x in range(W):
        if g[y][x]=='S':
            if x>=24 and ((x-18)/10.5)**2+((y-22.5)/9.5)**2>0.55: g[y][x]='s'
            elif x<=12 and y<=24 and ((x-18)/10.5)**2+((y-22.5)/9.5)**2>0.6: g[y][x]='L'
# eyebrows + piercing
for x in range(10,16): put(x,18,'H')
for x in range(21,27): put(x,18,'H')
put(11,17,'H');put(25,17,'H')
put(23,16,'p');put(24,17,'p')
# glasses
for cx in (13,23):
    for y in range(17,28):
        for x in range(W):
            d=math.hypot(x-cx,y-22)
            if 2.9<=d<3.9: put(x,y,'G')
            elif d<2.9 and g[y][x] in ('S','s','L'): g[y][x]='n'
    put(cx,22,'E');put(cx-1,22,'E');put(cx,23,'E');put(cx-1,23,'E')
    put(cx-2,20,'W');put(cx-1,20,'W') if False else None
    put(cx-2,21,'W'); put(cx-1,20,'W')
for x in (17,18,19): put(x,21,'G')
for x in range(27,30): put(x,21,'G')
# nose
put(18,25,'s');put(19,26,'s');put(18,26,'s')
# mustache, mouth, goatee
for x in range(14,23): put(x,27,'M')
put(13,28,'M');put(14,28,'M');put(22,28,'M');put(23,28,'M')
for x in range(16,21): put(x,29,'m')
for x in (16,18,20): put(x,30,'M')
for x in (17,18,19): put(x,31,'M')
for x,y in [(12,30),(14,31),(21,31),(23,30),(13,29),(24,29),(15,32),(20,32)]:
    if g[y][x] in ('S','s'): g[y][x]='s'
# body / sweater
for y in range(32,H):
    half=6+min(y-32,4)*1.4
    for x in range(W):
        if abs(x+0.5-18)<=half: put(x,y,'B')
for x in range(14,23): put(x,32,'b')
for x in range(13,24,2): put(x,33,'b')
# laptop (back of lid) held in front
for y in range(35,H):
    for x in range(10,27): put(x,y,'v')
for x in range(10,27): put(x,35,'V')
for y in range(35,H): put(10,y,'V'); put(26,y,'V')
# </> on lid
for x,y in [(14,38),(13,39),(14,40),(18,37),(18,38),(17,39),(17,40),(16,41) if False else (17,41),(22,38),(23,39),(22,40)]:
    put(x,y,'X')
# hands
for x,y in [(9,37),(9,38),(8,38),(27,37),(27,38),(28,38)]: put(x,y,'S')
# outline
filled={(x,y) for y in range(H) for x in range(W) if g[y][x]}
for y in range(H):
    for x in range(W):
        if g[y][x] is None and any((x+dx,y+dy) in filled for dx,dy in((1,0),(-1,0),(0,1),(0,-1))): g[y][x]='K'

def runs(grid,s,ox,oy):
    out=[]
    for y,row in enumerate(grid):
        x=0
        while x<len(row):
            c=row[x]
            if c is None: x+=1; continue
            x2=x
            while x2+1<len(row) and row[x2+1]==c: x2+=1
            out.append(f'<rect x="{ox+x*s}" y="{oy+y*s}" width="{(x2-x+1)*s}" height="{s}" fill="{P[c]}"/>')
            x=x2+1
    return '\n'.join(out)

FONT={'B':["11110","10001","10001","11110","10001","10001","11110"],'R':["11110","10001","10001","11110","10100","10010","10001"],
'U':["10001"]*6+["01110"],'N':["10001","11001","10101","10011","10001","10001","10001"],'O':["01110"]+["10001"]*5+["01110"],
'C':["01111"]+["10000"]*5+["01111"],'S':["01111","10000","10000","01110","00001","00001","11110"],'T':["11111"]+["00100"]*6,
'D':["11110"]+["10001"]*5+["11110"],'I':["11111"]+["00100"]*5+["11111"],' ':["00000"]*7}
def pixtext(txt,x0,y0,s,fill):
    out=[];x=x0
    for ch in txt:
        base='O' if ch=='Ó' else ch
        for r,row in enumerate(FONT[base]):
            for c,bit in enumerate(row):
                if bit=='1': out.append(f'<rect x="{x+c*s}" y="{y0+r*s}" width="{s}" height="{s}" fill="{fill}"/>')
        if ch=='Ó':
            out.append(f'<rect x="{x+3*s}" y="{y0-3*s}" width="{s}" height="{s}" fill="{fill}"/><rect x="{x+2*s}" y="{y0-2*s}" width="{s}" height="{s}" fill="{fill}"/>')
        x+=6*s
    return '\n'.join(out)

import base64
from PIL import Image as _Img
_av=_Img.open('assets/avatar.png')
AV_W=round(222*_av.width/_av.height)
AVATAR=base64.b64encode(open('assets/avatar.png','rb').read()).decode()
BW,BH=900,260
parts=[]
# bricks
bricks=[]
for row in range(0,9):
    y=row*24; off=-24 if row%2 else 0
    for col in range(-1,20):
        x=col*48+off
        r=random.random()
        c='#1b1124' if r<0.18 else ('#120a18' if r<0.35 else '#160d1d')
        bricks.append(f'<rect x="{x+2}" y="{y+2}" width="44" height="20" fill="{c}"/><rect x="{x+2}" y="{y+2}" width="44" height="2" fill="#21152b"/>')
        if random.random()<0.06:
            bricks.append(f'<rect x="{x+14}" y="{y+8}" width="2" height="4" fill="#0b0710"/><rect x="{x+16}" y="{y+12}" width="2" height="4" fill="#0b0710"/><rect x="{x+18}" y="{y+16}" width="2" height="4" fill="#0b0710"/>')
floor=[]
for col in range(0,19):
    floor.append(f'<rect x="{col*50+2}" y="214" width="46" height="44" fill="#100914"/><rect x="{col*50+2}" y="214" width="46" height="3" fill="#1d1226"/>')
def torch(x):
    return f'''<g shape-rendering="crispEdges">
  <rect x="{x-6}" y="118" width="12" height="6" fill="#2c2336"/><rect x="{x-3}" y="124" width="6" height="14" fill="#2c2336"/>
  <g class="chama" style="transform-origin:{x}px 116px">
    <rect x="{x-6}" y="100" width="12" height="18" fill="#612c7f"/><rect x="{x-3}" y="94" width="6" height="22" fill="#8b5cf6"/><rect x="{x-3}" y="106" width="6" height="8" fill="#c4a5ff"/>
  </g></g>
  <circle cx="{x}" cy="108" r="60" fill="url(#luz)"/>'''
def plus(x,y,s,d):
    return f'<g class="brilho" style="animation-delay:{d}s" fill="#a274ff"><rect x="{x}" y="{y-s}" width="{s}" height="{3*s}"/><rect x="{x-s}" y="{y}" width="{3*s}" height="{s}"/></g>'
monitor=''.join(f'<rect x="{808+x*4}" y="{62+y*4}" width="4" height="4" fill="#8b5cf6"/>' for y,row in enumerate(["1111111","1000001","1000001","1000001","1111111","0001000","0011100"]) for x,b in enumerate(row) if b=='1')
code=''.join(f'<rect x="{x*4}" y="{y*4}" width="4" height="4" fill="#8b5cf6"/>' for y,row in enumerate(["00100010100","01000010010","10000100001","01001000010","00101000100"]) for x,b in enumerate(row) if b=='1')
svg=f'''<svg xmlns="http://www.w3.org/2000/svg" width="{BW}" height="{BH}" viewBox="0 0 {BW} {BH}" role="img" aria-label="Bruno Custódio — banner em pixel art">
<title>Bruno Custódio</title>
<defs>
  <radialGradient id="luz"><stop offset="0" stop-color="#8b5cf6" stop-opacity=".28"/><stop offset="1" stop-color="#8b5cf6" stop-opacity="0"/></radialGradient>
  <radialGradient id="vinheta" cx=".5" cy=".55" r=".75"><stop offset=".45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".85"/></radialGradient>
  <clipPath id="borda"><rect width="{BW}" height="{BH}" rx="14"/></clipPath>
</defs>
<style>
  .heroi {{ animation: flutua 2.4s ease-in-out infinite; }}
  @keyframes flutua {{ 50% {{ transform: translateY(-5px); }} }}
  .chama {{ animation: tremula .35s steps(2) infinite alternate; }}
  @keyframes tremula {{ to {{ transform: scaleY(.82) scaleX(1.12); }} }}
  .brilho {{ animation: pisca 2.2s steps(3) infinite; }}
  @keyframes pisca {{ 50% {{ opacity: .15; }} }}
  .icone {{ animation: flutua 3s ease-in-out infinite; }}
  text {{ font-family: 'JetBrains Mono', 'Fira Code', Consolas, monospace; }}
</style>
<g clip-path="url(#borda)" shape-rendering="crispEdges">
  <rect width="{BW}" height="{BH}" fill="#0b0710"/>
  {''.join(bricks)}
  <rect y="210" width="{BW}" height="50" fill="#0b0710"/>
  {''.join(floor)}
  {torch(330)}
  {torch(860)}
  <ellipse cx="690" cy="238" rx="78" ry="10" fill="#000" opacity=".6"/>
  <circle cx="690" cy="150" r="120" fill="url(#luz)"/>
  <g class="heroi">
    <image href="data:image/png;base64,{AVATAR}" x="585" y="12" width="{AV_W}" height="222"/>
  </g>
  <g class="icone" style="animation-delay:.6s">{monitor}</g>
  <g transform="translate(528 96)"><g class="icone" style="animation-delay:1.2s">{code}</g></g>
  {plus(560,40,4,0)}{plus(840,36,4,.7)}{plus(800,170,3,1.3)}{plus(512,180,3,.4)}{plus(300,40,3,1.1)}
  <rect width="{BW}" height="{BH}" fill="url(#vinheta)"/>
  <g>
{pixtext("BRUNO",48,48,7,"#612c7f")}
{pixtext("BRUNO",44,44,7,"#ece6f5")}
{pixtext("CUSTÓDIO",48,132,7,"#612c7f")}
{pixtext("CUSTÓDIO",44,128,7,"#a274ff")}
  </g>
</g>
<rect x="1" y="1" width="{BW-2}" height="{BH-2}" rx="14" fill="none" stroke="#341d3c" stroke-width="2"/>
</svg>'''
open('assets/banner.svg','w').write(svg)
print(len(svg))
