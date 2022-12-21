function setDate() {
    timeElapsed = Date.now();
    const today = new Date(timeElapsed);
    console.log(today.toDateString())
    document.getElementById("date-today").innerHTML = '<p>' + today.toDateString() + '</p>'
}

setDate()


setTimeout(() => {
    const box = document.getElementsByClassName('messages-container');

    // 👇️ removes element from DOM
    box.style.display = 'none';

    // 👇️ hides element (still takes up space on page)
    // box.style.visibility = 'hidden';

}, 3000);