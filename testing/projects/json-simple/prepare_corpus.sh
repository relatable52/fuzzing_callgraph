CORPUS_DIR=$1
mkdir -p "$CORPUS_DIR"
cp -r $CORPUS/fuzzing-corpus/json/* $CORPUS_DIR
cp -r $CORPUS/go-fuzz-corpus/json/corpus/* $CORPUS_DIR
