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

import sys
import requests
from isodate import parse_duration
if sys.version_info[0] < 3:
    from urlparse import urlparse, parse_qs
else:
    from urllib.parse import urlparse, parse_qs

import supybot.log as log
import supybot.utils as utils
import supybot.callbacks as callbacks
from supybot.commands import urlSnarfer


def youtubeId(value):
    """Parses a string containing a YouTube URL

    Returns:
    a string containing a YouTube video ID
    """
    query = urlparse(value)
    yid = None
    if query.hostname == 'youtu.be':
        yid = query.path[1:]
    elif query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            yid = parse_qs(query.query)['v'][0]
        elif query.path[:7] == '/embed/' or query.path[:3] == '/v/':
            yid = query.path.split('/')[2]
        elif query.hostname == 'm.youtube.com' and query.path == '/watch':
            yid = parse_qs(query.query)['v'][0]
        elif (query.hostname == 'youtube.googleapis.com' and
              query.path[:3] == '/v/'):
            yid = query.path.split('/')[2]
    return yid

try:
    from supybot.i18n import PluginInternationalization
    from supybot.i18n import internationalizeDocstring
    _ = PluginInternationalization('Youtube')
except:
    _ = lambda x: x
    internationalizeDocstring = lambda x: x


@internationalizeDocstring
class Youtube(callbacks.PluginRegexp):
    """Listens for Youtube URLs and retrieves video info."""
    threaded = True
    regexps = ['youtubeSnarfer']

    """Google Developers YouTube Data API-key
    Obtain a key by following the instructions on:
    https://developers.google.com/youtube/v3/getting-started
    """
    apiKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

    _apiUrl = ''.join([
            'https://www.googleapis.com/youtube/v3/videos?part=',
            'snippet', '%2C',
            'contentDetails', '%2C',
            'statistics',
            '&id={}&key=', apiKey])

    if apiKey == 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx':
        log.error('No API key configured in Youtube plugin.py')

    def youtubeSnarfer(self, irc, msg, match):
        """Fetches data from the YouTube Data API."""
        channel = msg.args[0]
        if not irc.isChannel(channel):
            return
        if self.registryValue('youtubeSnarfer', channel):
            ytid = youtubeId(match.group(0))
            if ytid:
                try:
                    api_request = requests.get(self._apiUrl.format(ytid))
                except requests.exceptions.ConnectionError as exc:
                    log.error(''.join([
                                "Couldn't connect to Youtube's API: ",
                                exc]))
                    api_request = None

                if api_request and '<Response [200]>' in str(api_request):
                    api_result = api_request.json()
                    separator = self.registryValue('separator', channel)

                    if 'snippet' in api_result["items"][0]:
                        video_info = api_result["items"][0]

                        line = format("\x02YouTube\x02: %s",
                                      video_info['snippet']['title'])

                        if 'contentRating' in video_info['contentDetails']:
                            line += " \x02[NSFW]\x02"

                        if self.registryValue('showDuration', channel):
                            line += format(" %s %s",
                                           separator,
                                           str(
                                    parse_duration(video_info[
                                            'contentDetails']['duration'])))

                        if self.registryValue('showViews', channel):
                            line += format(" %s %s views",
                                           separator,
                                           video_info[
                                    'statistics']['viewCount'])

                        if self.registryValue('showLikes', channel):
                            line += format(" %s %s likes / %s dislikes",
                                           separator,
                                           video_info[
                                    'statistics']['likeCount'],
                                           video_info[
                                    'statistics']['dislikeCount'])

                        if self.registryValue('showChannel', channel):
                            line += format(" %s channel: %s",
                                           separator,
                                           video_info[
                                    'snippet']['channelTitle'])

                        if self.registryValue('showDate', channel):
                            line += format(" %s published: %s",
                                           separator,
                                           video_info[
                                    'snippet']['publishedAt'])

                        if not self.registryValue('prefixNick', channel):
                            irc.reply(line, prefixNick=False)
                        else:
                            irc.reply(line)
                else:
                    log.error(''.join(["Got ", str(api_request),
                                       " from the YouTube Data API"]))

    youtubeSnarfer = urlSnarfer(youtubeSnarfer)
    youtubeSnarfer.__doc__ = utils.web._httpUrlRe

Class = Youtube


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
