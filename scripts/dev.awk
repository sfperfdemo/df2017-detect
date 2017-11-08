BEGIN {FS="\t"}
{
  print substr($1,3,14) "	" $13
}
