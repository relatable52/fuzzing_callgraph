CORPUS_DIR=$1

mkdir -p "$CORPUS_DIR"

find $CORPUS/go-fuzz-corpus/bmp/corpus \
    $CORPUS/go-fuzz-corpus/gif/corpus \
    $CORPUS/go-fuzz-corpus/jpeg/corpus \
    $CORPUS/go-fuzz-corpus/png/corpus \
    $CORPUS/go-fuzz-corpus/tiff/corpus \
    $CORPUS/go-fuzz-corpus/webp/corpus \
    -type f ! -name "da39a3ee5e6b4b0d3255bfef95601890afd80709*" \
    -exec cp {} "$CORPUS_DIR" \;

find $CORPUS/fuzzing-corpus/bmp \
    $CORPUS/fuzzing-corpus/gif \
    $CORPUS/fuzzing-corpus/jpg \
    $CORPUS/fuzzing-corpus/png \
    $CORPUS/fuzzing-corpus/tiff \
    $CORPUS/fuzzing-corpus/webp \
    -type d -name "go-fuzz" -prune -o -type f -exec cp {} "$CORPUS_DIR" \;