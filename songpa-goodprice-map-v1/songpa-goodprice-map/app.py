import streamlit as st
import streamlit.components.v1 as components
import json, pathlib, re, math, copy
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from urllib.error import HTTPError, URLError
st.set_page_config(page_title='송파구 착한가격업소 지도',layout='wide')
st.title('송파구 착한가격업소 지도')
st.caption('서울시 착한가격업소 현황 제공 파일 기준 · 실제 가격과 영업 여부는 방문 전 확인해 주세요.')
shops=json.loads((pathlib.Path(__file__).parent/'shops.json').read_text(encoding='utf-8'))
def secret(name):
    try:
        return str(st.secrets.get(name, '')).strip()
    except Exception:
        return ''

key = secret('KAKAO_JS_KEY')
rest_key = secret('KAKAO_REST_KEY')

def candidates(address):
    a = re.sub(r'길(?=\d)', '길 ', re.sub(r'(\d)\s+길', r'\1길', address.replace('서울특별시', '서울'))).strip()
    base = re.match(r'^(.*?(?:대로|로|길)\s*\d+(?:-\d+)?)(?=\s|\(|$)', a)
    return list(dict.fromkeys([base.group(1), a] if base else [a]))

def lookup(address, api_key):
    for query in candidates(address):
        url = 'https://dapi.kakao.com/v2/local/search/address.json?' + urlencode({'query': query})
        req = Request(url, headers={'Authorization': 'KakaoAK ' + api_key})
        with urlopen(req, timeout=5) as response:
            docs = json.load(response).get('documents', [])
        for doc in docs:
            try:
                lat, lng = float(doc['y']), float(doc['x'])
                if math.isfinite(lat) and math.isfinite(lng) and 37.3 < lat < 37.8 and 126.7 < lng < 127.4:
                    return lat, lng
            except (KeyError, TypeError, ValueError):
                continue
    return None

def resolve(records, api_key, progress):
    result = copy.deepcopy(records)
    memo = {}  # current request only; no shared cache or disk storage
    error = ''
    for i, shop in enumerate(result):
        if shop.get('lat') is not None and shop.get('lng') is not None:
            continue
        address = shop['address']
        try:
            if address not in memo:
                memo[address] = lookup(address, api_key)
            if memo[address]:
                shop['lat'], shop['lng'] = memo[address]
        except HTTPError as exc:
            error = f'카카오 REST API 오류 ({exc.code})'
            if exc.code in (400, 401, 403, 429) or exc.code >= 500:
                break
        except (URLError, TimeoutError, OSError, ValueError):
            error = '주소 검색 서버 연결 또는 응답 오류'
            break
        progress.progress((i+1)/len(result), text=f'업소 위치 확인 중 ({i+1}/{len(result)})')
    return result, error

if not rest_key:
    st.warning('Streamlit Secrets에 KAKAO_REST_KEY를 등록해 주세요. 업소 검색은 이용할 수 있습니다.')
else:
    # Keep results only in the individual Streamlit session, never in a file or shared cache.
    import hashlib
    signature = hashlib.sha256((json.dumps(shops, ensure_ascii=False)+rest_key).encode()).hexdigest()
    if st.button('업소 위치 다시 조회', key='retry_locations'):
        st.session_state.pop('location_result', None)
    saved = st.session_state.get('location_result')
    if not saved or saved[0] != signature:
        progress = st.progress(0, text='업소 위치 확인 중')
        resolved, error = resolve(shops, rest_key, progress)
        progress.empty()
        st.session_state['location_result'] = (signature, resolved, error)
    _, shops, error = st.session_state['location_result']
    if error:
        st.warning(error + ' · REST 키와 카카오맵 사용 권한을 확인한 뒤 다시 조회해 주세요.')
    missing = sum(s.get('lat') is None or s.get('lng') is None for s in shops)
    if missing:
        st.caption(f'위치 미확인 {missing}개 업소도 목록과 품목 검색에서 확인할 수 있습니다.')
# Embed the source records as JSON, escaping HTML script termination.
data=json.dumps(shops,ensure_ascii=False).replace('<','\\u003c')
page='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font-family:system-ui,sans-serif;margin:0;color:#17352c;background:white}header{display:flex;flex-wrap:wrap;gap:8px;align-items:end;padding:10px 0}label{display:flex;flex-direction:column;font-size:13px;gap:4px;flex:1;min-width:130px}input,select,button{font:inherit;padding:9px;border:1px solid #aabbb4;border-radius:8px;background:white;color:#17352c}button{cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #167c5b}#map{height:390px;background:#edf2ef;border-radius:12px}#status{font-size:13px;padding:8px 0}#list{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px;max-height:490px;overflow:auto}.shop{border:1px solid #ccd9d1;border-radius:12px;padding:13px;line-height:1.5}.shop h3{margin:0;font-size:17px}.address{font-size:13px;color:#52645a}.item{display:flex;justify-content:space-between;gap:10px;padding:4px 0}.matched{font-weight:700;color:#17694d}a{color:#17694d}#detail{padding:8px 0}@media(max-width:600px){#map{height:300px}header{gap:5px}#list{max-height:400px}}</style></head><body>
<header><label>업소명·주소·품목<input id="q" placeholder="예: 짜장면, 풍납동"></label><label>업종<select id="type"></select></label><label>품목<select id="item"></select></label><label>가격 상한(원)<input id="max" type="number" min="0" step="500" placeholder="제한 없음"></label><label>정렬<select id="sort"><option value="name">업소명 순</option><option value="price">해당 품목 가격 낮은 순</option></select></label><button id="reset">초기화</button><button id="loc">내 위치</button></header><div id="map" role="region" aria-label="착한가격업소 지도"></div><div id="status" role="status"></div><div id="detail" aria-live="polite"></div><div id="list" aria-label="검색 결과"></div>
<script>const shops=__DATA__;const key=__KEY__;const el=id=>document.getElementById(id);let map=null,markers=[],positions=new Map(),filtered=[],done=false;let failed=shops.filter(s=>!Number.isFinite(s.lat)||!Number.isFinite(s.lng)).length;const norm=s=>String(s??'').toLowerCase().replace(/\\s/g,'').replace(/자장면/g,'짜장면').replace(/돈까스/g,'돈가스');function options(id,values){el(id).replaceChildren(new Option('전체',''),...values.sort((a,b)=>a.localeCompare(b,'ko')).map(x=>new Option(x,x)))}options('type',[...new Set(shops.map(s=>s.type))]);function itemOptions(){let old=el('item').value;options('item',[...new Set(shops.filter(s=>!el('type').value||s.type===el('type').value).flatMap(s=>s.items.map(m=>m.category)))]);if([...el('item').options].some(o=>o.value===old))el('item').value=old}itemOptions();function node(tag,text,cls){let n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n}function card(s,matched){let d=node('article','','shop');d.append(node('h3',s.name),node('div',s.type+' · '+s.address,'address'));for(let m of s.items){let r=node('div','','item'+(matched.includes(m)?' matched':''));r.append(node('span',m.name),node('span',m.price==null?'가격 미등록':m.price.toLocaleString('ko-KR')+'원'));d.append(r)}let a=node('a','카카오맵 길찾기');a.target='_blank';a.rel='noopener noreferrer';let p=positions.get(s.id);a.href=p?'https://map.kakao.com/link/to/'+encodeURIComponent(s.name)+','+p.getLat()+','+p.getLng():'https://map.kakao.com/?q='+encodeURIComponent(s.address);d.append(a);if(p&&map){let b=node('button','지도 위치');b.style.marginLeft='8px';b.onclick=()=>{map.setCenter(p);map.setLevel(3);show(s,matched)};d.append(b)}return d}function show(s,m){el('detail').replaceChildren(card(s,m))}function render(){let q=norm(el('q').value),t=el('type').value,c=el('item').value,max=el('max').value===''?Infinity:Number(el('max').value);filtered=shops.filter(s=>!t||s.type===t).map(s=>({s,m:s.items.filter(m=>(!c||m.category===c)&&(max===Infinity||(m.price!==null&&m.price<=max))&&(!q||[s.name,s.address,s.type,m.name,m.category].some(x=>norm(x).includes(q))))})).filter(x=>x.m.length);filtered.sort((a,b)=>el('sort').value==='price'?Math.min(...a.m.map(m=>m.price??Infinity))-Math.min(...b.m.map(m=>m.price??Infinity)):a.s.name.localeCompare(b.s.name,'ko'));el('list').replaceChildren(...filtered.map(x=>card(x.s,x.m)));let count=filtered.filter(x=>positions.has(x.s.id)).length;el('status').textContent=`전체 ${shops.length}개 중 ${filtered.length}개 업소 · 지도 위치 ${count}개 확인`+(done?` · 전체 위치 미확인 ${failed}개`:key?' · 지도 로딩 중':' · 지도 API 키 필요');if(map){markers.forEach(m=>m.setMap(null));markers=[];let bounds=new kakao.maps.LatLngBounds();for(let x of filtered){let p=positions.get(x.s.id);if(!p)continue;let m=new kakao.maps.Marker({map,position:p,title:x.s.name});kakao.maps.event.addListener(m,'click',()=>show(x.s,x.m));markers.push(m);bounds.extend(p)}if(markers.length&&done)map.setBounds(bounds)}}for(let id of ['q','item','max','sort'])el(id).addEventListener('input',()=>{el('detail').replaceChildren();render()});el('type').onchange=()=>{itemOptions();el('detail').replaceChildren();render()};el('reset').onclick=()=>{for(let id of ['q','type','max'])el(id).value='';itemOptions();el('item').value='';el('sort').value='name';el('detail').replaceChildren();render()};el('loc').onclick=()=>{if(!map||!navigator.geolocation){alert('현재 위치 기능을 사용할 수 없습니다.');return}navigator.geolocation.getCurrentPosition(p=>{map.setCenter(new kakao.maps.LatLng(p.coords.latitude,p.coords.longitude));map.setLevel(4)},()=>alert('위치 권한을 확인해 주세요.'))};render();function init(){map=new kakao.maps.Map(el('map'),{center:new kakao.maps.LatLng(37.5145,127.106),level:7});for(let s of shops){if(Number.isFinite(s.lat)&&Number.isFinite(s.lng)){positions.set(s.id,new kakao.maps.LatLng(s.lat,s.lng))}}done=true;render()}if(key){let script=document.createElement('script');script.src='https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey='+encodeURIComponent(key);script.onload=()=>{if(window.kakao?.maps?.load)kakao.maps.load(init);else el('map').textContent='카카오맵 설정을 확인해 주세요.'};script.onerror=()=>el('map').textContent='지도 로딩 실패: API 키 및 허용 도메인을 확인해 주세요.';document.head.append(script)}else el('map').textContent='카카오맵 JavaScript 키 설정 후 지도 위치가 표시됩니다. 아래 검색은 지금도 가능합니다.';</script></body></html>'''
page=page.replace('__DATA__',data).replace('__KEY__',json.dumps(str(key)).replace('<','\\u003c'))
components.html(page,height=1100,scrolling=True)
