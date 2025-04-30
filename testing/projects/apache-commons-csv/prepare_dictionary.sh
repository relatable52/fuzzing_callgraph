DICT_DIR=$1

mkdir -p "$DICT_DIR"

cp -r $CORPUS/fuzzing/dictionaries/csv.dict $DICT_DIR/dict.txt
