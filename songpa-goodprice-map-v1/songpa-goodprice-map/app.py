import streamlit as st
import streamlit.components.v1 as components
import json, pathlib
st.set_page_config(page_title='송파구 착한가격업소 지도',layout='wide')
st.markdown("""<style>
[data-testid="stAppViewContainer"], .stApp, [data-testid="stMain"] {background-color:#FAF7F0 !important;color:#24332B !important;color-scheme:light !important;}
[data-testid="stHeader"] {background-color:rgba(250,247,240,.94) !important;}
[data-testid="stAppViewContainer"] h1 {color:#24332B !important;}
[data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"], [data-testid="stAppViewContainer"] [data-testid="stCaptionContainer"] p {color:#33443B !important;}
[data-testid="stMainBlockContainer"], [data-testid="stMain"] .block-container {padding-top:1.25rem !important;}
@media(max-width:680px){[data-testid="stMainBlockContainer"], [data-testid="stMain"] .block-container {padding-top:.65rem !important;}}
</style>""", unsafe_allow_html=True)
st.title('송파구 착한가격업소 지도')
st.caption('서울시 착한가격업소 현황 제공 파일 기준')
shops=json.loads((pathlib.Path(__file__).parent/'shops.json').read_text(encoding='utf-8'))
def secret(name):
    try:
        return str(st.secrets.get(name, '')).strip()
    except Exception:
        return ''

key = secret('KAKAO_JS_KEY')
# Coordinates are prepared offline from an authorized source.
missing = sum(s.get('lat') is None or s.get('lng') is None for s in shops)
if missing:
    st.caption(f'위치 미등록 {missing}개 업소 · 업소 목록과 품목 검색은 이용 가능합니다.')
# Embed the source records as JSON, escaping HTML script termination.
data=json.dumps(shops,ensure_ascii=False).replace('<','\\u003c')
page='''<!doctype html><html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>
*{box-sizing:border-box}body{font-family:system-ui,sans-serif;margin:0;color:#17352c;background:white}header{display:flex;flex-wrap:wrap;gap:8px;align-items:end;padding:10px 0}label{display:flex;flex-direction:column;font-size:13px;gap:4px;flex:1;min-width:130px}input,select,button{font:inherit;padding:9px;border:1px solid #aabbb4;border-radius:8px;background:white;color:#17352c}button{cursor:pointer}button:focus-visible,a:focus-visible{outline:3px solid #167c5b}#map{height:390px;background:#edf2ef;border-radius:12px}#status{font-size:13px;padding:8px 0}#list{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:8px;max-height:490px;overflow:auto}.shop{border:1px solid #ccd9d1;border-radius:12px;padding:13px;line-height:1.5}.shop h3{margin:0;font-size:17px}.address{font-size:13px;color:#52645a}.item{display:flex;justify-content:space-between;gap:10px;padding:4px 0}.matched{font-weight:700;color:#17694d}a{color:#17694d}#detail{padding:8px 0}@media(max-width:600px){#map{height:300px;width:86%;margin-inline:auto}header{gap:5px}#list{max-height:400px}}
/* Songpa citizen service palette, matched to tobacco public_app.py */
:root{color-scheme:light}
body{background:#FAF7F0;color:#24332B}
header{background:#f1f5ee;border:1px solid #c5d6c9;border-radius:12px;padding:12px;margin-bottom:10px}
label{color:#33443B;font-weight:700}
input,select{background:#FFFFFF;color:#24332B;border:1px solid #789782;min-width:0;width:100%}
input::placeholder{color:#65736a;opacity:1}
input:focus,select:focus{outline:3px solid #95D2AC;outline-offset:1px;border-color:#287D4B}
button{background:#287D4B;border-color:#287D4B;color:#FFFFFF;font-weight:600}
button:hover{background:#38965D;border-color:#38965D}
button:active{background:#21683E;border-color:#21683E}
button:focus-visible,a:focus-visible{outline:3px solid #95D2AC;outline-offset:2px}
#reset{background:#FFFFFF;color:#21683E;border-color:#287D4B}
#reset:hover{background:#e7f1e9}
.shop{background:#FFFFFF;border-color:#ccd9d1;color:#24332B}
.address,#status{color:#33443B}
.matched,a{color:#21683E}
@media(max-width:600px){header{padding:9px;gap:5px}}

/* Temporary Christmas market notice */
#event-reopen{display:block;width:100%;margin:0 0 10px;background:#343D5C;border-color:#343D5C;text-align:left}
#event-reopen[hidden]{display:none}
#christmas-notice{width:min(540px,calc(100% - 24px));max-height:min(78vh,720px);padding:0;border:0;border-radius:16px;background:#fffdf7;color:#24332B;box-shadow:0 12px 42px #0005;overflow:auto;margin:16px auto auto}
#christmas-notice::backdrop{background:rgba(20,29,28,.60)}
.event-head{background:#21683E;color:white;padding:18px 22px}
.event-head p{margin:0 0 6px;font-size:13px;color:#fff}
.event-head h2{margin:0;font-size:23px;line-height:1.3}
.event-body{padding:16px 20px;line-height:1.55;font-size:14px}
.event-body p{margin:8px 0}
.event-benefit{border:1px solid #c5d6c9;background:#f1f5ee;border-radius:10px;padding:10px 12px;margin:10px 0}
.event-limit{background:#842f23;color:#fff;text-align:center;font-weight:800;font-size:20px;padding:10px;border-radius:9px;margin:12px 0}.event-limit strong{font-size:27px}.event-benefit-image{display:block;width:100%;height:auto;margin:9px auto;border-radius:6px}.event-cracker{margin:10px 0;text-align:center}.event-cracker img{display:block;width:180px;max-width:80%;height:auto;margin:auto;border-radius:8px}.event-cracker figcaption{font-size:12px;color:#33443B;margin-top:5px}.event-alert{background:#fff0e8;color:#842f23;border-radius:8px;padding:10px}
.event-actions{display:flex;gap:8px;flex-wrap:wrap;padding:12px 20px;background:#fffdf7;border-top:1px solid #ddd;position:sticky;bottom:0}
.event-actions button{flex:1}
#event-hide-today{background:white;color:#21683E}
@media(max-width:600px){#christmas-notice{max-height:min(70vh,540px)}.event-head{padding:14px 16px}.event-head h2{font-size:20px}.event-body{padding:12px 16px}.event-actions{padding:10px 16px}}
</style></head><body>

<button id="event-reopen" type="button" hidden>🎄 크리스마스 마켓 지역상권 상생 이벤트 안내 다시 보기</button>
<dialog id="christmas-notice" aria-labelledby="event-title">
  <div class="event-head"><p>2026 롯데타운 크리스마스 마켓 연계</p><h2 id="event-title">송파 지역상권 상생 이벤트</h2></div>
  <div class="event-body">
    <p><strong>2026. 11. 19.(목) ~ 2027. 1. 3.(일)</strong><br>롯데월드몰 뒤 월드파크 잔디광장</p>
    <p>송파구 착한가격업소 또는 송파사랑상품권 가맹점에서 <strong>당일 3만원 이상 구매</strong>하면 특별혜택을 드립니다.</p>
    <div class="event-limit">매일 선착순 <strong>100명</strong></div><p>결제수단 무관 · 매장 간 영수증 합산 불가</p>
    <div class="event-benefit"><strong>특별혜택 (택 1)</strong><img class="event-benefit-image" src="data:image/webp;base64,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" alt="혜택 구성: 옵션 1 무료 일반 입장권, 회전목마 이용권, 크리스마스 크래커 / 옵션 2 대기 없는 빠른 입장"><p>❶ 일반입장 + 회전목마 이용권 + 크리스마스 크래커</p><p>❷ 대기 없는 빠른입장</p><small>두 혜택 모두 별도 사전예약 없이 이용 가능</small></div>
    <figure class="event-cracker"><img src="data:image/webp;base64,UklGRjIEAABXRUJQVlA4ICYEAACQHQCdASq0AHwAPyWKuleuKSUjprpp4cAkiU3bq/dXpXj26HPdeeLD3Czxsyf18R1p4svE0GTF3w0+lZPP+q2AtLlMfhPWVH2DKMgaQXJ2IUt7OJ3tIi4WPY59LxbinHp+L/m52JRCdf3OnFSVWWq/VzfVkFcNYq3IVxJU56KaNDoXM+VUWrP55CrNkh1bN1n99hK/9EVdwDnEdNbR8WcpYhyEbuzVRIIShNWE1onSKozLwCqcSpJWGXFlRFIlCaCJLorNFkMweZvB4O75l45weep7/F1e2YA7KHXuvLtk8JTGQvS3r6W5gNBF4jNOUnx9FbdgAAD+8I/KHDapjn4RFEAOypmWIAmCfawLzQbGxFt7X1Yr1V6wdRDQ5L1lICA+rGLjODlenEfd8ZS3oe9Vh63WQfYfwBuEf/oGquxMXwwADftWkBo3OqwvlTeddiowuqe0/+dMb4uw613N7aFaannopQYWtXS3SvDZwno7fZLkok1jm8SmO49QBcSHUnxWcDwsesgrgsSDkmXVUZVqGJSq2DJ5TJfKHdex1zr7gnpR/7vu1sEOv+yyjsf9WzL1OBHcIsBc8BbmyNeduUNOhKoSzmbFwYpOyfq7bOk2Ail6izid0dOsU6OIbG9+8Olc8ffwbpCeppDjF+0uyPaF2dWCAyhQQQN3tC6kfj0DPsGGObMAiLrxa8eAIYG1HMnI0WaVxab0PcOxfwND9rMjbNE0dkt8iWZ2VWlbOVkcwnQ0MlzrgrML25Sd/yLHydLrvFRmN0vGIQL/Pd7z7tlWyFmr5KPpCX3gAuhwg7wmzdntKb9Em1nSUSPpciagwDc3WegzxZpGy2ksjSUmBtxI9vv/XvvAX1hd52GnpRuy8Pho1o3prpdh0ldf28STPd8nskcDdNTd8N27vPNUuG9W09+se5rlXlg1qSToATl5gDBDPjMR7jxMXQ6OS4RaMMj0eH5O0HvAn7CiRY+HzWmIe3L3h5lUZyUeZtvJdiAUubIQ/UNtpnWt9toLRj3FoqeAwJiThv5ivwRPiDfbzUzvn2f04drj09aHmVAXo9Hqtynbie32Z7u42Gkhps3Uv1kz0hP+mvyaK0aNZPxv9XowZH+rGu2Fw22We5+ZGYgZNw9dIDe7hoGDHvru3R4Sccz9HUKgYinQJloOH5mxypMjzOZlPTH8hmEgRSQcL0dd/v/oPyxKSrF7CiHkoIDk1FfXV/TFiaK6WwiO4OftyyhfL7rss1iPetA3HitDLhHYR+jxj/y4JYU+NaP+lKNeHMAOMpbD8Ul5IkJ4DVrcrRjQIQkXvAofnSxiqhV/Nn2MwewsDWZiw6bQNhvvKaHwFrgt5KrYkYQNdaIhPFR2402D+QdNRfe4OyJcgl3XsXkp9rF8j4eVTLRY+8TUmFPOxy4BclqAAAA=" alt="크리스마스 마켓 한정 크리스마스 크래커 실제 증정품"><figcaption>크리스마스 마켓 한정 굿즈 · 마시멜로 동봉</figcaption></figure><p><strong>참여방법</strong> · 당일 구매 영수증을 행사장 입구 우측 종합안내소에서 인증해 주세요.</p>
    <p class="event-alert"><strong>12.24.~12.25. 안내</strong><br>안전을 위해 크리스마스 크래커만 제공하며 입장 지원 및 회전목마 이용권은 제공하지 않습니다.</p>
    <p><small>주최: 롯데백화점 / 후원: 송파구</small></p>
  </div>
  <div class="event-actions"><button id="event-hide-today" type="button">오늘 하루 보지 않기</button><button id="event-close" type="button" autofocus>닫기</button></div>
</dialog>
<header><label>업소명·주소·품목<input id="q" placeholder="예: 짜장면, 풍납동"></label><label>업종<select id="type"></select></label><label>품목<select id="item"></select></label><label>가격 상한(원)<input id="max" type="number" min="0" step="500" placeholder="제한 없음"></label><label>정렬<select id="sort"><option value="name">업소명 순</option><option value="price">해당 품목 가격 낮은 순</option></select></label><button id="reset">초기화</button><button id="loc">내 위치</button></header><div id="map" role="region" aria-label="착한가격업소 지도"></div><div id="status" role="status"></div><div id="detail" aria-live="polite"></div><div id="list" aria-label="검색 결과"></div>
<script>const shops=__DATA__;const key=__KEY__;const el=id=>document.getElementById(id);let map=null,markers=[],positions=new Map(),filtered=[],done=false;let failed=shops.filter(s=>!Number.isFinite(s.lat)||!Number.isFinite(s.lng)).length;const norm=s=>String(s??'').toLowerCase().replace(/\\s/g,'').replace(/자장면/g,'짜장면').replace(/돈까스/g,'돈가스');function options(id,values){el(id).replaceChildren(new Option('전체',''),...values.sort((a,b)=>a.localeCompare(b,'ko')).map(x=>new Option(x,x)))}options('type',[...new Set(shops.map(s=>s.type))]);function itemOptions(){let old=el('item').value;options('item',[...new Set(shops.filter(s=>!el('type').value||s.type===el('type').value).flatMap(s=>s.items.map(m=>m.category)))]);if([...el('item').options].some(o=>o.value===old))el('item').value=old}itemOptions();function node(tag,text,cls){let n=document.createElement(tag);n.textContent=text;if(cls)n.className=cls;return n}function card(s,matched){let d=node('article','','shop');d.append(node('h3',s.name),node('div',s.type+' · '+s.address,'address'));for(let m of s.items){let r=node('div','','item'+(matched.includes(m)?' matched':''));r.append(node('span',m.name),node('span',m.price==null?'가격 미등록':m.price.toLocaleString('ko-KR')+'원'));d.append(r)}if(s.coordinate_match==='주소 기준 건물 위치')d.append(node('div','주소 기준 건물 위치 · 상호 미대조','address'));if(s.coordinate_match==='미확인')d.append(node('div','지도 위치 미확인','address'));let a=node('a','카카오맵 길찾기');a.target='_blank';a.rel='noopener noreferrer';let p=positions.get(s.id);a.href=p?'https://map.kakao.com/link/to/'+encodeURIComponent(s.name)+','+p.getLat()+','+p.getLng():'https://map.kakao.com/?q='+encodeURIComponent(s.address);d.append(a);if(p&&map){let b=node('button','지도 위치');b.style.marginLeft='8px';b.onclick=()=>{map.setCenter(p);map.setLevel(3);show(s,matched)};d.append(b)}return d}function show(s,m){el('detail').replaceChildren(card(s,m))}function render(){let q=norm(el('q').value),t=el('type').value,c=el('item').value,max=el('max').value===''?Infinity:Number(el('max').value);filtered=shops.filter(s=>!t||s.type===t).map(s=>({s,m:s.items.filter(m=>(!c||m.category===c)&&(max===Infinity||(m.price!==null&&m.price<=max))&&(!q||[s.name,s.address,s.type,m.name,m.category].some(x=>norm(x).includes(q))))})).filter(x=>x.m.length);filtered.sort((a,b)=>el('sort').value==='price'?Math.min(...a.m.map(m=>m.price??Infinity))-Math.min(...b.m.map(m=>m.price??Infinity)):a.s.name.localeCompare(b.s.name,'ko'));el('list').replaceChildren(...filtered.map(x=>card(x.s,x.m)));let count=filtered.filter(x=>positions.has(x.s.id)).length;el('status').textContent=`전체 ${shops.length}개 중 ${filtered.length}개 업소 · 지도 위치 ${count}개 확인`+(done?` · 전체 위치 미확인 ${failed}개`:key?' · 지도 로딩 중':' · 지도 API 키 필요');if(map){markers.forEach(m=>m.setMap(null));markers=[];let bounds=new kakao.maps.LatLngBounds();for(let x of filtered){let p=positions.get(x.s.id);if(!p)continue;let m=new kakao.maps.Marker({map,position:p,title:x.s.name});kakao.maps.event.addListener(m,'click',()=>show(x.s,x.m));markers.push(m);bounds.extend(p)}if(markers.length&&done)map.setBounds(bounds)}}for(let id of ['q','item','max','sort'])el(id).addEventListener('input',()=>{el('detail').replaceChildren();render()});el('type').onchange=()=>{itemOptions();el('detail').replaceChildren();render()};el('reset').onclick=()=>{for(let id of ['q','type','max'])el(id).value='';itemOptions();el('item').value='';el('sort').value='name';el('detail').replaceChildren();render()};el('loc').onclick=()=>{if(!map||!navigator.geolocation){alert('현재 위치 기능을 사용할 수 없습니다.');return}navigator.geolocation.getCurrentPosition(p=>{map.setCenter(new kakao.maps.LatLng(p.coords.latitude,p.coords.longitude));map.setLevel(4)},()=>alert('위치 권한을 확인해 주세요.'))};render();function init(){map=new kakao.maps.Map(el('map'),{center:new kakao.maps.LatLng(37.5145,127.106),level:7});for(let s of shops){if(Number.isFinite(s.lat)&&Number.isFinite(s.lng)){positions.set(s.id,new kakao.maps.LatLng(s.lat,s.lng))}}done=true;render()}if(key){let script=document.createElement('script');script.src='https://dapi.kakao.com/v2/maps/sdk.js?autoload=false&appkey='+encodeURIComponent(key);script.onload=()=>{if(window.kakao?.maps?.load)kakao.maps.load(init);else el('map').textContent='카카오맵 설정을 확인해 주세요.'};script.onerror=()=>el('map').textContent='지도 로딩 실패: API 키 및 허용 도메인을 확인해 주세요.';document.head.append(script)}else el('map').textContent='카카오맵 JavaScript 키 설정 후 지도 위치가 표시됩니다. 아래 검색은 지금도 가능합니다.';</script>
<script>
(function(){
  const dialog=document.getElementById('christmas-notice');
  const reopen=document.getElementById('event-reopen');
  const day=new Intl.DateTimeFormat('sv-SE',{timeZone:'Asia/Seoul',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  if(day<'2026-11-19'||day>'2027-01-03')return;
  const storageKey='songpa-christmas-notice-2026-hidden-date';
  let hiddenToday=false;
  try{hiddenToday=localStorage.getItem(storageKey)===day;}catch(e){}
  reopen.hidden=false;
  reopen.onclick=()=>{if(!dialog.open)dialog.showModal();};
  document.getElementById('event-close').onclick=()=>dialog.close();
  document.getElementById('event-hide-today').onclick=()=>{try{localStorage.setItem(storageKey,day);}catch(e){}dialog.close();};
  if(!hiddenToday)dialog.showModal();
})();
</script>
</body></html>'''
page=page.replace('__DATA__',data).replace('__KEY__',json.dumps(str(key)).replace('<','\\u003c'))
components.html(page,height=1100,scrolling=True)
