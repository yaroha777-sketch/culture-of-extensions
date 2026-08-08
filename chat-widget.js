(function(){
var BOOK_URL = "https://app.squareup.com/appointments/book/oireayuannjp07/LQYSJW8GJE1Y6/start";
var LEAD_ENDPOINT = "https://formsubmit.co/ajax/cultureofextensions@gmail.com";

var css = `
#coe-chat-btn{position:fixed;bottom:22px;right:22px;z-index:9999;background:#C9B896;color:#141516;
border:none;padding:14px 22px;border-radius:999px;font:500 13px/1 'Jost',system-ui,sans-serif;
letter-spacing:.08em;text-transform:uppercase;cursor:pointer;box-shadow:0 8px 28px rgba(0,0,0,.45);
display:flex;align-items:center;gap:8px;transition:transform .2s,opacity .2s}
#coe-chat-btn:hover{transform:translateY(-2px)}
#coe-chat-btn svg{width:16px;height:16px;flex-shrink:0}
#coe-chat-win{position:fixed;bottom:22px;right:22px;z-index:9999;width:340px;max-width:calc(100vw - 32px);
max-height:min(560px,calc(100vh - 100px));background:#1c1d1f;border:1px solid rgba(201,184,150,.22);
border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,.55);display:none;flex-direction:column;overflow:hidden;
font-family:'Jost',system-ui,sans-serif}
#coe-chat-win.open{display:flex}
#coe-chat-head{background:#151617;padding:16px 18px;display:flex;justify-content:space-between;align-items:center;
border-bottom:1px solid rgba(201,184,150,.16)}
#coe-chat-head span{font-family:'Bodoni Moda',serif;color:#F2EFE7;font-size:15px;letter-spacing:.02em}
#coe-chat-head button{background:none;border:none;color:#b9b5ac;font-size:18px;cursor:pointer;line-height:1;padding:2px 6px}
#coe-chat-head button:hover{color:#C9B896}
#coe-chat-msgs{padding:16px 18px;overflow-y:auto;flex:1;display:flex;flex-direction:column;gap:10px}
.coe-msg{font-size:14.5px;line-height:1.65;padding:11px 14px;border-radius:12px;max-width:88%}
.coe-msg.ai{background:#232427;color:#e5e2d9;align-self:flex-start;border-bottom-left-radius:3px}
.coe-msg.user{background:#C9B896;color:#141516;align-self:flex-end;border-bottom-right-radius:3px}
#coe-quick{display:flex;flex-direction:column;gap:8px;margin-top:2px}
.coe-action{background:transparent;border:1px solid #C9B896;color:#C9B896;padding:11px 14px;border-radius:9px;
cursor:pointer;font:500 13px/1.3 'Jost',sans-serif;letter-spacing:.03em;text-align:center;text-decoration:none;
transition:background .2s,color .2s}
.coe-action:hover{background:#C9B896;color:#141516}
.coe-action.solid{background:#C9B896;color:#141516}
.coe-action.solid:hover{opacity:.85;background:#C9B896}
#coe-chat-inputs{display:none;padding:14px 18px;border-top:1px solid rgba(201,184,150,.16);gap:8px;flex-direction:column}
#coe-chat-inputs input{background:#151617;border:1px solid rgba(201,184,150,.22);border-radius:8px;
padding:11px 12px;color:#F2EFE7;font:400 14px 'Jost',sans-serif;outline:none}
#coe-chat-inputs input:focus{border-color:#C9B896}
#coe-chat-inputs button{background:#C9B896;color:#141516;border:none;padding:11px;border-radius:8px;
font:500 13px 'Jost',sans-serif;letter-spacing:.06em;text-transform:uppercase;cursor:pointer}
#coe-chat-inputs button:hover{opacity:.85}
@media(max-width:420px){#coe-chat-win{right:16px;bottom:16px;width:calc(100vw - 32px)}#coe-chat-btn{right:16px;bottom:16px}}
`;
var style = document.createElement('style'); style.textContent = css; document.head.appendChild(style);

var btn = document.createElement('button');
btn.id = 'coe-chat-btn';
btn.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/></svg>Contact Us';

var win = document.createElement('div');
win.id = 'coe-chat-win';
win.innerHTML = `
<div id="coe-chat-head"><span>Culture of Extensions — Concierge</span><button id="coe-close" aria-label="Close">✕</button></div>
<div id="coe-chat-msgs">
  <div class="coe-msg ai">Welcome to Culture of Extensions! <br><br>Would you like to book a <b>Free Consultation</b> — we'll walk through the process, match your ideal method and hair, and go over pricing — or leave your details so Lana can call you back?</div>
  <div id="coe-quick">
    <button class="coe-action solid" id="coe-book">Book Free Consultation</button>
    <button class="coe-action" id="coe-callback">Request a Call Back</button>
  </div>
</div>
<div id="coe-chat-inputs">
  <input type="text" id="coe-name" placeholder="Your name" autocomplete="name">
  <input type="tel" id="coe-phone" placeholder="Phone number" autocomplete="tel">
  <button id="coe-send">Send</button>
</div>`;

document.body.appendChild(btn);
document.body.appendChild(win);

function toggle(force){
  var open = force !== undefined ? force : !win.classList.contains('open');
  win.classList.toggle('open', open);
}
btn.addEventListener('click', function(){ toggle(); });
win.querySelector('#coe-close').addEventListener('click', function(){ toggle(false); });

function addMsg(text, who){
  var d = document.createElement('div');
  d.className = 'coe-msg ' + who;
  d.innerHTML = text;
  var box = win.querySelector('#coe-chat-msgs');
  box.appendChild(d);
  box.scrollTop = box.scrollHeight;
}

win.querySelector('#coe-book').addEventListener('click', function(){
  win.querySelector('#coe-quick').style.display = 'none';
  addMsg('I\'d like to book a Free Consultation.', 'user');
  setTimeout(function(){
    addMsg('Perfect — choose a time that works for you:<br><br><a href="'+BOOK_URL+'" target="_blank" rel="noopener" class="coe-action solid" style="display:block">Open Booking System</a>', 'ai');
  }, 450);
});

win.querySelector('#coe-callback').addEventListener('click', function(){
  win.querySelector('#coe-quick').style.display = 'none';
  addMsg('I\'d like a call back.', 'user');
  setTimeout(function(){
    addMsg('Of course — leave your name and phone number below and Lana will reach out shortly.', 'ai');
    win.querySelector('#coe-chat-inputs').style.display = 'flex';
    win.querySelector('#coe-name').focus();
  }, 450);
});

async function sendLead(){
  var name = win.querySelector('#coe-name').value.trim();
  var phone = win.querySelector('#coe-phone').value.trim();
  if(!name || !phone){ return; }
  addMsg(name + ' — ' + phone, 'user');
  win.querySelector('#coe-chat-inputs').style.display = 'none';
  setTimeout(function(){
    addMsg('Thank you, ' + name.split(' ')[0] + '! Your details have been received — we\'ll call you soon.', 'ai');
  }, 400);
  var payload = { name: name, phone: phone, page: window.location.href };
  try{
    await fetch('/api/lead', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
  }catch(err){ console.error('Notion lead delivery error:', err); }
  try{
    await fetch(LEAD_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'Accept': 'application/json' },
      body: JSON.stringify({
        name: name, phone: phone,
        _subject: 'New callback request — Culture of Extensions site',
        source: 'Website concierge chat', page: window.location.href
      })
    });
  }catch(err){ console.error('Email lead delivery error:', err); }
}
win.querySelector('#coe-send').addEventListener('click', sendLead);
win.querySelector('#coe-phone').addEventListener('keypress', function(e){ if(e.key==='Enter') sendLead(); });
})();
