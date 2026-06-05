from flask import Flask, request, render_template_string
import requests
import re

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HACKER TRACKER</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>

/* MATRIX BACKGROUND */

#matrix{
position:fixed;
top:0;
left:0;
width:100%;
height:100%;
z-index:-5;
opacity:0.25;
}

/* BUILT BY SHASHI */

.creator{
position:fixed;
bottom:15px;
right:15px;
padding:10px 18px;
border-radius:12px;

background:rgba(0,0,0,0.5);
backdrop-filter:blur(8px);

border:1px solid #00f7ff;

color:#00f7ff;
font-size:13px;
font-weight:bold;

box-shadow:
0 0 10px #00f7ff,
0 0 20px #00f7ff;

animation:creatorGlow 2s infinite alternate;
}

@keyframes creatorGlow{
from{
transform:scale(1);
opacity:.8;
}
to{
transform:scale(1.05);
opacity:1;
}
}


@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700&display=swap');

*{
margin:0;
padding:0;
box-sizing:border-box;
font-family:'Orbitron',sans-serif;
}

body{
background:#050816;
overflow-x:hidden;
color:white;
}

/* ANIMATED BACKGROUND */

body::before{
content:"";
position:fixed;
top:0;
left:0;
width:100%%;
height:100%%;
background:
radial-gradient(circle at top left,#00f7ff22,transparent 30%%),
radial-gradient(circle at bottom right,#ff00ff22,transparent 30%%),
#050816;
z-index:-2;
}

/* PARTICLE GLOW */

body::after{
content:"";
position:fixed;
width:100%%;
height:100%%;
background-image:
radial-gradient(#00f7ff 1px, transparent 1px);
background-size:35px 35px;
opacity:0.15;
animation:movebg 20s linear infinite;
z-index:-1;
}

@keyframes movebg{
0%%{
transform:translateY(0px);
}
100%%{
transform:translateY(35px);
}
}

/* TITLE */

.title{
text-align:center;
font-size:38px;
font-weight:700;
margin-top:25px;
margin-bottom:20px;
color:#00f7ff;
text-shadow:
0 0 10px #00f7ff,
0 0 20px #00f7ff,
0 0 40px #00f7ff;
animation:glow 1s infinite alternate;
}

@keyframes glow{
from{
opacity:0.7;
}
to{
opacity:1;
}
}

/* CONTAINER */

.container{
width:95%%;
max-width:520px;
margin:auto;
padding:20px;
}

/* GLASS CARD */

.card{
background:rgba(255,255,255,0.05);
backdrop-filter:blur(12px);
border:1px solid rgba(255,255,255,0.1);
padding:20px;
border-radius:18px;
margin-top:18px;
box-shadow:
0 0 20px rgba(0,247,255,0.3);
transition:0.3s;
animation:cardEntry 0.8s ease;
}

@keyframes cardEntry{
from{
opacity:0;
transform:translateY(50px);
}
to{
opacity:1;
transform:translateY(0);
}
}

.card:hover{
transform:translateY(-3px);
box-shadow:
0 0 30px rgba(0,247,255,0.5);
}


/* =========================
   MOBILE RESPONSIVE DESIGN
   ========================= */

@media screen and (max-width:768px){

.container{
width:100%;
padding:12px;
}

.title{
font-size:26px;
margin-top:15px;
}

.card{
padding:15px;
border-radius:14px;
}

input{
font-size:15px;
padding:13px;
}

button{
padding:13px;
font-size:15px;
}

.info{
font-size:15px;
line-height:28px;
}

#map{
height:250px;
}

.creator{
right:8px;
bottom:8px;
font-size:11px;
padding:8px 12px;
}

}

@media screen and (max-width:480px){

.title{
font-size:22px;
}

.card{
padding:12px;
}

input{
font-size:14px;
padding:12px;
}

button{
font-size:14px;
padding:12px;
}

#map{
height:220px;
}

.creator{
font-size:10px;
padding:6px 10px;
}

}


/* INPUT */

input{
width:100%%;
padding:15px;
margin-top:10px;
border:none;
outline:none;
border-radius:12px;
background:rgba(255,255,255,0.08);
color:white;
font-size:16px;
border:1px solid rgba(0,247,255,0.5);
box-shadow:0 0 10px rgba(0,247,255,0.2);
}

input::placeholder{
color:#9befff;
}

/* BUTTON */

button{
width:100%%;
padding:15px;
margin-top:15px;
border:none;
border-radius:12px;
background:linear-gradient(90deg,#00f7ff,#7a00ff);
color:white;
font-size:17px;
font-weight:bold;
cursor:pointer;
transition:0.3s;
box-shadow:
0 0 15px rgba(0,247,255,0.5);
}

button:hover{
transform:scale(1.04);
box-shadow:
0 0 25px rgba(0,247,255,0.8);
}

/* MAP */

#map{
height:320px;
border-radius:18px;
margin-top:15px;
overflow:hidden;
border:2px solid rgba(0,247,255,0.6);
box-shadow:
0 0 20px rgba(0,247,255,0.4);
}

/* DISTANCE */

#distance{
margin-top:15px;
text-align:center;
font-size:20px;
font-weight:bold;
color:#00f7ff;
text-shadow:
0 0 10px #00f7ff;
}

/* INFO */

.info{
line-height:34px;
font-size:17px;
}

/* FOOTER */

.footer{
text-align:center;
margin-top:18px;
font-size:13px;
color:#9befff;
opacity:0.8;
}

</style>

</head>
<div class="title">
⚡ SHASHI CYBER CONSOLE ⚡
</div>
<body>

<div class="container">

<div class="card">
<form method="POST">
<input
type="text"
name="number"
placeholder=" TARGET NUMBER "
required
style="
text-align:center;
letter-spacing:2px;
font-weight:bold;
">

<button>☠ ACCESS NOW ☠</button>
</form>
</div>

{% if data %}
<div class="card info">

<div style="
text-align:center;
font-size:22px;
margin-bottom:20px;
color:#00f7ff;
text-shadow:0 0 15px #00f7ff;
font-weight:bold;
">
⚡ TARGET INFORMATION ⚡
</div>

<div style="
padding:15px;
border-radius:15px;
background:rgba(0,0,0,0.4);
border:1px solid rgba(0,247,255,0.5);
box-shadow:0 0 15px rgba(0,247,255,0.3);
">

<p style="margin-bottom:18px;">
<span style="color:#00f7ff;">👤 NAME :</span><br>
<span style="
font-size:20px;
font-weight:bold;
color:white;
">
{{data.name}}
</span>
</p>

<p style="margin-bottom:18px;">
<span style="color:#00f7ff;">📱 MOBILE :</span><br>
<span style="
font-size:20px;
font-weight:bold;
color:white;
">
{{data.mobile}}
</span>
</p>

<p>
<span style="color:#00f7ff;">📍 LOCATION :</span><br>
<span style="
font-size:17px;
line-height:30px;
color:#d7faff;
">
{{data.address}}
</span>
</p>

</div>

</div>


{% endif %}

</div>

<script>
let map = L.map('map').setView([20.59,78.96],5);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

let address = document.getElementById("addr")?.innerText;

if(address){

navigator.geolocation.getCurrentPosition(function(pos){

let userLat = pos.coords.latitude;
let userLng = pos.coords.longitude;

L.marker([userLat,userLng]).addTo(map).bindPopup("You");

fetch("https://nominatim.openstreetmap.org/search?format=json&q="+encodeURIComponent(address))
.then(res=>res.json())
.then(d=>{

if(d.length>0){

let lat = d[0].lat;
let lon = d[0].lon;

L.marker([lat,lon]).addTo(map).bindPopup("Target");

L.polyline([[userLat,userLng],[lat,lon]],{color:"blue"}).addTo(map);

map.fitBounds([[userLat,userLng],[lat,lon]]);

// distance
function dist(a,b,c,d){
let R=6371;
let dLat=(c-a)*Math.PI/180;
let dLon=(d-b)*Math.PI/180;
let x=Math.sin(dLat/2)**2+
Math.cos(a*Math.PI/180)*Math.cos(c*Math.PI/180)*
Math.sin(dLon/2)**2;
return R*2*Math.atan2(Math.sqrt(x),Math.sqrt(1-x));
}

let km = dist(userLat,userLng,lat,lon);

document.getElementById("distance").innerHTML="📏 Distance: "+km.toFixed(2)+" KM";

}

});

});

}
</script>

<div class="creator">
    ⚡ BUILT BY SHASHI.MULI ⚡
</div>

<canvas id="matrix"></canvas>

<script>
const canvas = document.getElementById("matrix");
const ctx = canvas.getContext("2d");

canvas.height = window.innerHeight;
canvas.width = window.innerWidth;

const letters =
"01ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&@";
const fontSize = 14;
const columns = canvas.width / fontSize;

const drops = [];

for(let i=0;i<columns;i++){
    drops[i]=1;
}

function draw(){

    ctx.fillStyle="rgba(5,8,22,0.08)";
    ctx.fillRect(0,0,canvas.width,canvas.height);

    ctx.fillStyle="#00f7ff";
    ctx.font=fontSize+"px monospace";

    for(let i=0;i<drops.length;i++){

        const text =
        letters[Math.floor(
        Math.random()*letters.length)];

        ctx.fillText(
        text,
        i*fontSize,
        drops[i]*fontSize
        );

        if(
        drops[i]*fontSize > canvas.height &&
        Math.random() > 0.975
        ){
            drops[i]=0;
        }

        drops[i]++;
    }
}

setInterval(draw,33);

window.addEventListener("resize",()=>{
    canvas.width=window.innerWidth;
    canvas.height=window.innerHeight;
});
</script>


</body>
</html>
"""

# ===== ONLY NEW API =====
def fetch_data(number):
    try:
        url = f"https://exploitsindia.site/track/live.php?term={number}"
        res = requests.get(url, timeout=10).text

        def get(pattern):
            m = re.search(pattern, res)
            return m.group(1).strip() if m else "N/A"

        return {
            "name": get(r"Name[:\-]?\s*(.*)"),
            "mobile": number,
            "address": get(r"Address[:\-]?\s*(.*)")
        }

    except:
        return None

@app.route("/", methods=["GET","POST"])
def home():
    data = None

    if request.method == "POST":
        number = request.form.get("number")
        data = fetch_data(number)

    return render_template_string(HTML, data=data)
if __name__ == "__main__":
    print("""
          
███████╗██╗  ██╗ █████╗ ███████╗██╗  ██╗██╗
██╔════╝██║  ██║██╔══██╗██╔════╝██║  ██║██║
███████╗███████║███████║███████╗███████║██║
╚════██║██╔══██║██╔══██║╚════██║██╔══██║██║
███████║██║  ██║██║  ██║███████║██║  ██║██║
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ DEVELOPER BY SHASHI ⚡
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SERVER STARTING...
""")
    
    app.run(host="0.0.0.0", port=5000)