#!/bin/bash
set -e

APP_NAME="SnowBlitz_Beta_PlayTest_Demo_0.9.1"
MAIN="main.py"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_ROOT="$ROOT/executable"
WORK_ROOT="$ROOT/build"
SPEC_ROOT="$ROOT/specs"

function copy_assets() {
  TARGET="$1"
  cp -r "$ROOT/assets" "$TARGET"
  cp -r "$ROOT/logs" "$TARGET"
  cp -r "$ROOT/saves" "$TARGET"
}

function cleanup_internal() {
  INTERNAL_DIR="$1/_internal"

  if [ -d "$INTERNAL_DIR" ]; then
    echo "Cleaning up _internal directory..."
    rm -rf "$INTERNAL_DIR/assets"
    rm -rf "$INTERNAL_DIR/logs"
    rm -rf "$INTERNAL_DIR/saves"
  fi
}

function build() {
  echo "Building Linux..."

  TMP_DIST="$DIST_ROOT/linux_tmp"
  FINAL_DIST="$DIST_ROOT/linux"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
    --clean \
    --windowed \
    --name "$APP_NAME" \
    --add-data "$ROOT/assets:assets" \
    --add-data "$ROOT/logs:logs" \
    --add-data "$ROOT/saves:saves" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/linux" \
    --specpath "$SPEC_ROOT/linux"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"
  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
  cleanup_internal "$FINAL_DIST"
}
build

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"
echo "Build completed."
rm -rf executable/_internal/assets