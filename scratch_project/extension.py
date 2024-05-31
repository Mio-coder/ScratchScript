class Extension:
  def __init__(self, extension_id):
      self.extension_id = extension_id

  def to_dict(self):
      return self.extension_id
