# ~/bin/zshrc — zsh interactive shell config
# Canonical location: ~/bin/zshrc (symlinked from ~/.zshrc)

source ~/.shellrc.common

# --- Prompt ---
if [[ "$TERMINAL_EMULATOR" == "JetBrains-JediTerm" ]] || [[ "$TERM_PROGRAM" == "JetBrains-JediTerm" ]]; then
    PROMPT='%# '
else
    export whoami=$(whoami | sed 's/b0h0166/BH/')
    export hostname=$(hostname | sed 's/m-c02xf1jsjgh7/mac/' | sed 's/m-c47v699ryp/mac/' | sed 's/qualityengpdp00-ien1-contentquality-1/CQGCP/')
    export hostname=$(echo $hostname | sed 's/\(......\).*\(..\)/\1..\2/')
    PROMPT=$'%{\e[7m%}'$whoami@$hostname$'%{\e[0m%} %{\e[0;31m%}%D{%m-%d %H:%M} %{\e[0;32m%}%1~%{\e[0m%} %# '
fi

# --- History ---
setopt share_history
setopt inc_append_history
unsetopt hist_ignore_all_dups
setopt EXTENDED_HISTORY
HISTSIZE=50000
SAVEHIST=$HISTSIZE
HISTFILE=~/.zsh_history

# --- Misc ---
TIMEFMT=$'real=%*E\tuser=%*U\tsys=%*S'
alias axbrew='arch -x86_64 /usr/local/homebrew/bin/brew'
