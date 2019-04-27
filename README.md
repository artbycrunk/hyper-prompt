# Hyper-prompt
Highly Customize-able prompt for your shell

## Setup

```bash
git clone https://github.com/artbycrunk/hyper-prompt
cd hyper-prompt
python setup.py install
```

### Bash

Add the following to your `.bashrc` file:

```bash
function _update_ps1() {
    PS1=$(hyper-prompt $?)
}

if [[ $TERM != linux && ! $PROMPT_COMMAND =~ _update_ps1 ]]; then
    PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
fi
```

### tcsh

Add the following to your `.tcshrc`:

```bash
alias precmd 'set prompt="`hyper-prompt --shell tcsh $?`"'
```

## Customization

### Config File

Use `~/.config/hyper-prompt/config.json` as a config file for customizations.

Example of a default config
```
"theme": "default",
"mode":"patched",
"segments": [
    "username",
    {
        "type": "virtual",
        "module": "hyper_prompt.segments.virtual"
    }
]
```

### Segmets

Segments are the building blocks of hyper-prompt

You can mix and match different segments to build your prompt.

## Troubleshooting

If you continue to have issues, please open an
[issue](https://github.com/artbycrunk/hyper-prompt/issues/new).
