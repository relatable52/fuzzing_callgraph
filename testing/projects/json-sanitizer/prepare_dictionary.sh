DICT_DIR=$1
mkdir -p "$DICT_DIR"
cat $CORPUS/fuzzing/dictionaries/json.dict \
    $CORPUS/fuzzing/dictionaries/html.dict \
    $CORPUS/fuzzing/dictionaries/xml.dict \
    > $DICT_DIR/dict.txt
