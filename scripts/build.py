"""Build seven portable GitHub profile themes and a local preview gallery."""
import argparse
import base64
import json
import sys
import xml.etree.ElementTree as ET
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = 'Theater-ahyeon/github-profile-themes'
RAW = f'https://raw.githubusercontent.com/{REPO}/main'
THEMES = [
    dict(id='phoebe-cathedral', name='辉弦圣堂', en='Radiant Cathedral', desc='白金圣光、蓝色彩窗与古典衬线字体。', font='Georgia,serif', light=['#FAF9F5','#172D50','#92703A','#DED7C6'], dark=['#101A2C','#F7F5EE','#D9C089','#36465E']),
    dict(id='phoebe-notebook', name='菲比贴纸手账', en='Phoebe Notebook', desc='奶油方格纸、Q 版菲比、蓝紫便签和圆角纸卡。', font='Arial,sans-serif', light=['#FFF9EC','#353347','#7960A0','#E3DFD4'], dark=['#242636','#F7F0DC','#C6B4EF','#44485E']),
    dict(id='phoebe-sea-glow', name='海风暮光', en='Sea Glow', desc='海边暮光、留白排版与克制的香槟色细线。', font='Georgia,serif', light=['#F4F6F7','#22394B','#836C42','#D4DDE2'], dark=['#142235','#F0F2F3','#D4BF97','#36495C']),
    dict(id='deepseek-cafe', name='奶茶休息站', en='Token Tea Club', desc='焦糖与奶油色、咖啡馆菜单、奶茶补给和票据装饰。', font='Georgia,serif', source='1279.webp', light=['#FFF3DF','#4A3029','#AD573F','#D9B798'], dark=['#302721','#FBECD4','#EBAA89','#665043']),
    dict(id='deepseek-terminal', name='终端工作台', en='Whale Terminal', desc='薄荷绿命令行、等宽字体与正在思考的蓝鲸助手。', font='Consolas,monospace', source='003.webp', light=['#EDF5F0','#183F34','#206B51','#AEC8BC'], dark=['#101D1C','#D6F6E8','#74DCAD','#33594D']),
    dict(id='deepseek-press', name='开发者小报', en='The Context Times', desc='报纸栏线、超长上下文梗图、刊号与编辑部式排版。', font='Georgia,serif', source='257.webp', light=['#F5F1E7','#292B2D','#AD423C','#BFB8AC'], dark=['#282829','#EFEBE1','#ED978B','#626264']),
    dict(id='deepseek-orbit', name='鲸鱼太空舱', en='Whale Orbit', desc='轨道弧线、发射面板、火箭鲸鱼与蓝橙对比。', font='Arial,sans-serif', source='ekQ35-8jlfZbT3cSmr-sg.jpg', light=['#EEF3FB','#172B4A','#996023','#B9C9DF'], dark=['#101B31','#EAF2FF','#EDB675','#354A6B']),
]


def svg(w, h, body, title):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(title)}"><title>{escape(title)}</title>{body}</svg>'


def text(x, y, value, size, color, font='Arial,sans-serif', extra=''):
    return f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" font-family="{font}" {extra}>{escape(str(value))}</text>'


def image_data(name):
    p = ROOT/'sources/deepseek'/name
    mime = 'image/webp' if p.suffix == '.webp' else 'image/jpeg'
    return f'data:{mime};base64,' + base64.b64encode(p.read_bytes()).decode()


def new_art(t, mode, dest):
    bg, ink, accent, line = t[mode]
    font, slug = t['font'], t['id']
    im = image_data(t['source'])
    if slug == 'deepseek-cafe':
        body = f'<rect width="1200" height="480" rx="30" fill="{bg}"/><path d="M437 22V458" stroke="{line}" stroke-width="2" stroke-dasharray="5 8"/><rect x="27" y="27" width="378" height="426" rx="12" fill="#FFFFFF" stroke="{line}" stroke-width="2"/><image x="40" y="55" width="354" height="354" href="{im}"/>'
        body += text(482,77,'TOKEN TEA CLUB',16,accent,font,'letter-spacing="5"')
        body += text(478,176,'Theater-ahyeon',54,ink,font)
        body += text(482,219,'a fresh brew of code & curiosity.',22,accent,font)
        body += f'<path d="M482 250H1135" stroke="{line}"/>'
        for y,a,b in [(295,'01 / learning','BUPT'),(339,'02 / making','side projects'),(383,'03 / sharing','open source')]:
            body += text(486,y,a,19,ink,font)+text(1118,y,b,19,accent,font,'text-anchor="end"')
        body += text(482,437,'TAKE A BREAK. BUILD SOMETHING NICE.',12,accent,'Arial,sans-serif','letter-spacing="2"')
    elif slug == 'deepseek-terminal':
        body = f'<rect width="1200" height="480" rx="10" fill="{bg}"/><path d="M0 48H1200 M728 48V480" stroke="{line}" stroke-width="2"/>'
        for x,c in [(28,'#DE7C78'),(53,'#DEBF78'),(78,'#75BB97')]:body += f'<circle cx="{x}" cy="24" r="6" fill="{c}"/>'
        body += text(105,30,'theater@whale: ~/open-source',15,ink,font)
        body += text(44,113,'$ whoami',21,accent,font)+text(42,186,'Theater-ahyeon',53,ink,font,'font-weight="700"')
        body += text(44,243,'> code, notes, and side projects',21,accent,font)
        for y,s in [(307,'[ ok ] learning at BUPT'),(346,'[ ok ] sending small patches upstream'),(385,'[ .. ] thinking about the next idea')]:body += text(44,y,s,18,ink,font)
        body += f'<rect x="44" y="418" width="13" height="23" fill="{accent}"/><rect x="754" y="70" width="420" height="384" rx="8" fill="#FFFFFF"/><image x="778" y="77" width="368" height="368" href="{im}"/>'
    elif slug == 'deepseek-press':
        body = f'<rect width="1200" height="500" fill="{bg}"/><path d="M25 36H1175 M25 132H1175 M25 141H1175 M25 462H1175 M703 157V445" stroke="{ink}" stroke-width="2"/>'
        body += text(32,27,'PERSONAL EDITION / NO. 01',12,ink,font,'letter-spacing="2"')+text(1170,27,'CODE · NOTES · OPEN SOURCE',12,ink,font,'text-anchor="end" letter-spacing="2"')
        body += text(600,109,'THE CONTEXT TIMES',61,ink,font,'text-anchor="middle" font-weight="700"')
        body += text(36,197,'THEATER-AHYEON',20,accent,font,'letter-spacing="3"')+text(35,268,'Small patches.',55,ink,font,'font-weight="700"')+text(35,327,'Shared progress.',55,ink,font,'font-weight="700"')
        body += text(38,389,'Dispatches from a curious developer at BUPT.',20,ink,font)+text(38,426,'Less noise. More things worth making.',20,accent,font)
        body += f'<image x="725" y="153" width="440" height="296" href="{im}" preserveAspectRatio="xMidYMid meet"/>'
        body += text(32,485,'THE LONG CONTEXT DESK',12,ink,font,'letter-spacing="2"')+text(1170,485,'ONE PAGE AT A TIME',12,ink,font,'text-anchor="end" letter-spacing="2"')
    else:
        body = f'<rect width="1200" height="480" rx="18" fill="{bg}"/><g fill="none" stroke="{line}" stroke-width="1"><ellipse cx="270" cy="240" rx="355" ry="156" transform="rotate(-24 270 240)"/><circle cx="270" cy="240" r="218"/><path d="M42 416H666"/></g>'
        for x,y in [(72,62),(618,80),(654,323),(338,35),(125,387),(552,377),(690,149)]:body += f'<circle cx="{x}" cy="{y}" r="2" fill="{accent}"/>'
        body += f'<rect x="778" width="422" height="480" fill="#111B2C"/><image x="786" y="0" width="414" height="480" href="{im}" preserveAspectRatio="xMidYMid meet"/>'
        body += text(47,105,'MISSION / OPEN SOURCE',15,accent,font,'letter-spacing="4"')+text(42,206,'Theater-ahyeon',58,ink,font,'font-weight="700"')
        body += text(47,258,'little commits, wider orbits.',26,ink,font)+text(47,330,'BUPT  /  CODE  /  CURIOSITY',15,accent,font,'letter-spacing="3"')
        body += text(47,447,'FLIGHT LOG: KEEP EXPLORING',13,ink,'Consolas,monospace','letter-spacing="2"')
    (dest/f'hero-{mode}.svg').write_text(svg(1200,500 if slug=='deepseek-press' else 480,body,t['en']),encoding='utf-8')
    mark={'deepseek-cafe':'TEA BREAK','deepseek-terminal':'// next section','deepseek-press':'• • •','deepseek-orbit':'— ORBIT —'}[slug]
    body=f'<path d="M0 26H455 M745 26H1200" stroke="{line}" stroke-width="2"/>'+text(600,32,mark,15,accent,font,'text-anchor="middle" letter-spacing="3"')
    (dest/f'divider-{mode}.svg').write_text(svg(1200,52,body,'Section divider'),encoding='utf-8')
    footer={'deepseek-cafe':('thanks a latte.','same time, next commit?'),'deepseek-terminal':('$ echo "thanks for stopping by"','exit 0  // see you next session'),'deepseek-press':('END OF THIS EDITION','More stories after the next commit.'),'deepseek-orbit':('TRANSMISSION COMPLETE','See you on the next orbit.')}[slug]
    body=f'<rect x="1" y="1" width="1198" height="148" rx="{0 if slug=="deepseek-press" else 16}" fill="{bg}" stroke="{line}"/>'+text(600,68,footer[0],30,ink,font,'text-anchor="middle"')+text(600,105,footer[1],16,accent,font,'text-anchor="middle"')
    (dest/f'footer-{mode}.svg').write_text(svg(1200,150,body,footer[0]),encoding='utf-8')


def cards(t, mode, dest, data):
    bg,ink,accent,line=t[mode];font=t['font'];rad=22 if t['id'] in ('phoebe-notebook','deepseek-cafe') else 6
    def card(title,body):
        head=f'<rect x="2" y="2" width="576" height="246" rx="{rad}" fill="{bg}" stroke="{line}" stroke-width="2"/><path d="M26 72H554" stroke="{line}"/>'+text(28,45,title,22,ink,font)
        return svg(580,250,head+body,title)
    body=''
    for i,(label,value) in enumerate([('Public original repos',data['repositories']),('Stars on these repos',data['stars']),('Contributions / past year',data['contributions'])]):
        y=111+i*44;body+=text(28,y,label,17,ink)+text(546,y+1,f'{value:,}',24,accent,font,'text-anchor="end" font-weight="700"')
    body+=text(28,232,'GitHub public data · '+data['generated_at'][:10],11,ink)
    (dest/f'stats-{mode}.svg').write_text(card('GitHub Stats',body),encoding='utf-8')
    body=''
    for x,label,n in [(152,'Merged PRs',len(data['merged_prs'])),(428,'Projects',len(data['projects']))]:body+=text(x,145,n,44,accent,font,'text-anchor="middle" font-weight="700"')+text(x,181,label,17,ink,font,'text-anchor="middle"')
    body+=text(290,224,'Public upstream repositories · all time',12,ink,'Arial,sans-serif','text-anchor="middle"')
    (dest/f'collaboration-{mode}.svg').write_text(card('Open-source collaboration',body),encoding='utf-8')
    projects=sorted(data['projects'].items(),key=lambda kv:(kv[0]!='bytedance/deer-flow',-kv[1],kv[0]));h=110+48*max(1,len(projects))
    body=f'<rect x="2" y="2" width="1196" height="{h-4}" rx="{rad}" fill="{bg}" stroke="{line}" stroke-width="2"/>'+text(30,44,'Merged contributions',25,ink,font)
    for i,(name,count) in enumerate(projects):
        y=91+i*48;pr=next(p for p in data['merged_prs'] if p['repository']['nameWithOwner']==name)
        body+=text(32,y,name,20,ink,font)+text(934,y,f'latest #{pr["number"]} · {pr["mergedAt"][:10]}',16,ink,'Arial,sans-serif','text-anchor="end"')+text(1166,y,f'{count} merged',20,accent,font,'text-anchor="end" font-weight="700"')+f'<path d="M30 {y+16}H1170" stroke="{line}" stroke-dasharray="4 7"/>'
    body+=text(32,h-18,'Own repositories and forks excluded · '+data['generated_at'][:10],12,ink)
    (dest/f'projects-{mode}.svg').write_text(svg(1200,h,body,'Merged contributions by project'),encoding='utf-8')


def picture(slug,kind,width='100%'):
    prefix=f'{RAW}/themes/{slug}/assets/{kind}'
    return f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{prefix}-dark.svg">\n  <source media="(prefers-color-scheme: light)" srcset="{prefix}-light.svg">\n  <img src="{prefix}-light.svg" width="{width}" alt="{kind} — {slug}">\n</picture>'


def documents(t,data):
    slug=t['id'];folder=ROOT/'themes'/slug
    # Curated examples remain direct, auditable links; counts above are exhaustive.
    examples=[]
    example_html=[]
    for name in ['bytedance/deer-flow','TencentCloud/Octop','crewAIInc/crewAI']:
        hits=[p for p in data['merged_prs'] if p['repository']['nameWithOwner']==name]
        if hits:
            pr=hits[0]
            label=pr['title'].replace('[',r'\[').replace(']',r'\]')
            examples.append(f'- **{name}** — [{label} #{pr["number"]}]({pr["url"]})')
            example_html.append(f'<li><b>{escape(name)}</b> — <a href="{escape(pr["url"])}">{escape(pr["title"])} #{pr["number"]}</a></li>')
    md=picture(slug,'hero')+'\n\n### about\n\n- Learning at **BUPT** · exploring computer science\n- Music, side projects, and a little curiosity\n- [theater1347507191@163.com](mailto:theater1347507191@163.com)\n\n'+picture(slug,'divider')+'\n\n### open-source notebook\n\n'+picture(slug,'stats','49%')+'\n'+picture(slug,'collaboration','49%')+'\n\n'+picture(slug,'projects')+'\n\n**Selected merged PRs**\n\n'+'\n'.join(examples)+'\n\n'+picture(slug,'footer')+f'\n\n<sub>Theme: {t["en"]} · [Theme collection](https://github.com/{REPO}) · [Artwork sources](https://github.com/{REPO}/blob/main/SOURCES.md)</sub>\n'
    (folder/'README.md').write_text(md,encoding='utf-8')
    preview=ROOT/'.preview';preview.mkdir(exist_ok=True)
    for mode in ('light','dark'):
        bg,fg=('#fff','#1f2328') if mode=='light' else ('#0d1117','#e6edf3')
        path=f'../themes/{slug}/assets/'
        im=lambda kind:f'<img src="{path}{kind}-{mode}.svg" alt="{kind}">'
        content=im('hero')+'<h3>about</h3><p>Learning at <b>BUPT</b> · exploring computer science<br>Music, side projects, and a little curiosity<br>theater1347507191@163.com</p>'+im('divider')+'<h3>open-source notebook</h3><div class="cards">'+im('stats')+im('collaboration')+'</div>'+im('projects')+'<h4>Selected merged PRs</h4><ul>'+''.join(example_html)+'</ul>'+im('footer')
        html=f'<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{t["en"]}</title><style>body{{margin:0;background:{bg};color:{fg};font:16px/1.6 Arial,sans-serif}}main{{max-width:1000px;margin:auto;padding:28px}}img{{max-width:100%;display:block}}.cards{{display:flex;gap:1%;margin:0 0 18px}}.cards img{{width:49.5%}}h3{{margin-top:24px}}li{{overflow-wrap:anywhere}}a{{color:inherit}}@media(max-width:500px){{main{{padding:12px}}}}</style><main>{content}</main></html>'
        (preview/f'{slug}-{mode}.html').write_text(html,encoding='utf-8')


def validate():
    for t in THEMES:
        for kind in ('hero','divider','footer','stats','collaboration','projects'):
            for mode in ('light','dark'):
                p=ROOT/'themes'/t['id']/'assets'/f'{kind}-{mode}.svg'
                root=ET.parse(p).getroot()
                assert root.tag=='{http://www.w3.org/2000/svg}svg'
                for el in root.iter():
                    assert not el.tag.endswith('script')
                    for k,v in el.attrib.items():
                        if k.endswith('href'):assert v.startswith(('data:image/','#'))
    print('Validated 84 self-contained SVG assets across 7 themes.')


def build(refresh=False):
    if refresh:
        from github_data import fetch
        data=fetch()
        (ROOT/'data/github.json').write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
    else:data=json.loads((ROOT/'data/github.json').read_text(encoding='utf-8'))
    for t in THEMES:
        dest=ROOT/'themes'/t['id']/'assets';dest.mkdir(parents=True,exist_ok=True)
        for mode in ('light','dark'):
            if 'source' in t:new_art(t,mode,dest)
            cards(t,mode,dest,data)
        documents(t,data)
    (ROOT/'themes.json').write_text(json.dumps(THEMES,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    validate()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--refresh',action='store_true');args=parser.parse_args();build(args.refresh)
