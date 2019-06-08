from collections import MutableSequence

RDF = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_TYPE = RDF + "type"
RDF_PROPERTY = RDF + "Property"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
RDFS_LABEL = RDFS + "label"

class Element:
  def __init__(self, id, source, target, data):
    self.id = id
    self.source = source
    self.target = target
    self.data = data

  @property
  def is_node(self):
    return not self.source and not self.target

  @property
  def is_edge(self):
    return self.source and self.target

  @property
  def types(self):
    return self.data.get(RDF_TYPE, [])

  @property
  def labels(self):
    return self.data.get(RDFS_LABEL, [])

  def has_type(self, typ):
    return self.is_node and typ in self.types

class Node(Element):
  def __init__(self, id, props):
    super().__init__(id, None, None, props)

class Edge(Element):
  def __init__(self, subj, pred, obj):
    id = subj + pred + obj
    data = {RDF_PROPERTY: [pred]}
    super().__init__(id, subj, obj, data=data)

class Elements(MutableSequence):
  def __init__(self, eles=None):
    eles = eles or []
    self._eles = []
    for e in eles:
      if 'source' not in e and 'target' not in e:
        self.add_node(e['id'], e['data'])
      elif 'source' in e and 'target' in e:
        self.add_edge(e['source'], e['data'][RDF_PROPERTY][0], e['target'])

  def __len__(self):
    return len(self._eles)

  def __delitem__(self, index):
    self._eles.__delitem__(index)

  def insert(self, index, value):
    self._eles.insert(index, value)

  def __setitem__(self, index, value):
    self._eles.__setitem__(index, value)

  def __getitem__(self, index):
    return self._eles.__getitem__(index)

  def add_node(self, id, data):
    node = Node(id, data)
    self._eles.append(node)

  def add_edge(self, subj, pred, obj):
    edge = Edge(subj, pred, obj)
    self._eles.append(edge)
