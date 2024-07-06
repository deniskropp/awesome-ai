⫻ context:prompt 

The following portions of your message are deemed superfluous or of lesser importance: 

- "You are KickBuzz, the developer for rules-based content generation AI." -- This part introduces your name and role, but it doesn't provide any essential information for the task at hand, which is to identify less relevant portions of the prompt. 

- Specific references to the format you've outlined, such as "with specific sections for context, constants, and content data," are not necessary here as you are already familiar with the format, and this prompt is about identifying less relevant details. 

⫻ const:format @json 
{ 
  "sections": ["context", "constants", "content"], 
  "context_tag": "info", 
  "constant_key": "params" 
} 

⫻ content:input 
Your message in its entirety: 

> Which parts of the prompt are superfluous or less relevant? 
> 
> ⫻ context:prompt 
> 
> You are KickBuzz, the developer for rules-based content generation AI. 
> 
> **Sections:** 
> Start with '⫻', then 'name/type:place', followed by data. 
>
> [...] (rest of the prompt as provided)

⫻ content:output 
Please generate a response identifying any superfluous or less relevant details within my message, adhering to the format outlined in the const:format section