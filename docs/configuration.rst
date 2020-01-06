===========================
Configuration
===========================


Configuration File
===========================

Hyper prompt will lookup multiple locations for a config file.
The config file provides options on how to display the prompt.

A valid config will be looked up in the following order.

* $PWD/hyper_prompt.json
* $HOME/.hyper_prompt.json
* $HOME/.config/hyper_prompt/config.json

Note: If no config file is available the fallback is a hardcoded default list of segments.

Example config::

      "theme": "default",
      "mode":"patched",
      "segments": [
          "username",
          {
              "type": "virtual",
              // a user built segment which is discoverable via the python path
              "module": "hyper_prompt.segments.virtual"
          }
      ]


Shell Configuration
===========================

Bash
----------------------------

Add the following to your `.bashrc` file::

      function _update_ps1() {
          PS1=$(hyper-prompt $?)
      }

      if [[ $TERM != linux && ! $PROMPT_COMMAND =~ _update_ps1 ]]; then
          PROMPT_COMMAND="_update_ps1; $PROMPT_COMMAND"
      fi

Zsh
----------------------------

Add the following to your `.zshrc`::

      function prompt_precmd() {
          PS1="$(hyper-prompt --shell zsh $?)"
      }

      function add_prompt_precmd() {
        for s in "${precmd_fn[@]}"; do
          if [ "$s" = "prompt_precmd" ]; then
            return
          fi
        done
        precmd_fn+=(prompt_precmd)
      }

      if [ "$TERM" != "linux" ]; then
          add_prompt_precmd
      fi

Fish
----------------------------

Add the following to your `~/.config/fish/config.fish`::

      function fish_prompt
          hyper-prompt --shell bare $status
      end

Tcsh
----------------------------

Add the following to your `.tcshrc`::

      alias precmd 'set prompt="`hyper-prompt --shell tcsh $?`"'

