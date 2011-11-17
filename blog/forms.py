from django import forms
from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.conf import settings

class TinyMCEForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TinyMCEForm, self).__init__(*args, **kwargs)
        self.fields['body'].widget = TinyMCE(
            attrs={
                'cols': 100, 
                'rows': 30,},
            mce_attrs={
                'theme' : "advanced",
                'skin' : "o2k7",
                'skin_variant' : "silver",
                'plugins': "fullscreen, media, paste",
                'theme_advanced_toolbar_location' : "top",
                'theme_advanced_toolbar_align' : "left",
                'theme_advanced_blockformats' : "p,h1,h2,h3,h4,h5,h6,dt,dd,"
                                                + "code,samp",
                'theme_advanced_buttons1' : "image, media, code",
                'theme_advanced_buttons2' : "bold, italic, strikethrough,"
                                            + "seperator, justifyleft, "
                                            + "justifycenter, justifyright,"
                                            + "seperator, numlist, bullist,"
                                            + "blockquote, seperator, link,"
                                            + "unlink, seperator, fullscreen",
                'theme_advanced_buttons3' : "formatselect, underline,"
                                            + "justifyfull, forecolorpicker,"
                                            + "seperator, pastetext,"
                                            + "pasteword, removeformat,"
                                            + "seperator, charmap, seperator,"
                                            + "outdent, indent, seperator,"
                                            + "undo, redo, help", 
                'content_css' : settings.STATIC_URL 
                                + "blog/css/custom_content.css",
                'file_browser_callback' : 'fileBrowser'
                })
