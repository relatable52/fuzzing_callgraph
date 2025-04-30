DICT_DIR=$1

mkdir -p "$DICT_DIR"

touch $DICT_DIR/dict.txt

cat $CORPUS/fuzzing-corpus/dictionaries/xml.dict \
    $CORPUS/fuzzing-corpus/dictionaries/html_tags.dict \
    > $DICT_DIR/dict.txt
