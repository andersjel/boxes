class Namespace:

  def __init__(self, content):
    self.__dict__.update(content)
    self._content = content

  def __repr__(self):
    return 'Namespace({!r})'.format(self._content)
