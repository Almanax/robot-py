from element import Element, Elements, Node, Edge, \
  RDF_TYPE, NTWK_SERVICE, NTWK_HOSTS, NTWK_IP, RDFS_LABEL, RDF_PROPERTY

def test_node():
  url = 'http://example.com#1'
  types = [NTWK_SERVICE]
  node = Node(url, {RDF_TYPE:types})
  assert node.id == url, 'Should be {}'.format(url)
  assert node.data == {RDF_TYPE: types}, 'Should be {}'.format({RDF_TYPE: types})
  assert not node.source
  assert not node.target

def test_edge():
  subj = 'http://example.com#1'
  pred = NTWK_HOSTS
  obj = 'http://example.com#2'
  edge = Edge(subj, pred, obj)
  url = subj+pred+obj
  assert edge.id == url, 'Should be {}'.format(url)
  assert edge.source == subj, 'Should be {}'.format(subj)
  assert edge.target == obj, 'Should be {}'.format(obj)

def test_element_is_node():
  node = Node('http://example.com#1', {RDF_TYPE:[NTWK_SERVICE]})
  assert node.is_node, 'Should be True'
  edge = Edge('http://example.com#1', NTWK_HOSTS, 'http://example.com#2')
  assert not edge.is_node, 'Should be False'

def test_element_is_edge():
  node = Node('http://example.com#1', {RDF_TYPE:[NTWK_SERVICE]})
  assert not node.is_edge, 'Should be False'
  edge = Edge('http://example.com#1', NTWK_HOSTS, 'http://example.com#2')
  assert edge.is_edge, 'Should be True'

def test_element_has_type():
  node = Node('http://example.com#1', {RDF_TYPE:[NTWK_SERVICE]})
  assert node.has_type(NTWK_SERVICE), 'Should be True'
  assert not node.has_type(NTWK_IP), 'Should be False'

def test_element_types():
  types = [NTWK_SERVICE]
  node = Node('http://example.com#1', {RDF_TYPE:types})
  assert node.types == types, 'Should be {}'.format(types)

def test_element_labels():
  node = Node('http://example.com#1', {RDF_TYPE:[NTWK_SERVICE]})
  assert len(node.labels) == 0, 'Should be 0'
  labels = ['hello world']
  node = Node('http://example.com#1', {RDF_TYPE:[NTWK_SERVICE],RDFS_LABEL:labels})
  assert node.labels == labels, 'Should be {}'.format(labels)

def test_elements_empty():
  eles = Elements()
  assert len(eles) == 0, 'Should be 0'

n1 = {
  'id': 'http://example.com#1',
  'data': {RDF_TYPE: [NTWK_SERVICE]}}

e1 = {
  'id': 'http://example.com#1'+RDF_PROPERTY+'http://example.com#2',
  'source': 'http://example.com#1',
  'target': 'http://example.com#2',
  'data': {RDF_PROPERTY: [NTWK_HOSTS]}}

l1 = [n1]
l2 = [e1]
l3 = [n1,e1]

def test_elements_from_list():
  eles = Elements(l1)
  assert len(eles) == 1, 'Should be 1'
  assert eles[0].is_node, 'Should be True'
  eles = Elements(l2)
  assert len(eles) == 1, 'Should be 1'
  assert eles[0].is_edge, 'Should be True'
  eles = Elements(l3)
  assert len(eles) == 2, 'Should be 2'
