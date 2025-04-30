CORPUS_DIR=$1

cp -r $CORPUS/fuzzing-corpus/zip/* $CORPUS_DIR
cp -r $CORPUS/go-fuzz-corpus/zip/corpus/* $CORPUS_DIR
