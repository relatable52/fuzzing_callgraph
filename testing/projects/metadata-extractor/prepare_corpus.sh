CORPUS_DIR=$1

cp $CORPUS/go-fuzz-corpus-master/bmp/corpus/* \
    $CORPUS/go-fuzz-corpus-master/gif/corpus/* \
    $CORPUS/go-fuzz-corpus-master/jpeg/corpus/* \
    $CORPUS/go-fuzz-corpus-master/png/corpus/* \
    $CORPUS/go-fuzz-corpus-master/tiff/corpus/* \
    $CORPUS/go-fuzz-corpus-master/webp/corpus/* \
    $CORPUS_DIR