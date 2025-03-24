CORPUS_DIR=$1

mkdir -p "$CORPUS_DIR"

find $CORPUS/go-fuzz-corpus-master/bmp/corpus \
     $CORPUS/go-fuzz-corpus-master/gif/corpus \
     $CORPUS/go-fuzz-corpus-master/jpeg/corpus \
     $CORPUS/go-fuzz-corpus-master/png/corpus \
     $CORPUS/go-fuzz-corpus-master/tiff/corpus \
     $CORPUS/go-fuzz-corpus-master/webp/corpus \
     -type f ! -name "da39a3ee5e6b4b0d3255bfef95601890afd80709*" \
     -exec cp {} "$CORPUS_DIR" \;