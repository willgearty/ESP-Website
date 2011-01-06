
__author__    = "Individual contributors (see AUTHORS file)"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "AGPL v.3"
__copyright__ = """
This file is part of the ESP Web Site
Copyright (c) 2007 by the individual contributors
  (see AUTHORS file)

The ESP Web Site is free software; you can redistribute it and/or
modify it under the terms of the GNU Affero General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.

Contact information:
MIT Educational Studies Program
  84 Massachusetts Ave W20-467, Cambridge, MA 02139
  Phone: 617-253-4882
  Email: esp-webmasters@mit.edu
Learning Unlimited, Inc.
  527 Franklin St, Cambridge, MA 02139
  Phone: 617-379-0178
  Email: web-team@lists.learningu.org
"""

from esp.users.models    import GetNodeOrNoBits, PermissionDenied
from esp.datatree.models import *
from esp.datatree.url_map import get_branch_info
from django.http import Http404
from esp.web.util.main import render_to_response
from django.core.cache import cache

def branch_find(view_func):
    """
    A decorator to be used on a view.
    The signature of the view its used on is:

    view(request, node, name, section, action, *args **kwargs)

    Where:
       request: A standard HttpRequest object.
       node:    A DataTree node corresponding to this url.
       name:    The name of the node, e.g. 'learn:index'.
       section: A section, e.g. 'learn', or 'teach'.
       action:  An action that is being performed on this url,
                the standard ones are ['create','edit','read']
    """

    def _new_func(request, url='index', subsection=None, filename=None, *args, **kwargs):

        # Cache which tree node corresponds to this URL
        cache_key = 'qsdeditor_%s_%s_%s_%s' % (request.user.id,
                                               url, subsection, filename)
        cache_key = cache_key.replace(' ', '')
        retVal = cache.get(cache_key)
        if retVal is None:
            # function "constants"
            READ_VERB = GetNode('V/Flags/Public')

            # Process the URL
            if filename:
                url += '/%s' % filename
            tree_node_uri, view_address, subsection, action = get_branch_info(url, subsection)

            # Fetch the datatree node
            try:
                # attempt to get the node
                branch = GetNodeOrNoBits(tree_node_uri,
                                         request.user,
                                         READ_VERB,
                                        #only create if we are planning on writing.
                                         action in ('create','edit',)
                                         )
            except PermissionDenied:
                raise Http404, "No such site, no bits to create it: '%s'" % \
                             tree_node_uri
            except DataTree.NoSuchNodeException, e:
                edit_link = request.path[:-5]+'.edit.html'
                branch = e.anchor
                return render_to_response('qsd/nopage_create.html',
                                          request,
                                          (branch, section),
                                          {'edit_link': edit_link})

            # Save our cached answer
            retVal = (branch, view_address, subsection, action)

            if request.user.id is None:
                cache.set(cache_key, retVal, 86400)
            else:
                cache.set(cache_key, retVal, 3600)

        return view_func(*((request,) + retVal + args), **kwargs)

    _new_func.__doc__ = view_func.__doc__
    return _new_func


