# Here I will display the copyright message and some other information (see it in other programs)

from imagepy.core.engine import Free
from imagepy import IPy


about_message = 'Author: Zoltan Csati\nLicense: MIT\nSpecial thanks to Yan Xiaolong.\n' \
                'Libraries used:\n\tx\n\ty'


class About(Free):
    title = 'About'

    def run(self, para=None):
        IPy.alert(about_message, title='About')


plgs = [About]
