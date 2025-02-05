function streamResponse(prompt) {
    const apiUrl = 'http://localhost:11434/api/generate';

    const data = {
        model: 'llama3:70b',
        stream: true,
        temperature: 0.7,
        max_tokens: -1,
        messages: [
            { role: 'system', content: 'You are a helpful assistant.' },
            { role: 'user', content: prompt }
        ]
    };

    responseContainer.innerHTML = '';

    fetch(apiUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        function read() {
            reader.read().then(({ done, value }) => {
                if (done) {
                    return;
                }
                const text = decoder.decode(value, { stream: true });
                responseContainer.innerHTML += text;
                read();
            });
        }

        read();
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
