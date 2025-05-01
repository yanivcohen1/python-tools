// history of the conversation ( user history (user) and  model respose history (Assistant) )
const chatHistory = [];

async function chat(prompt) {
  chatHistory.push({ role: 'user', content: prompt });

  const fullPrompt = chatHistory.map(msg => {
    return `${msg.role === 'user' ? 'User' : 'Assistant'}: ${msg.content}`;
  }).join('\n') + '\nAssistant:';

  const response = await fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      model: 'mistral',
      prompt: fullPrompt,
      stream: false
    }),
  });

  const result = await response.json();
  chatHistory.push({ role: 'assistant', content: result.response });

  console.log(result.response);
}
