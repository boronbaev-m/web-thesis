const startBtn = document.getElementById('start');
startBtn.addEventListener('click', () => {
    window.scrollTo({
        top: document.body.scrollHeight,
        behavior: 'smooth'
    });
});

const codeForm = document.getElementById('codeForm');
codeForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const code = document.getElementById('codeInput').value;

    const response = await fetch('/submit', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ code }),
    });

    const result = await response.json();
    window.location.href = `/result.html?job_id=${result.job_id}`;
});
