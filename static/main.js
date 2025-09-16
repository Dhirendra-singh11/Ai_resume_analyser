const atsElm=document.getElementsByClassName("ats-score")[0]
const ats=parseInt(atsElm.textContent.replace(/\D/g,''),10)

const circumference=2*Math.PI*45;

const donut=document.getElementById('donut')
donut.style.strokeDasharray = circumference;
donut.style.strokeDashoffset = circumference;


const offset = circumference - (ats / 100) * circumference;

setTimeout(() => {donut.style.strokeDashoffset = offset;}, 300);

if (ats >= 70) {
                donut.style.stroke = '#4caf50';
            } else if (ats>= 40) {
                donut.style.stroke = '#ff9800';
            } else {
                donut.style.stroke = '#f44336';
            }