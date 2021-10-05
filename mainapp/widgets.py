from django.forms.widgets import Input


class ChangeImageSize(Input):
    input_type = 'number'
    template_name ='change_image_size_widget.html'

