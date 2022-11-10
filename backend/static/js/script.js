function setDate() {
    timeElapsed = Date.now();
    const today = new Date(timeElapsed);
    console.log(today.toDateString())
    document.getElementById("date-today").innerHTML='<p>' + today.toDateString()+ '</p>'
}

setDate()