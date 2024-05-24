const startBtn = document.getElementById('start')
startBtn.addEventListener('click', () => {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
})

const form = document.getElementById('form')
form.addEventListener('submit', async (e) => {
    e.preventDefault()

    const submitBtn = e.target[1]

    submitBtn.textContent = 'Loading'
    submitBtn.disabled = true

    try {
        const response = await fetch('http://127.0.0.1:5000/submit', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ code: e.target[0].value })
        })
        if (response.ok) {
            const data = await response.json()
            alert(JSON.stringify(data))
            localStorage.setItem('message', data.result);
            const url = new URL(window.location.href);
            url.pathname = `result.html`;

            window.location.href = `result.html`;
        } else {
            alert('error');
        }
    } catch (e) {
        alert('error');
    }

    submitBtn.textContent = 'Check code'
    submitBtn.disabled = false
    // const data = {jobId: 1}
    //
    // const url = new URL(window.location.href);
    // url.pathname = `result.html`;
    //
    // window.location.href = `result.html?jobId=${data?.jobId}`;
})