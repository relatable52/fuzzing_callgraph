CORPUS_DIR=$1

cp -r $CORPUS/fuzzing-corpus/xml/* $CORPUS_DIR
cp -r $CORPUS/go-fuzz-corpus/xml/corpus/* $CORPUS_DIR
