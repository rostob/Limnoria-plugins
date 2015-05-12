"""
# Copyright (c) 2015, Tobias Rosenqvist
# Copyright (c) 2013, Sergio Conde
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""

import supybot.conf as conf
import supybot.registry as registry
try:
    from supybot.i18n import PluginInternationalization
    _ = PluginInternationalization('Youtube')
except:
    _ = lambda x: x


def configure(advanced):
    """Configures the plugin by asking questions."""
    from supybot.questions import yn
    conf.registerPlugin('Youtube', True)
    if not yn(_("""This plugin offers a snarfer that will try to fetch
                   info about Youtube videos that it sees in the channel.
                   Would you like this snarfer to be enabled?
                   IMPORTANT:
                   You also need to edit plugin.py and enter your Google
                   Developers YouTube Data API key which you can obtain by
                   following the instructions on the following url before
                   the plugin will work correctly:
                   https://developers.google.com/youtube/v3/getting-started
                """), default=True):
        Youtube.youtubeSnarfer.setValue(False)

    if not yn(_("""Do you want to show the number of views?"""),
              default=True):
        Youtube.showViews.setValue(False)

    if not yn(_("""Do you want to show the duration?"""),
              default=True):
        Youtube.showDuration.setValue(False)

    if not yn(_("""Do you want to show likes/dislikes?"""),
              default=True):
        Youtube.showLikes.setValue(False)

    if yn(_("""Do you want to show the channel name?"""),
              default=False):
        Youtube.showChannel.setValue(True)

    if yn(_("""Do you want to show the video publish date?"""),
              default=False):
        Youtube.showDate.setValue(True)

    if yn(_("""Do you want the bot to prefix its reply with the nickname
               that posted the video URL?
            """), default=False):
        Youtube.prefixNick.setValue(True)

Youtube = conf.registerPlugin('Youtube')

conf.registerChannelValue(Youtube, 'youtubeSnarfer',
    registry.Boolean(True, _("""Enable the Youtube snarfer.""")))

conf.registerChannelValue(Youtube, 'showViews',
    registry.Boolean(True, _("""Show the number of views.""")))

conf.registerChannelValue(Youtube, 'showDuration',
    registry.Boolean(True, _("""Show the duration.""")))

conf.registerChannelValue(Youtube, 'showLikes',
    registry.Boolean(True, _("""Show likes/dislikes.""")))

conf.registerChannelValue(Youtube, 'showChannel',
    registry.Boolean(False, _("""Show the video channel.""")))

conf.registerChannelValue(Youtube, 'showDate',
    registry.Boolean(False, _("""Show the video publish date.""")))

conf.registerChannelValue(Youtube, 'prefixNick',
    registry.Boolean(False, _("""Prefix the reply with nickname.""")))

conf.registerChannelValue(Youtube, 'separator',
    registry.String('-', _("""The character or string separating
                              the data.""")))


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
