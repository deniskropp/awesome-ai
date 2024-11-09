import { Ollama } from 'ollama'

const ollama = new Ollama({ host: 'http://127.0.0.1:11434' })


const model = process.argv[2];


process.stdin.setEncoding('utf8');

process.stdin.on('readable', async () => {
    let chunk;

    while ((chunk = process.stdin.read()) !== null) {
        chunk = chunk.replace(/\bpass\b/g, '<fill-in>');

        //console.log('\n\n----', chunk, '----\n\n');

        const parts = chunk.split('<fill-in>');
        const prefix = parts[0];
        const suffix = parts[1];

        console.log('\n\n====');
        console.log(prefix);
        console.log('----');
        console.log(suffix);
        console.log('====');

        const response = await ollama.generate({
            model: model ?? 'codestral',
            raw: true,
            prompt: `<s>[SUFFIX] ${suffix} [PREFIX] ${prefix}`,
            stream: true,
            options: {
                temperature: 0.1,
                num_gpu: 1,
                num_thread: 24,
            },
        });

        for await (const part of response) {
            process.stdout.write(part.response);
        }
    }
});
