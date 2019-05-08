# Hyper-prompt
Highly Customize-able prompt for your shell

![header](images/header.gif)

## Requirements

- Python3
- Powerline Fonts : https://github.com/powerline/fonts

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

## Customization Options

### Config File

Hyper prompt will lookup multiple locations for a config file for options on how to display your prompt..

It will first look for a `hyper_prompt.json` in your current project/folder, if it doesn't exists look for `$HOME/.hyper_prompt.json` else finally look for `$HOME/.config/hyper_prompt/config.json`

Use `~/.config/hyper-prompt/config.json` as a config file for customizations.

Example of a default config
```json
"theme": "default",
"mode":"patched",
"segments": [
    "username",
    {
        "type": "virtual",
        # a user built segment which is discoverable via the python path
        "module": "hyper_prompt.segments.virtual"
    }
]
```

### Segments

Segments are the building blocks of hyper-prompt

You can mix and match different segments to build your prompt.

## Troubleshooting

If you continue to have issues, please open an
[issue](https://github.com/artbycrunk/hyper-prompt/issues/new).
