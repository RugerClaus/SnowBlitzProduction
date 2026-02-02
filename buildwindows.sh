#!/bin/bash
set -e

APP_NAME="SnowBlitz_Beta_PlayTest_Demo_0.9.1"
MAIN="main.py"

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DIST_ROOT="$ROOT/executable"
WORK_ROOT="$ROOT/build"
SPEC_ROOT="$ROOT/specs"

ASSETS_PATH="$ROOT/assets"
LOGS_PATH="$ROOT/logs"
SAVES_PATH="$ROOT/saves"

convert_to_windows_path() {
  local unix_path="$1"
  echo "$(cygpath -w "$unix_path")"
}

# Convert paths
ASSETS_PATH_WIN=$(convert_to_windows_path "$ASSETS_PATH")
LOGS_PATH_WIN=$(convert_to_windows_path "$LOGS_PATH")
SAVES_PATH_WIN=$(convert_to_windows_path "$SAVES_PATH")

function copy_assets() {
  TARGET="$1"
  cp -r "$ASSETS_PATH" "$TARGET"
  cp -r "$LOGS_PATH" "$TARGET"
  cp -r "$SAVES_PATH" "$TARGET"
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
  echo "Building Windows..."

  TMP_DIST="$DIST_ROOT/windows_tmp"
  FINAL_DIST="$DIST_ROOT/windows"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
    --clean \
    --windowed \
    --name "$APP_NAME" \
    --add-data "$ASSETS_PATH_WIN;assets" \
    --add-data "$LOGS_PATH_WIN;logs" \
    --add-data "$SAVES_PATH_WIN;saves" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/windows" \
    --specpath "$SPEC_ROOT/windows"

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
rm -rf "$DIST_ROOT/_internal/assets"
