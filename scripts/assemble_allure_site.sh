#!/usr/bin/env bash
#
# Assemble the GitHub Pages site for pliskin_june11.
#
# `allure generate` produces a report for ONE run. Publishing that directly
# would wipe every previous report, because actions-gh-pages replaces the
# whole branch. This turns "one run's report" into "the published site".
#
#   In CI:    scripts/assemble_allure_site.sh allure-report gh-pages site "$RUN" 30
#   Locally:  scripts/assemble_allure_site.sh          <- all defaults
#
# Run `allure generate allure-results --clean -o allure-report` first.
#
# Produces:
#   site/index.html      redirect to the newest report
#   site/latest/         the newest report        -> /latest/
#   site/<run>/          this run, archived       -> /42/
#   site/last-history/   what the NEXT run reads to draw trend graphs
#
# Older numbered runs are copied forward from the existing site and pruned to
# the newest KEEP. Plain POSIX-ish shell, so it behaves the same on the CI
# runner and on a Mac.

set -euo pipefail

REPORT="${1:-allure-report}"   # freshly generated report
GH_PAGES="${2:-gh-pages}"      # checkout of the published branch (may not exist)
SITE="${3:-site}"              # what gets published
RUN="${4:-local}"              # run number; "local" when testing by hand
KEEP="${5:-30}"                # how many numbered runs to keep

if [ ! -d "$REPORT" ]; then
    echo "ERROR: '$REPORT' not found." >&2
    echo "Run this first:  allure generate allure-results --clean -o $REPORT" >&2
    exit 1
fi

rm -rf "$SITE"
mkdir -p "$SITE"

# --- carry forward previous runs --------------------------------------------
# Only numeric directories. Copying `latest/` forward would double the site
# size every run, and copying `.git` would confuse the publish step.
if [ -d "$GH_PAGES" ]; then
    for dir in "$GH_PAGES"/*/; do
        [ -d "$dir" ] || continue
        name="$(basename "$dir")"
        case "$name" in
            '' | *[!0-9]*) continue ;;
        esac
        cp -r "$dir" "$SITE/$name"
    done
fi

# --- add this run ------------------------------------------------------------
cp -r "$REPORT" "$SITE/$RUN"

# --- prune to the newest $KEEP ----------------------------------------------
# `head -n -N` would be shorter but it is a GNU extension; this works anywhere.
count="$(find "$SITE" -maxdepth 1 -type d -exec basename {} \; | grep -Ec '^[0-9]+$' || true)"
if [ "$count" -gt "$KEEP" ]; then
    remove=$((count - KEEP))
    find "$SITE" -maxdepth 1 -type d -exec basename {} \; \
        | grep -E '^[0-9]+$' \
        | sort -n \
        | sed -n "1,${remove}p" \
        | while IFS= read -r old; do
            rm -rf "${SITE:?}/${old:?}"
        done
fi

# --- latest ------------------------------------------------------------------
# A copy, not a symlink: GitHub Pages does not follow symlinks.
rm -rf "$SITE/latest"
cp -r "$REPORT" "$SITE/latest"

# --- history for the next run ------------------------------------------------
# This is what makes trend graphs work. The next run copies this back into
# allure-results/history/ before generating, so Allure can see prior outcomes.
rm -rf "$SITE/last-history"
if [ -d "$REPORT/history" ]; then
    cp -r "$REPORT/history" "$SITE/last-history"
else
    echo "NOTE: $REPORT/history is missing -- the next run will have no trend."
fi

# --- root redirect -----------------------------------------------------------
# Without this, the Pages root is a directory listing (or a 404).
cat > "$SITE/index.html" <<'HTML'
<!doctype html>
<meta charset="utf-8">
<meta http-equiv="refresh" content="0; url=./latest/">
<title>Test report</title>
<p><a href="./latest/">Latest test report</a></p>
HTML

echo "Site assembled at $SITE/ :"
ls -1 "$SITE"
echo
echo "View it:  allure open $SITE/latest"
echo "   (do NOT double-click index.html -- file:// blocks the data it loads)"
