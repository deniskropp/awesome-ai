from openai import OpenAI


class Qlloma:
    def __init__(self):
        self.client = OpenAI(
            base_url="http://localhost:8080/v1",
            api_key=""
        )

    def generate_response(self, prompt, options):
        response = self.client.chat.completions.create(
            model="Qwen2.5-7B-Instruct-Q4_K_M.gguf",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            stream=True,
            max_tokens=200,
        )
        for chunk in response:
            if chunk.choices[0].delta.content is not None:
                print(
                    chunk.choices[0].delta.content,
                    end="",
                    flush=True,
                )
        print("\n")
