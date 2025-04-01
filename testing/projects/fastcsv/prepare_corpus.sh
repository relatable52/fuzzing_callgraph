CORPUS_DIR=$1
mkdir -p "$CORPUS_DIR"
cp -r $CORPUS/go-fuzz-corpus/csv/corpus/* $CORPUS_DIR