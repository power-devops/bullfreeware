#!/bin/bash

shopt -s failglob
 
# Print output from failing tests
printf -v sep "%0.s-" {1..80}
for exit_file in t/test-results/*.exit; do
    [ "$(< "$exit_file")" -eq 0 ] && continue
    out_file="${exit_file%exit}out"
    printf '\n%s\n%s\n%s\n' "$sep" "$out_file" "$sep"
    cat "$out_file"
done
exit 1
