__author__    = "MIT ESP"
__date__      = "$DATE$"
__rev__       = "$REV$"
__license__   = "GPL v.2"
__copyright__ = """
This file is part of the ESP Web Site
Copyright (c) 2009 MIT ESP

The ESP Web Site is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

Contact Us:
ESP Web Group
MIT Educational Studies Program,
84 Massachusetts Ave W20-467, Cambridge, MA 02139
Phone: 617-253-4882
Email: web@esp.mit.edu
"""

""" Forms for Resources application """

from django import forms
from django.forms.formsets import formset_factory
from esp.resources.models import ResourceType, ResourceRequest


class IDBasedModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%d" % obj.id

class ResourceRequestForm(forms.Form):
    resource_type = IDBasedModelChoiceField(queryset=ResourceType.objects.all(), widget=forms.HiddenInput)
    desired_value = forms.ChoiceField(choices=(), widget=forms.RadioSelect, required=False)
    #   desired_value = forms.ChoiceField(choices=())
    
    def __init__(self, data=None, **kwargs):
    
        if 'resource_type' in kwargs:
            self.resource_type = kwargs['resource_type']
            del kwargs['resource_type']

        super(ResourceRequestForm, self).__init__(data, **kwargs)
    
        if data and ('prefix' in kwargs):
            self.prefix = kwargs['prefix']
            key_name = self.add_prefix('resource_type')
            if key_name in data:
                self.resource_type = ResourceType.objects.get(id=data[key_name])

        if hasattr(self, 'resource_type'):
            self.fields['desired_value'].label = self.resource_type.name
            #   Use radio buttons for 4 or fewer choices; select boxes above that to save space
            if len(self.resource_type.choices) > 4:
                self.fields['desired_value'].widget = forms.Select()
            #   Don't provide a blank default value
            #   self.fields['desired_value'].choices = zip(tuple(' ') + self.resource_type.choices, tuple(' ') + self.resource_type.choices)    
            self.fields['desired_value'].choices = zip(self.resource_type.choices, self.resource_type.choices)
            
            self.initial['resource_type'] = self.resource_type.id
        
class ResourceRequestFormSet(formset_factory(ResourceRequestForm, extra=0)):
    """ Like a FormSet, but handles the list of resource_types for the forms to start out with. """
    def __init__(self, *args, **kwargs):
        if 'resource_type' in kwargs:
            self.resource_type = kwargs['resource_type']
            del kwargs['resource_type']
        super(ResourceRequestFormSet, self).__init__(*args, **kwargs)
    
    def initial_form_count(self):
        """Returns the number of forms that are required in this FormSet."""
        if hasattr(self, 'resource_type'):
            return len(self.resource_type)
        else:
            return super(ResourceRequestFormSet, self).initial_form_count()
    
    def _construct_form(self, i, **kwargs):
        #   Adapted from Django 1.1 release.
        """
        Instantiates and returns the i-th form instance in a formset.
        """
        defaults = {'auto_id': self.auto_id, 'prefix': self.add_prefix(i)}
        if self.data or self.files:
            defaults['data'] = self.data
            defaults['files'] = self.files
        if self.initial:
            try:
                defaults['initial'] = self.initial[i]
            except IndexError:
                pass
        # Allow extra forms to be empty.
        if i >= self.initial_form_count():
            defaults['empty_permitted'] = True
            
        #   Update by Michael Price for resource requests (app specific)
        default_args = kwargs.copy()
        if hasattr(self, 'resource_type'):
            #   Select out appropriate list item for the form being constructed.
            if type(self.resource_type) == list:
                default_args['resource_type'] = self.resource_type[i]
            
        defaults.update(default_args)
        form = self.form(**defaults)
        self.add_fields(form, i)
        
        return form
    
class ResourceTypeForm(forms.ModelForm):
    name = forms.CharField(label='New Request', required=False)

    class Meta:
        model = ResourceType
        fields = ['name']
    
class ResourceTypeFormSet(formset_factory(ResourceTypeForm, extra=0)):
    pass
