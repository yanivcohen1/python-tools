[ollama api URL](https://github.com/ollama/ollama-js/tree/main)

# Getting Started

# with node
```js 
npm i ollama
import ollama from 'ollama'
```

# without node
```js 
import ollama from 'ollama/browser'
```

# Streaming responses
```js 
import ollama from 'ollama'

const message = { role: 'user', content: 'Why is the sky blue?' }
const response = await ollama.chat({ model: 'llama3.1', 
                              messages: [message], stream: true })
for await (const part of response) {
  process.stdout.write(part.message.content)
}
```

