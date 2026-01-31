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

function build_linux() {
  echo "Building Linux..."

  TMP_DIST="$DIST_ROOT/linux_tmp"
  FINAL_DIST="$DIST_ROOT/linux"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
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
}

function build_windows() {
  echo "Building Windows..."

  TMP_DIST="$DIST_ROOT/windows_tmp"
  FINAL_DIST="$DIST_ROOT/windows"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
    --name "$APP_NAME.exe" \
    --add-data "$ROOT/assets;assets" \
    --add-data "$ROOT/logs;logs" \
    --add-data "$ROOT/saves;saves" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/windows" \
    --specpath "$SPEC_ROOT/windows"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"
  mv "$TMP_DIST/$APP_NAME.exe" "$FINAL_DIST"/
  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
}

function build_macos() {
  echo "Building macOS..."

  TMP_DIST="$DIST_ROOT/macos_tmp"
  FINAL_DIST="$DIST_ROOT/macos"

  pyinstaller "$ROOT/$MAIN" \
    --onedir \
    --noconsole \
    --name "$APP_NAME" \
    --add-data "$ROOT/assets:assets" \
    --add-data "$ROOT/logs:logs" \
    --add-data "$ROOT/saves:saves" \
    --distpath "$TMP_DIST" \
    --workpath "$WORK_ROOT/macos" \
    --specpath "$SPEC_ROOT/macos"

  rm -rf "$FINAL_DIST"
  mkdir -p "$FINAL_DIST"
  mv "$TMP_DIST/$APP_NAME"/* "$FINAL_DIST"/
  rm -rf "$TMP_DIST"

  copy_assets "$FINAL_DIST"
}

case "$1" in
  linux)
    build_linux
    ;;
  windows)
    build_windows
    ;;
  macos)
    build_macos
    ;;
  all)
    build_linux
    build_windows
    build_macos
    ;;
  *)
    echo "Usage: ./build.sh [linux|windows|macos|all]"
    exit 1
    ;;
esac

rm -rf "$WORK_ROOT"
rm -rf "$SPEC_ROOT"
echo "Build completed."
