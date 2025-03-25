DICT_DIR=$1

mkdir -p "$DICT_DIR"

cat $CORPUS/fuzzing-corpus/dictionaries/gif.dict \
    $CORPUS/fuzzing-corpus/dictionaries/jpeg.dict \
    $CORPUS/fuzzing-corpus/dictionaries/png.dict \
    $CORPUS/fuzzing-corpus/dictionaries/tiff.dict \
    $CORPUS/fuzzing-corpus/dictionaries/webp.dict \
    > $DICT_DIR/dict.txt
