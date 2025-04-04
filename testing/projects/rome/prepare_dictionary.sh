DICT_DIR=$1

mkdir -p "$DICT_DIR"

cp -r $CORPUS/fuzzing-corpus/dictionaries/xml.dict $DICT_DIR/dict.txt