import { readFileSync } from 'fs'
import { OpenAI } from 'openai'

const openai = new OpenAI({
    apiKey: process.env.AIML_API_KEY,
    baseURL: 'https://api.aimlapi.com/v1'
})


const messages = [
    {
        role: 'system' as const,
        content: readFileSync('./FizzEase/prompt/System Instructions.txt', 'utf-8')
    }
]

const main = async () => {
    const streamingParams: OpenAI.Chat.ChatCompletionCreateParams = {
        model: 'mistralai/Mistral-7B-Instruct-v0.3',
        messages: messages,
        temperature: 0.7,
        //max_tokens: 500,
        stream: true as const,
    };
    const chatCompletion = await openai.chat.completions.create(streamingParams);

    for await (const chunk of chatCompletion) {
        process.stdout.write(chunk.choices[0]?.delta?.content || '')
    }
}


main()
