pandoc\
  ./output/2023-04-05_gist_11.1.0.md\
  -o ./output/2023-04-05_gist_11.1.0.md.v2.epub\
  --toc\
  ./figures.etc/metadata.yaml\
  -M title='The Zest of gist'\
  --lua-filter=codeblock-filter.lua