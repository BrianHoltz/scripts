# recd() - cd again via regular expression
#
# Copyright (C) 2005,2009 Brian Holtz  brian@holtz.org
#
# This software is redistributable under the terms of the
# Creative Commons Attribution-ShareAlike license 2.0
# at http://creativecommons.org/licenses/by-sa/2.0/
#
# --------------------------------------------------------------
#
# recd automatically saves and searches your directory history and bookmarks.
# recd is a "cd" replacement in the same genus as cdargs and gotodir and ecd,
# but doesn't require explicit bookmarking or use of a bookmark menu.
# recd knows where you've been, and uses that knowledge to
# figure out what you mean by "cd foo" when foo isn't a directory.
#
# Usage:
# source recd.sh; alias cd=recd
# cd dir	cd dir and push to DIRSTACK & bookmarks if dest >2 dirs away
# cd pattern	cd to 1st match in DIRSTACK, history & bookmarks
# cd N		cd to Nth element in DIRSTACK
# dirz [-t]	print a [temporally] sorted list of dir history & bookmarks
# dirz N	cd to Nth entry of dirz list
# popdir dir	remove dir from DIRSTACK and bookmarks XXX unimplemented
#
# recd() invokes "builtin cd" and upon success does nothing else except:
# if the destination is >2 pathname components away, it
# 1) bookmarks the destination via a symlink in ~/dirs, and
# 2) pushes OLDPWD onto DIRSTACK and removes any deeper redundant entries.
#
# If "builtin cd" fails, recd() treats $1 as a pattern by which 
# to grep your DIRSTACK, shell history of cd commands, 
# and ~/dirs bookmarks. It pushd's to the most recent match
# and prints up to five alternative matches.
#
# XXX The -L and -P options of builtin cd confuse recd()
# XXX Do not try to pushd to (and maybe even rm) dangling symlinks
#
# 2006-11-03 marca	Diagnose error on extant dir with no permissions
# 2006-12-12 holtz	Fixed cd /
# 2007-02-15 holtz	'cd subdir' was pushdir'ing cuz after cd'ing into subdir,
#			[ -d subdir ] usually is false. The fix: store argWasDir.
# 2009-03-03 holtz	Changed tail +N to tail -n +2 to make Linux happy.
#			Check for $HOME==~ to prevent duplicates in DIRSTACK
# 2009-03-12 holtz	Do not assume ~ is writable
# 
# Efficiency: When "builtin cd" succeeds, the only extra process
# forked is the /bin/ln -s that bookmarks the destination (if $1
# has >2 pathname components). All the other forked commands here
# (grep, tail, head, sed, perl) are only run if "builtin cd" fails
# and so we need to do a search. On my box, the no-search case takes
# about 0.1 sec, and the search case about 0.5 sec, compared to
# 0.01 sec for builtin cd.
#
recd ()
{
	local argWasDir
	if [ -d "$1" ]; then argWasDir=1; fi
	# 2>/dev/null so cd won't complain about things it can't find but recd can
	if builtin cd ${1+"$@"} 2>/dev/null; then
		local slashes=${1//[^\/]} # deletes all non-slashes
		if [ ${#slashes} -gt 2  -o $# -eq 0 -o ! "$argWasDir" \
		     -o "${1:0:1}" == "/" -o "${1:0:1}" == "~" ];
		then
			# dest is interestingly different from PWD,
			# so cd back and pushd
			builtin cd - > /dev/null 2>&1
			pushdir "$OLDPWD"
		fi
		return
	fi
	# if permissions problem, then let cd fail and diagnose error
        if [ -d "$1" ]; then
            builtin cd $1
            return
        fi 	# builtin cd failed. Start searching...
	local target skipAlternatives
	# if the non-numeric part of $1 is empty...
	if [ -z "${1//[0-9]}" ]; then
		# ...then go to Nth DIRSTACK entry
		target=`builtin dirs -l +"$@" 2> /dev/null`
		skipAlternatives=1
	fi
	if [ -z "$target" ]; then
		# tail -n +2 to rule out PWD
		target=`builtin dirs -p -l | tail -n +2 | grep -i "$1" | head -1`
	fi
	# Exact bookmark match takes precedence over history
	# If it also took precedence over DIRSTACK, then putting ~/dirs in
	# CDPATH would be almost equivalent, but PWD would end up as ~/dirs/$1
	if [ -d "~/dirs/$1" ]; then
		target=`/bin/ls -l "~/dirs/$1" | sed 's/.* -> //'`
	fi
	if [ -z "$target" ]; then
		# grep -v to rule out PWD
		target=`dirz -t | grep -v "^$PWD\$" | grep -i "$1" | head -1 | sed -e "s,^~/,$HOME/,"`
	fi
	if [ -z "$target" ]; then
		# Search failed. Let builtin cd fail
		builtin cd ${1+"$@"}
		return
	fi
	# We used our magic, so on success show where we ended up
	pushdir "$target" && pwd
	local returnVal=$?
	if [ $skipAlternatives ]; then return $returnVal; fi
	# Suppress PWD and OLDPWD from search results, via tail + and grep -v
	# Use perl to only print header if there really are alternatives
	( builtin dirs -p -v | tail -n +3 | grep -i "$1"; \
	dirz -t | grep -v "^$OLDPWD\$" | grep -v "^$PWD\$" | grep -i "$1" ) \
	| tail -n +2 | head -5 \
	| perl -pe 'if ($printed eq "") { print "----- alternative recd destinations -----\n"; $printed="1" }'
	return $returnVal
}

# pushdir dir - pushd dir after bookmarking via a symlink in ~/dirs
# Removes other instances of dir from DIRSTACK
# Never puts ~ or / in DIRSTACK
pushdir ()
{
	local dest="$1"
	local basedir="$PWD"
	# XXX if you use .. as other than prefix, you get /../ in link targ
	# while ../ is the prefix of dest...
	while [ ${dest:0:3} == "../" ]; do
		# ...remove last element of basedir and first element of dest
		basedir="${basedir%/*}"
		if [ -z "$basedir" ]; then basedir=/; fi
		dest="${dest:3}"
	done
	# if relative, prepend PWD
	if [ "${dest:0:1}" != "/"  -a "${dest:0:1}" != "~" ]; then
		dest="${basedir}/${dest}"
	fi
	# Cannot usefully link to /
        if [ "$dest" != "/" ]; then
		# ln confused by trailing slash, so delete
		dest="${dest%/}"
		if [ ! -d ~/dirs ] && [ -w ~ ]; then mkdir ~/dirs; fi
		# XXX if ~/dirs/ is prefix of $dest, do not symlink
		if [[ -w ~/dirs ]]; then
			ln -sf "$dest" ~/dirs
		fi
	fi
	# Never put ~ or / in DIRSTACK
	if [ "$PWD" == "$HOME" -o "$PWD" == / ]; then
		if builtin cd "$dest" > /dev/null; then :; else return; fi
	else
		# can fail if $dest is e.g. /lib/modules/$(uname -r)/build
		if builtin pushd "$dest" > /dev/null; then :; else return; fi
	fi
	# remove new pwd from rest of DIRSTACK
	for (( i=${#DIRSTACK[*]}-1; $i > 0; i=$i-1 )); do
		local existingEntry=${DIRSTACK[$i]}
		# $DIRSTACK entries have $HOME not ~, so translate
		if [ $existingEntry != ${existingEntry#$HOME} ]; then
			existingEntry="~${existingEntry#$HOME}"
		fi
		# echo ${DIRSTACK[0]} vs $existingEntry
		if [ "${DIRSTACK[0]}" == "$existingEntry" ]; then
			builtin popd +$i > /dev/null
		fi
	done
}

# dirz [-t]	sort [by time] bookmarked (and interesting historical) dirs
# dirz N	pushdir Nth element of dirz output
dirz ()
{
	# if $1 is numeric
	if [ ! -z "$1" -a -z "${1//[0-9]}" ]; then
		local target=`dirz | tail -n +$1 | head -1 | cut -f 2 | sed -e "s,^~/,$HOME/,"`
		pushdir "$target"
		pwd
		return
	fi
	local ordercmd="sort -u"
	local numbercmd="cat -n"
	if [ "$1" == "-t" ]; then
		# when ordered by time, suppress redundant entries
		ordercmd="perl -ne 'if (! defined \$dirs{ \$_ }) { print \$_; \$dirs{ \$_ } = 1}'"
		numbercmd=cat
	fi
	# grep out absolute cd commands
	# sed away all but the path with no trailing /
	# grep away any uninteresting (< 3 components) paths
	# reverse the list via perl
	# append the bookmark targets via ls
	# replace $HOME with ~, reorder, number, season to taste
	(history \
	| grep '[0-9]  cd [/~]' \
	| sed -e 's/.*  cd //' -e 's,/$,,' \
	| grep '..*/.*/.*/' \
	| perl -e "@lines = <STDIN>; @senil = reverse @lines; print @senil;"; \
	/bin/ls -lt ~/dirs | tail -n +2 | sed 's/.* -> //') \
	| sed -e "s,^$HOME/,~/," | eval $ordercmd | $numbercmd
}
