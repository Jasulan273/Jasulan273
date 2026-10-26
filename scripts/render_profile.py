from pathlib import Path
import json, math, collections, statistics, html, subprocess
BASE=Path(__file__).resolve().parents[1]
OUT=BASE
result=subprocess.run(['gh','api','graphql','--input',str(BASE/'scripts/profile_query.json')],check=True,capture_output=True,text=True)
data=json.loads(result.stdout)['data']['user']
days=[d for w in data['contributionsCollection']['contributionCalendar']['weeks'] for d in w['contributionDays']]
counts=[d['contributionCount'] for d in days]
total=sum(counts); active=sum(v>0 for v in counts); peak=max(counts)
lang=collections.Counter()
for repo in data['repositories']['nodes']:
 for edge in repo['languages']['edges']: lang[edge['node']['name']]+=edge['size']
size=sum(lang.values()); top=lang.most_common(6); top.append(('Other',size-sum(v for _,v in top)))
shares=[v/size for _,v in top]

BG='#101714'; TILE='#17211b'; EDGE='#2a382f'; TEXT='#eaf0e6'; MUTED='#849b8b'; LIME='#d1f589'
S=[]
def add(s): S.append(s)
def txt(x,y,text,size=14,color=TEXT,weight=400,mono=False,anchor=None,spacing=None):
 attrs=f' text-anchor="{anchor}"' if anchor else ''
 if spacing is not None: attrs+=f' letter-spacing="{spacing}"'
 add(f'<text x="{x}" y="{y}" fill="{color}" font-family="{"monospace" if mono else "Arial,Helvetica,sans-serif"}" font-size="{size}" font-weight="{weight}"{attrs}>{html.escape(str(text))}</text>')
def line(x1,y1,x2,y2,color=EDGE,width=1): add(f'<path d="M{x1} {y1}H{x2}" fill="none" stroke="{color}" stroke-width="{width}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color}" stroke-width="{width}"/>')
def panel(y,h): add(f'<rect x="0.5" y="{y+.5}" width="1199" height="{h-1}" rx="20" fill="{BG}" stroke="{EDGE}"/>')
def section(y,num,title,detail):
 txt(30,y,num,11,LIME,mono=True,spacing=1)
 txt(65,y,title,12,TEXT,mono=True,spacing=2)
 txt(1168,y,detail,10,MUTED,mono=True,anchor='end',spacing=.6)

add('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1200" height="1040" viewBox="0 0 1200 1040" role="img" aria-labelledby="title desc">')
add('<title id="title">Core stack, engineering focus and Pac-Man contribution arcade</title><desc id="desc">Next.js, Node.js, NestJS, Django, React, TypeScript, Python and FastAPI. Engineering focus on web applications, APIs, services and LLM integrations. The Pac-Man board represents actual weekly GitHub contribution totals.</desc>')
add('''<defs><linearGradient id="pulse" x1="0" x2="1"><stop stop-color="#7bb89b"/><stop offset=".55" stop-color="#d1f589"/><stop offset="1" stop-color="#b3c9a5"/></linearGradient><linearGradient id="area" x1="0" x2="0" y1="0" y2="1"><stop stop-color="#d1f589" stop-opacity=".19"/><stop offset="1" stop-color="#d1f589" stop-opacity="0"/></linearGradient><filter id="glow" x="-100%" y="-100%" width="300%" height="300%"><feGaussianBlur stdDeviation="3"/></filter></defs>''')

# 1. Skill cards with quiet connective paths, inspired by Neural Pulse + Swiss Grid.
panel(0,310); section(36,'01','CORE STACK','WEB / API / PYTHON')
line(30,54,1170,54)
skills=[('Next.js','REACT FRAMEWORK','next'),('Node.js','JAVASCRIPT RUNTIME','node'),('NestJS','TYPESCRIPT BACKEND','nest'),('Django','PYTHON FRAMEWORK','django'),('React','USER INTERFACES','react'),('TypeScript','TYPED JAVASCRIPT','ts'),('Python','BACKEND & DATA','python'),('FastAPI','PYTHON APIS','fast')]
for i,(name,sub,kind) in enumerate(skills):
 x=30+(i%4)*288; y=73+(i//4)*112
 if i<4:
  add(f'<path id="wire{i}" d="M{x+136} {y+94}v18" stroke="#5a7f60" stroke-width="1.3"/>')
  add(f'<circle r="2.5" fill="{LIME}"><animateMotion dur="3s" begin="{i*.5}s" repeatCount="indefinite"><mpath xlink:href="#wire{i}"/></animateMotion></circle>')
 add(f'<rect x="{x}" y="{y}" width="272" height="94" rx="12" fill="{TILE}" stroke="{EDGE}"/>')
 add(f'<rect x="{x+16}" y="{y+16}" width="39" height="39" rx="11" fill="#223329"/>')
 # Original vector glyphs; visual marks do not imply skill ratings.
 gx,gy=x+35.5,y+35.5
 if kind=='react':
  for deg in [0,60,120]: add(f'<ellipse cx="{gx}" cy="{gy}" rx="13" ry="5" fill="none" stroke="{LIME}" stroke-width="1.2" transform="rotate({deg} {gx} {gy})"/>')
  add(f'<circle cx="{gx}" cy="{gy}" r="2.2" fill="{LIME}"/>')
 elif kind=='node':
  pts=' '.join(f'{gx+14*math.cos(math.pi/3*j-math.pi/6):.1f},{gy+14*math.sin(math.pi/3*j-math.pi/6):.1f}' for j in range(6))
  add(f'<polygon points="{pts}" fill="none" stroke="{LIME}" stroke-width="1.4"/>'); txt(gx,gy+4,'JS',10,LIME,600,True,'middle')
 elif kind=='fast': add(f'<path d="M{gx+4} {gy-14}l-13 17h9l-3 12 14-19h-9z" fill="{LIME}"/>')
 else:
  glyph={'next':'N','nest':'N','django':'dj','ts':'TS','python':'Py'}[kind]
  txt(gx,gy+6,glyph,18,LIME,700,False,'middle')
  if kind=='next': line(gx+2,gy-5,gx+10,gy+10,LIME,1.5)
 txt(x+70,y+39,name,22,TEXT,600)
 txt(x+17,y+76,sub,9,MUTED,mono=True,spacing=1)

# 2. Bento cards: concrete engineering areas, inspired by GitSkins + DevQuest.
Y=328; panel(Y,325); section(Y+36,'02','ENGINEERING FOCUS','INTERFACES / SERVICES / INTEGRATIONS')
line(30,Y+54,1170,Y+54)
for i in range(3):
 x=30+i*386
 add(f'<rect x="{x}" y="{Y+74}" width="368" height="220" rx="13" fill="{TILE}" stroke="{EDGE}"/>')
 txt(x+22,Y+103,f'0{i+1}',10,LIME,mono=True)

# A small interface wireframe.
x=30
add(f'<rect x="{x+107}" y="{Y+100}" width="145" height="88" rx="8" fill="#101b15" stroke="#526c57"/>')
line(x+107,Y+120,x+252,Y+120,'#526c57')
for i in range(3): add(f'<circle cx="{x+119+i*8}" cy="{Y+110}" r="2" fill="#6b846c"/>')
add(f'<rect x="{x+118}" y="{Y+131}" width="28" height="44" rx="3" fill="#283e2c"/>')
for i,ww in enumerate([80,62,72]): line(x+157,Y+135+i*12,x+157+ww,Y+135+i*12,'#86a880',3)
add(f'<rect x="{x+231}" y="{Y+143}" width="32" height="58" rx="6" fill="#17291c" stroke="{LIME}"/>')
line(x+242,Y+150,x+251,Y+150,LIME)
txt(x+22,Y+235,'Web applications',23,TEXT,600)
txt(x+22,Y+267,'INTERFACES · CLIENT / SERVER',9,MUTED,mono=True,spacing=.6)

# Connected service modules.
x=416
for i,(xx,yy) in enumerate([(x+115,Y+102),(x+195,Y+126),(x+115,Y+156)]):
 add(f'<rect x="{xx}" y="{yy}" width="56" height="32" rx="6" fill="#17291c" stroke="{LIME if i==1 else "#526c57"}"/>')
 for k in [0,1]: add(f'<circle cx="{xx+10+k*8}" cy="{yy+16}" r="2" fill="#87a57b"/>')
 line(xx+29,yy+16,xx+45,yy+16,'#87a57b',2)
add(f'<path id="services" d="M{x+171} {Y+118}h24v24h0M{x+195} {Y+142}h-16v30h-8" fill="none" stroke="#5c855e"/>')
add(f'<circle r="2.6" fill="{LIME}"><animateMotion dur="5s" repeatCount="indefinite"><mpath xlink:href="#services"/></animateMotion></circle>')
txt(x+22,Y+235,'APIs & services',23,TEXT,600)
txt(x+22,Y+267,'REST APIS · SERVICE INTEGRATION',9,MUTED,mono=True,spacing=.6)

# Streaming tokens, grounded in the public EdTech implementation.
x=802
add(f'<rect x="{x+104}" y="{Y+103}" width="58" height="76" rx="9" fill="#17291c" stroke="#526c57"/>')
txt(x+133,Y+146,'{ }',18,LIME,600,True,'middle')
add(f'<path id="stream" d="M{x+162} {Y+140}h47" stroke="#75996b" stroke-width="1.4"/>')
add(f'<circle r="2.7" fill="{LIME}"><animateMotion dur="2s" repeatCount="indefinite"><mpath xlink:href="#stream"/></animateMotion></circle>')
add(f'<rect x="{x+211}" y="{Y+103}" width="58" height="76" rx="9" fill="#17291c" stroke="{LIME}"/>')
for i,ww in enumerate([31,21,28,13]):
 add(f'<rect x="{x+224}" y="{Y+119+i*12}" width="{ww}" height="3" rx="1.5" fill="#9cbe87"><animate attributeName="opacity" values=".35;1;.35" dur="3s" begin="{i*.3}s" repeatCount="indefinite"/></rect>')
txt(x+22,Y+235,'LLM integrations',23,TEXT,600)
txt(x+22,Y+267,'STREAMING · CONTEXT MANAGEMENT',9,MUTED,mono=True,spacing=.6)

# 3. Pac-Man: one pellet per GitHub contribution week. Entirely self-hosted SVG.
Y=671; panel(Y,325); section(Y+36,'03','PAC / CONTRIBUTIONS','PAST YEAR / WEEKLY ACTIVITY')
line(30,Y+54,1170,Y+54)
add(f'<rect x="30" y="{Y+69}" width="1140" height="145" rx="14" fill="#0d1510" stroke="#3f5b40"/>')
rows=[Y+88+j*35 for j in range(4)]
for j in range(3):
 yy=rows[j]+17.5
 for i in range(5):
  add(f'<rect x="{94+i*212}" y="{yy-3.5}" width="152" height="7" rx="3.5" fill="#203b25" stroke="#66864c" stroke-width=".7"/>')
weeks=data['contributionsCollection']['contributionCalendar']['weeks']
values=[sum(d['contributionCount'] for d in week['contributionDays']) for week in weeks]
maxweek=max(values)
coords=[]
for row in range(4):
 for col in range(14):
  xx=65+(col if row%2==0 else 13-col)*(1070/13)
  coords.append((xx,rows[row]))
route='M'+ 'L'.join(f'{x:.2f},{y:.2f}' for x,y in coords)
route+=f'L65,{rows[-1]}L46,{rows[-1]}L46,{rows[0]}Z'
add(f'<path id="arcade-route" d="{route}" fill="none" stroke="none"/>')
for i,(x,y) in enumerate(coords):
 if i>=len(values): continue
 v=values[i]; rr=2 if v==0 else 3+math.sqrt(v/maxweek)*2.3
 color='#29402d' if v==0 else LIME
 add(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{rr:.2f}" fill="{color}" opacity="{.55 if v==0 else .9}"><title>{weeks[i]["contributionDays"][0]["date"]}: {v} weekly contributions</title>')
 if v:
  t=min(.96,(i+1)/59)
  add(f'<animate attributeName="opacity" values=".9;0;0;.9" keyTimes="0;{t:.5f};.99;1" dur="24s" calcMode="discrete" repeatCount="indefinite"/>')
 add('</circle>')
add('<g><animateMotion dur="24s" repeatCount="indefinite" rotate="auto"><mpath xlink:href="#arcade-route"/></animateMotion>')
add(f'<circle r="12" fill="{LIME}"/><path d="M0 0L13 -9V9Z" fill="#0d1510"><animate attributeName="d" values="M0 0L13 -9V9Z;M0 0L13 -1V1Z;M0 0L13 -9V9Z" dur=".35s" repeatCount="indefinite"/></path><circle cx="1" cy="-6" r="1.5" fill="#18291b"/></g>')
for lag,color in [(1.0,'#8fc8ad'),(1.9,'#bfb2d9')]:
 add(f'<g><animateMotion dur="24s" begin="{-24+lag}s" repeatCount="indefinite"><mpath xlink:href="#arcade-route"/></animateMotion><path d="M-10 10V-1a10 10 0 0 1 20 0v11l-4-4-3 4-3-4-3 4-3-4Z" fill="{color}"/><ellipse cx="-3" cy="-1" rx="3" ry="4" fill="#edf5ed"/><ellipse cx="5" cy="-1" rx="3" ry="4" fill="#edf5ed"/><circle cx="-2" cy="-1" r="1.6" fill="#18291b"/><circle cx="6" cy="-1" r="1.6" fill="#18291b"/></g>')
txt(34,Y+229,days[0]['date'],8,MUTED,mono=True)
txt(1166,Y+229,days[-1]['date'],8,MUTED,mono=True,anchor='end')
line(30,Y+243,1170,Y+243)
metrics=[('CONTRIBUTIONS',str(total)),('ACTIVE DAYS',str(active)),('PEAK DAY',str(peak)),('WEEKLY AVERAGE',f'{total/(len(days)/7):.1f}')]
for i,(label,value) in enumerate(metrics):
 xx=34+i*288
 if i>0: line(xx-15,Y+256,xx-15,Y+307)
 txt(xx,Y+266,label,9,MUTED,mono=True,spacing=1)
 txt(xx,Y+300,value,26,TEXT,600,True)
error=0

txt(30,1026,'FULL-STACK / WEB & API',10,MUTED,mono=True,spacing=1)
add('<a xlink:href="mailto:texnop30618@gmail.com">')
txt(1170,1026,'texnop30618@gmail.com ↗',11,LIME,mono=True,anchor='end');add('</a>')
add('</svg>')
(OUT/'assets/profile.svg').write_text(''.join(S))

print('Updated profile.svg from current GitHub contribution data.')
