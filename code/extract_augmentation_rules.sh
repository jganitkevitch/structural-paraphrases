
# hacky script that extracts (in this example) adjectives from the grammar and
# builds deletion rules (with a hard-coded penalty feature):

zcat paraphrase_grammar_samt_fixed_aggregated_fr-en.gz | fgrep "[JJ" | gzip > JJ.gz

zcat JJ.gz | grep "^\[J\(J\|JR\|JS\)\] |||" | cut -d "|" -f 1,4 | sort -u | \
  fgrep -v ",1]" > JJ_words.txt

cat JJ_words.txt | \
  awk 'BEGIN { FS="|" } { print $1 "|||" $2 "|||  ||| 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0" }' | \
  gzip > paraphrase_augmentation.gz

zcat paraphrase_grammar_samt_fixed_aggregated_fr-en.gz paraphrase_augmentation.gz | \
  gzip > paraphrase_grammar_samt_augmented_fr-en.gz 
