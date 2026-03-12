# ~/bin/zprofile — zsh login shell config
# Canonical location: ~/bin/zprofile (symlinked from ~/.zprofile)
# Runs once per login shell, after /etc/zprofile (which runs path_helper)

eval "$(/opt/homebrew/bin/brew shellenv)"
export PATH="/opt/homebrew/Cellar/scala@2.12/2.12.19/bin:$PATH"

# Added by Toolbox App
export PATH="$PATH:/Users/b0h0166/Library/Application Support/JetBrains/Toolbox/scripts"
