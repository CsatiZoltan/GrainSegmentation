# Here I will display the copyright message and some other information (see it in other programs)

from imagepy.core.engine import Free
from imagepy import IPy


about_message = 'This program is free software under the GNU General Public License v3.0\n\n' \
                'Developer: Zoltan Csati (special thanks to Yan Xiaolong)\n\n' \
                'Software used: ImagePy\n\n' \
                'Home page: https://github.com/CsatiZoltan/GrainSegmentation'


class About(Free):
    title = 'About'

    def run(self, para=None):
        IPy.alert(about_message, title='About')


plgs = [About]
