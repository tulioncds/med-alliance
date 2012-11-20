# -*- coding: utf-8 -*-
from unidecode import unidecode

from django.db import models
from django.conf import settings
from django.utils.encoding import smart_str
from django.db.utils import ConnectionHandler, DEFAULT_DB_ALIAS
from django.template import Context
from django.template.loader import render_to_string
from django import forms
from django.utils.safestring import mark_safe

from geopy import geocoders

import logging
logger = logging.getLogger(__name__)

connections = ConnectionHandler(settings.DATABASES)
connection = connections[DEFAULT_DB_ALIAS]

GOOGLE_KEY = None
if hasattr(settings, 'GOOGLE_KEY'):
    GOOGLE_KEY = settings.GOOGLE_KEY

class GeoCode(object):
    u""" Representa a latitude e a longitude de um endereço """

    def __init__(self, latitude=None, longitude=None, name=None, address=None):
        self.latitude = latitude
        self.longitude = longitude
        self.name=name.replace(';', ' ')
        self.address=address.replace(';', ' ')

    def __unicode__(self):
        return ';'.join([self.latitude and unicode(self.latitude) or '',
                         self.longitude and unicode(self.longitude) or '',
                         self.name and unicode(self.name) or '',
                         self.address and unicode(self.address) or '',])


class GeoCodeField(models.Field):
    __metaclass__ = models.SubfieldBase
    description = u"Latitude e longitude de um endereço"

    def get_internal_type(self):
        return 'CharField'

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 255

        if 'geocoder' in kwargs:
            self.geocoder = kwargs.pop('geocoder')
        elif GOOGLE_KEY:
            self.geocoder = geocoders.Google(GOOGLE_KEY)

        super(GeoCodeField, self).__init__(*args, **kwargs)

    def value_to_string(self, obj):
        """
        Returns a string value of this field from the passed obj.
        This is used by the serialization framework.
        """
        geocode = self._get_val_from_obj(obj)
        serialized = self.get_db_prep_value(geocode)
        return serialized

    def to_python(self, value):
        if not value:
            return value
        if isinstance(value, GeoCode):
            return value

        latitude, longitude, name, address = value.split(';')
        return GeoCode(latitude, longitude, name, address)

    def get_prep_value(self, value):
        return self.to_python(value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if not isinstance(value, GeoCode):
            return None
        return unicode(value)

    def get_default(self):
        if self.has_default():
            if callable(self.default):
                return self.default()
            return self.default
        if not self.empty_strings_allowed or (self.null and not connection.features.interprets_empty_strings_as_nulls):
            return None
        return ""

    def pre_save(self, model_instance, add):
        if GOOGLE_KEY:
            if not hasattr(model_instance, 'get_geocode_info'):
                raise NotImplementedError("models com GeoCodeField devem implementar o metodo 'get_geocode_info'.")

            geocode_info = model_instance.get_geocode_info()

            name = None
            address = None
            if geocode_info:
                name, address = geocode_info
                address = unidecode(address)
            if address and name:
                try:
                    g = self.geocoder
                    for point in g.geocode(address, False):
                        p = point
                        break
                    address, (latitude, longitude,) = p
                    model_instance.geocode = GeoCode(
                                                     latitude,
                                                     longitude,
                                                     name,
                                                     address
                                                    )

                    if hasattr(model_instance, 'set_address'):
                        model_instance.set_address(address)
                except Exception, e:
                    logger.error(e)

            return model_instance.geocode

    def formfield(self, **kwargs):
        kwargs['widget'] = GeoCodeWidget
        return super(GeoCodeField, self).formfield(**kwargs)

class GeoCodeWidget(forms.TextInput):
    """ Widget para selecionar a posicao no mapa """

    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'css/jquery-ui-1.8.7.custom.css',
            )
        }
        js = (
            'http://www.google.com/jsapi',
            settings.STATIC_URL + 'jquery/js/jquery-ui-1.8.7.custom.min.js',
            'http://maps.google.com/maps/api/js?key=%s&v=3&sensor=false&language=pt-BR' % GOOGLE_KEY,
        )

    def __init__(self, language=None, attrs=None):
        self.language = language or settings.LANGUAGE_CODE[:2]
        super(GeoCodeWidget, self).__init__(attrs=attrs)

    def render(self, name, value, attrs=None):
        if not value:
            return ''
        super(GeoCodeWidget, self).render(name, value, attrs)
        from tangerina.reviva.sites import site
        context = Context()
        context.update({
                'geonames' : True,
                'latitude': value.latitude,
                'longitude': value.longitude,
                'name': value.name,
                'address': value.address,
                'width': '780',
                'height': '580',
                'zoom': '15',
                'get_markers' : '%s:get_markers' % site.app_name,
            })
