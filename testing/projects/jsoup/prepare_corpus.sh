CORPUS_DIR=$1

mkdir -p "$CORPUS_DIR/xml"
mkdir -p "$CORPUS_DIR/html"

cp -r $CORPUS/go-fuzz-corpus/xml/corpus/* $CORPUS_DIR/xml/
cp -r $CORPUS/go-fuzz-corpus/htmltemplate/corpus/* $CORPUS_DIR/html/

cp -r $CORPUS/fuzzing-corpus/xml/* $CORPUS_DIR/xml/
cp -r $CORPUS/fuzzing-corpus/html/* $CORPUS_DIR/html/