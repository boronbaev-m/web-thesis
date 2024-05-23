const startBtn = document.getElementById('start')
startBtn.addEventListener('click', () => {
    console.log("clicked")
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
})

const form = document.getElementById('form')
form.addEventListener('submit', (e) => {
    e.preventDefault()
    console.log("submit")

    // fetch('http://127.0.0.1:5000/submit', {
    //     method: 'POST',
    //     headers: { 'Content-Type': 'application/json' },
    //     body: JSON.stringify({ code: e.target[0].value })
    // }).then(response => {
    //     if (response.ok) {
    //         return response.json();
    //     }
    //     throw new Error('Network response was not ok.');
    // })
    //     .then(data => {
    //         console.log(data);
    //     })
})