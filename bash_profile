# ~/bin/bash_profile — bash login/interactive shell config
# Canonical location: ~/bin/bash_profile (symlinked from ~/.bash_profile)

eval "$(/opt/homebrew/bin/brew shellenv)"
export PATH="/opt/homebrew/Cellar/scala@2.12/2.12.19/bin:$PATH"

# Added by Toolbox App
export PATH="$PATH:/Users/b0h0166/Library/Application Support/JetBrains/Toolbox/scripts"

source ~/.shellrc.common

# --- History ---
export HISTSIZE=5000
export HISTFILE=~/.bash_history
export HISTFILESIZE=50000
shopt -s histappend
if [[ "$TERM_PROGRAM" == "Apple_Terminal" ]]; then
    PROMPT_COMMAND="update_terminal_cwd; history -a; history -c; history -r"
else
    PROMPT_COMMAND="history -a; history -c; history -r"
fi

# --- Prompt ---
if [[ "$TERMINAL_EMULATOR" == "JetBrains-JediTerm" ]] || [[ "$TERM_PROGRAM" == "JetBrains-JediTerm" ]]; then
    export PS1="\$ "
else
    export whoami=$(whoami | sed 's/b0h0166/BH/')
    export hostname=$(hostname | sed 's/m-c02xf1jsjgh7/mac/' | sed 's/m-c47v699ryp/mac/' | sed 's/qualityengpdp00-ien1-contentquality-1/CQGCP/')
    export hostname=$(echo $hostname | sed 's/\(......\).*\(..\)/\1..\2/')
    export PS1="\[\e[0;7m\]${whoami}@${hostname}\[\e[m\] \[\e[0;31m\]\D{%m-%d} \A\[\e[0m\] \[\e[0;32m\]\W\$\[\e[0m\] "
fi

# --- Aliases ---
alias sb="source ~/.bash_profile"
alias ff="find . -name"
alias trimparquet="~/bin/trimparquet/trim_parquet_env/bin/python ~/bin/trimparquet/trim.py"
