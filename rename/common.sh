#!/bin/bash

# 解析 --profile / CONFUSE_PROFILE，并加载 profiles/<name>/rename.env

resolve_confuse_profile() {
    local profile="${CONFUSE_PROFILE:-default}"
    local arg
    for arg in "$@"; do
        case "$arg" in
            --profile=*)
                profile="${arg#--profile=}"
                ;;
            --profile)
                echo "missing value for --profile" >&2
                exit 1
                ;;
        esac
    done

    local index=1
    while [[ $index -le $# ]]; do
        if [[ "${!index}" = "--profile" ]]; then
            local next=$((index + 1))
            if [[ $next -gt $# ]]; then
                echo "missing value for --profile" >&2
                exit 1
            fi
            profile="${!next}"
        fi
        index=$((index + 1))
    done

    echo "$profile"
}

load_rename_profile() {
    CONFUSE_PROFILE="$(resolve_confuse_profile "$@")"
    export CONFUSE_PROFILE

    local profile_file="$CONFUSE_PATH/profiles/$CONFUSE_PROFILE/rename.env"
    if [[ ! -f "$profile_file" ]]; then
        echo "Profile not found: $profile_file" >&2
        exit 1
    fi
    # shellcheck disable=SC1090
    source "$profile_file"
}
