from rdflib import *

def rdf2dot_pwin(g, stream, opts={}):
    """
    Convert the RDF graph to DOT
    writes the dot output to the stream
    """

    nodes = {}
    g.bind_namespaces = "rdflib"

    def node(x,g, color):
        if x not in nodes:
            nodes[x] = '''"{}" [color="{}"]'''.format(qname(x,g), color)
        #print(nodes[x])
        return nodes[x]


    def qname(x, g):
        try:
            q = g.compute_qname(x)
            return q[0] + ":" + q[2]
        except:
            return x

    def color(o):
        if isinstance(o, (URIRef)):
            return "BLACK"
        elif isinstance(o, (BNode)):
            return "ORANGE"
        elif isinstance(o, (Literal)):
            return "BLUE"
        else:
            return "BLACK"

    def isListNode(pred):
        #listPredicates = ["http://www.w3.org/1999/02/22-rdf-syntax-ns#first", "http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"]
        listPredicates = ["http://www.w3.org/1999/02/22-rdf-syntax-ns#rest"]
        return str(pred) in listPredicates



    stream.write('''digraph {
    node [shape="box", style="rounded"];
    rankdir="LR"; ratio="auto";
    subgraph RDF {''')
    listMembers = []
    firstMember = []
    statements = []
    #for s, p, o in g:
    for s,p,o in g:
        if isListNode(p):
            listMembers.append((s, p, o))

        #print(listMembers)

        first = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#first")
        rest = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#rest")
        nil = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#nil")
        if p == first:
            #listMembers.append((s,p,o))
            for s1,p1,o1 in g:
                if s1 == s and p1 == rest and not o1 == nil:
                    statements.append((s1,p1,o1))
        if isinstance(s, (URIRef,BNode)):
            sn = node(s,g, color(s))
        if isinstance(o, (URIRef, BNode, Literal)):
            on = node(o,g, color(o))
        #print(s, qname(s,g))
        opstr = ("""\t"%s" -> "%s" [ label="%s"] ;\n""")
        stream.write(opstr % (qname(s,g), qname(o,g), qname(p, g)))
    print("listMembers", listMembers)
    print("statements", statements)
    for y in nodes.keys():
        stream.write(nodes[y] +'\n')
    stream.write("}\n}")


def isObjectOfFirstRest(g, node):
    try:
        q = """prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                ask { ?x (rdf:rest|rdf:first) _:""" + str(node) + "l" + """  filter(isblank(?x)) }"""
        print(q)
        res = bool(g.query(q))
        return res
    except Exception as e:
        return 'Err'


if __name__ == "__main__":
    import io

    def visualize(g):
        stream = io.StringIO()
        rdf2dot_pwin(g, stream, opts={})
        f=open('./output/myGraph.dot','w')
        f.write(stream.getvalue())


    gist_ontology_file = './ontology/v11.1.gistCore.owl'

    g = Graph()
    g_draw = Graph()
    g.parse(gist_ontology_file)
    gist = Namespace('https://ontologies.semanticarts.com/gist/')

    g.namespace_manager.bind('gist', gist)
    ds = Dataset()

    g_res = g.query('describe  <https://ontologies.semanticarts.com/gist/PlannedEvent> ')
    for x in g_res:
        g_draw.add(x)

    # for z in ds.graphs():
    #     print(z)
    #     for a in z:
    #         print(a)
    myList = list(g_draw.query(
        """
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        select ?x ?y where
        {
        ?x rdf:rest*/rdf:first ?y.
        }
        """))

    [print(isObjectOfFirstRest(g_draw, x), isObjectOfFirstRest(g_draw, y)) for x, y in myList]


    visualize(g_draw)