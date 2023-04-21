import bleach  # https://bleach.readthedocs.io/en/latest/index.html


class SafeHtml:
    def __init__(self):
        self.allowed_attrs = {'a': ['href', 'title'],
                              'abbr': ['title'],
                              'acronym': ['title'],
                              'table': ['border', ]}
        self.allowed_tags = frozenset([
            'a', 'abbr', 'acronym', 'caption', 'b', 'blockquote', 'code',
            'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'ol', 'p', 'strong', 'table', 'tbody', 'td', 'tr', 'ul'
        ])
        self.allowed_protocols = frozenset(['http', 'https', 'mailto'])
        self.strip_disallowed = True  # Default: False. When True --> strip disallowed tags instead of escaping them.
        self.strip_html_comments = True  # Default: True
        # self.linkify_filter = bleach.linkifier.LinkifyFilter(source=t)

    def clean(self, text):
        safe_text = bleach.clean(text=text,
                                 tags=self.allowed_tags,
                                 attributes=self.allowed_attrs,
                                 protocols=self.allowed_protocols,
                                 strip=self.strip_disallowed,
                                 strip_comments=self.strip_html_comments)
        return safe_text  # Returned in unicode.


# # Testing:

# safe = SafeHtml()
# abc = safe.clean(text="<script><b><i>an example</i></b></script>")
# print(abc)  # --> &lt;script&gt;<b><i>an example</i></b>&lt;/script&gt;

# ------------ #

# sanitizer = SafeHtml()
# # # Set <i> to not allowed.
# my_text = '<b><i>an example</i></b>'
# new_text = sanitizer.clean(my_text)

# When self.strip_disallowed == False:
# new_text --> '<b>&lt;i&gt;an example&lt;/i&gt;</b>'

# When strip_disallowed == True:
# new_text --> '<b>an example</b>'
