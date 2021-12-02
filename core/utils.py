class AdminUtility():
    def __init__(self,*args, **kwargs):
        self.request=None
        self.user=None
        if 'request' in kwargs:
            self.request=kwargs['request']
        if 'user' in kwargs:
            self.user=kwargs['user']

    def add_page_btn(self,*args, **kwargs):
        return f"""
        """