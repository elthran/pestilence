#!/usr/bin/env bash
# Set the current directory so that all paths are consistent.
move_to_base() {
    script_dir=$1
    pushd ${script_dir}/.. > /dev/null
}

return_from_base () {
    popd > /dev/null
}

# generate a random password, default is 32 chars
# alterante usage is `randpw 16` (or whatever)
randpw() {
    < /dev/urandom tr -dc "[:alnum:]" | head -c${1:-${1-32}}; echo;
}

# strip leading whitespace
rstrip() {
    sed -e 's/^[ \t]*//' | sed '0,/^$/{//d}'
}

package_exists() {
    return dpkg -l "$1" &> /dev/null
}
