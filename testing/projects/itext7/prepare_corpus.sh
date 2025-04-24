CORPUS_DIR=$1
mkdir -p "$CORPUS_DIR"
cp -r $CORPUS/fuzzing-corpus/pdf/* $CORPUS_DIR