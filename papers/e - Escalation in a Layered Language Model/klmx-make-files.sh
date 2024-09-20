#!/usr/bin/env -S bash -e
# -c 'cat $1 2>/dev/null | exec sc -t es2015 - && exec node $0.js $@ && rm $0.js'

sys() {
    cat ./SyS.prompt
}

sep() {
    echo -e '\n\n\n'
}

sec() {
    echo "⫻$1:$2"
    cat $2
}

content() {
    echo "⫻content"
    echo "$1"
}


sys
sep

cat const_about_Me.klms
sep

sec 'context/file' 'v1/v1_gemini.md'
sep

sec 'context/file' 'v2/v2_gemini.md'
sep

sec 'context/file' 'v3/v3_gemini.md'
sep

sec 'context/file' 'v4/v4_gemini.md'
sep

sec 'context/file' 'v5/v5_gemini.md'
sep

content 'Come up with a v6 of the paper'
