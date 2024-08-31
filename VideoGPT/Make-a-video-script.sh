sys() {
    cat ../.prompts/SyS.prompt
}

sep() {
    echo '\n\n\n'
}

sec() {
    echo "///$1:"
    cat $2
}


cat const_about_Me.klms
sep

sec 'context/prompt' Make-a-video-script.prompt
sep

sec 'content/input' $1
sep

