from zipfile import ZipFile
from lxml import etree

f = r"C:\Users\Pedro\Documents\SemanticArts\GIST.owl\gist11.1.0_gist_constellations_KindleBook\2022-10-09_gist_11.1.0_constellations.epub"
fout = r"C:\Users\Pedro\Documents\SemanticArts\GIST.owl\gist11.1.0_gist_constellations_KindleBook\2022-10-09_gist_11.1.0_constellations.out.epub"

infile = ZipFile(f)
outfile = ZipFile(fout, "w")

# load up the locations
nav = infile.read("nav.xhtml")
xmldoc = etree.fromstring(nav)
dict = {}
for link in xmldoc.xpath('//x:a/@href', namespaces={"x":"http://www.w3.org/1999/xhtml"}):
    split_link = link.split("#")
    dict[split_link[1]] = split_link[0]
print(dict["gistemailaddress"])

for f in infile.infolist():

    if "ch0" in f.filename:
        newfile = infile.read(f.filename)
        for x in dict.keys():
            newfile = str(newfile).replace("a href=\"#" + x + "-identifier", "a href=\"" + str(dict[x]) + "#" + str(x) )
            print("replace:  ", "a href=\"#" + x + "-identifier", "a href=\"" + str(dict[x]) + "#" + str(x)  )
        #print(newfile)
        outfile.writestr(f.filename, newfile)
    else:
        newfile = infile.read(f.filename)
        outfile.writestr(f.filename, newfile)
