// static/script.js

document.addEventListener("DOMContentLoaded", () => {

    let btn = document.getElementById("loveBtn");

    let music = document.getElementById("music");

    let beat = document.getElementById("beat");

    let uploadedImages = document.body.dataset.images;

    if (uploadedImages) {

        let parsed = JSON.parse(uploadedImages);

        images = parsed.map(
            img => "/static/uploads/" + img
        );

        console.log(images);
    }

    createStars();

    createRain();

    if (btn) {

        let name = JSON.parse(btn.dataset.name);

        btn.onclick = () => {

            startLove(name);

            music?.play().catch(() => {});

            beat?.play().catch(() => {});
        };
    }
});


/* MAIN LOVE MESSAGE */

function startLove(name){

    let msg = document.getElementById("message");

    msg.innerHTML = "";

    let text =
    `Hey ${name} Baby I don’t need anything perfect—having you around already feels like enough. I love you so much ❤️`;

    let i = 0;

    function type(){

        if(i < text.length){

            msg.innerHTML += text.charAt(i);

            i++;

            setTimeout(type,45);
        }
    }

    type();

    startSlideshow();

    startHearts();

    enableNoButtonEscape();

    setTimeout(() => {

        let box = document.getElementById("finalBox");

        if(box){

            box.style.display = "block";
        }

    },8000);
}


/* SLIDESHOW */

let images = [];

let index = 0;

function startSlideshow(){

    let img = document.getElementById("slideshow");

    if(!img || images.length === 0) return;

    function change(){

        img.classList.remove("show");

        setTimeout(() => {

            img.src = images[index];

            img.classList.add("show");

            index = (index + 1) % images.length;

        },400);
    }

    change();

    setInterval(change,3500);
}


/* HEARTS */

function startHearts(){

    setInterval(() => {

        let h = document.createElement("div");

        h.innerHTML = "❤️";

        h.className = "heart";

        h.style.left =
        Math.random() * 100 + "vw";

        h.style.fontSize =
        (14 + Math.random() * 18) + "px";

        document.body.appendChild(h);

        setTimeout(() => h.remove(),4000);

    },600);
}


/* STARS */

function createStars(){

    for(let i=0;i<120;i++){

        let star = document.createElement("div");

        star.className = "star";

        star.style.left =
        Math.random() * 100 + "vw";

        star.style.top =
        Math.random() * 100 + "vh";

        star.style.animationDuration =
        (1 + Math.random() * 2) + "s";

        document.body.appendChild(star);
    }
}


/* RAIN */

function createRain(){

    for(let i=0;i<140;i++){

        let r = document.createElement("div");

        r.className = "rain";

        r.style.left =
        Math.random() * 100 + "vw";

        r.style.animationDuration =
        (0.6 + Math.random() * 1.2) + "s";

        r.style.opacity = Math.random();

        document.body.appendChild(r);
    }
}


/* NO BUTTON */

function enableNoButtonEscape(){

    let btn =
    document.getElementById("noBtn");

    if(!btn) return;

    btn.style.position = "fixed";

    function move(){

        let x =
        Math.random() *
        (window.innerWidth - 100);

        let y =
        Math.random() *
        (window.innerHeight - 100);

        btn.style.left = x + "px";

        btn.style.top = y + "px";
    }

    btn.addEventListener("mouseenter", move);

    btn.addEventListener("touchstart", move);

    setInterval(move,2000);
}


/* YES BUTTON */

function yesClicked(){

    alert("I knew it babyyy ❤️");
}