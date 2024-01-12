// Nehmen wir an, Sie haben ein Objekt mit den Daten, die aktualisiert werden sollen
let socket = new WebSocket("ws://localhost:6789");

socket.onmessage = function(event) {

    let data = JSON.parse(event.data);
    changeOverlayDuo(data)
    setWidthOfRankedOverlay(data.name, data.division)
};





function changeOverlayDuo(data) {
    if (data.division == "Master" || data.division == "Grandmaster" || data.division == "Challenger") {
        document.getElementById("rank-tier-duo").textContent = "";
    }
    else {
        document.getElementById("rank-tier-duo").textContent = data.rank;
    }
    document.getElementById("rank-division-duo").textContent = data.division;
    if (data.division == "Unranked"){
        document.getElementById("rank-lp-duo").textContent ="";
    }
    else {
        document.getElementById("rank-lp-duo").textContent = data.lp+"lp";
    }
    document.getElementById("profile-link-duo").textContent = "www.op.gg/summoners/euw/" + data.player;
    document.getElementById("player-name-duo").textContent = data.player;
    document.getElementById("wins-duo").textContent = data.wins
    document.getElementById("losses-duo").textContent = data.losses
    document.getElementById("perc-wr-duo").textContent = data.session_wr +"%"
    changePlayerColor(data.division)
    changeRankIcon(data.division)
    setWinRateColor(data.wins, data.losses)

}

function changeRankIcon(division) {

    icon = document.getElementById("divison-icon-duo");
    icon.src="..\\overlay\\rank_icons\\"+division+".png";
}

function changePlayerColor(division){

        const player_name = document.getElementById("player-name-duo")
        const color = setColorByDivision(division)
        player_name.style.color=color
}

function setWinRateColor(wins, losses){
    if(wins == 0 && losses == 0){
        document.getElementById("perc-wr-duo").style.color = "rgb(255, 255, 255)"
        document.getElementById("perc-wr").style.color = "rgb(255, 255, 255)"
    }
    if(wins < losses){
        document.getElementById("perc-wr-duo").style.color = "rgb(220, 20, 60)"
        document.getElementById("perc-wr").style.color = "rgb(220, 20, 60)"
    }
    else {
        document.getElementById("perc-wr-duo").style.color = "rgb(11, 218, 81)"
        document.getElementById("perc-wr").style.color = "rgb(11, 218, 81)"
    }
}


function setWidthOfRankedOverlay(name){

        if(name.length <= 14){
            width = 445
        }
        else{
            width = 445 + (len(name) - 14)*10
        }
        document.getElementById("overlay-duo").style.width = width+"px"
        document.getElementById("session-overlay-duo").style.width = width+"px"
}


function setColorByDivision(division) {
    let color;

    switch (division) {
        case 'Iron':
            color = "rgb(150, 144, 145)";
            break;
        case 'Bronze':
            color = "rgb(182, 145, 137)";
            break;
        case 'Silver':
            color = "rgb(207, 207, 207)";
            break;
        case 'Gold':
            color = "rgb(216, 193, 93)";
            break;
        case 'Platinum':
            color = "rgb(54, 163, 194)";
            break;
        case 'Emerald':
            color = "rgb(118, 218, 140)";
            break;
        case 'Diamond':
            color = "rgb(152, 193, 255)";
            break;
        case 'Master':
            color = "rgb(218, 142, 228)";
            break;
        case 'Grandmaster':
            color = "rgb(233, 130, 130)";
            break;
        case 'Challenger':
            color = "rgb(186, 255, 249)";
            break;
        default:
            color = "white"
    }

    return color;
}