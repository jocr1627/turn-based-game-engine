class Knockdown(Action):
  def execute(self, diff):
    self.parent.set('is_prone', True)
  
  def get_is_valid(self, diff):
    return not self.parent.get('is_prone')
