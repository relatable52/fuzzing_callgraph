DICT_DIR=$1
mkdir -p "$DICT_DIR"
cat $CORPUS/fuzzing-corpus/dictionaries/json.dict \
    $CORPUS/fuzzing-corpus/dictionaries/html.dict \
    $CORPUS/fuzzing-corpus/dictionaries/xml.dict \
    > $DICT_DIR/dict.txt
