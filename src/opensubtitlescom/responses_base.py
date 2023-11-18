"""
Copyright (c) 2023 Omer Duskin.

This file is part of Opensubtitles API wrapper.

Opensubtitles API is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published by the Massachusetts
Institute of Technology.

For full details, please see the LICENSE file located in the root
directory of this project.

This module define base class of opensubtitles responses.
"""

import ast
import json
import functools
import logging
from typing import Any
from datetime import datetime, date

logger = logging.getLogger(__name__)


def rgetattr(obj, attr, *args):
    """Support getattr on nested subobjects / chained properties.

    For example, for d = DotDict(aa={"bb": cc"})
    rgetattr(d, "aa.bb") will return "cc"
    """

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def rsetattr(obj, attr, val):
    """Support setattr on nested subobjects / chained properties."""
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


class ResponseJSONEncoder(json.JSONEncoder):
    """JSON encoder class for handling custom serialization of Response objects.

    Handle the SearchResponse that consists of Subtitle list.
    """

    def default(self, o: object) -> Any:
        """Override the default method of the JSONEncoder class.

        Serializes objects with a 'to_dict' method using 'to_dict'.
        Falls back to the super class's default method for other objects.

        Parameters:
            o (object): The object to be serialized.

        Returns:
            Any: The serialized representation of the object.
        """
        if hasattr(o, "to_dict"):
            return o.to_dict()
        return super().default(o)


class BaseResponse:
    """
    Base class for API responses.

    Attributes:
        Meta (class): Meta class for BaseResponse.
    """

    def __init__(self, **kwargs):
        """Initialize the BaseResponse object with optional keyword arguments."""
        pass

    class Meta:
        """Meta class for BaseResponse."""

        abstract = True

    def __str__(self):
        """Return a string representation of the BaseResponse object."""
        return self.__repr__()

    def __repr__(self):
        """Return a string representation of the BaseResponse object."""
        main_field = getattr(self.Meta, "main_field", "")
        main_field_value = f" {getattr(self, main_field)}" if main_field else ""
        return f"<{self.__class__.__name__}{main_field_value}>"

    def fields(self):
        """Return a dictionary of attributes and their values."""
        attributes = vars(self)
        return attributes

    def attr(
        self,
        key,
        default=None,
        cast=None,
        jsonify=False,
        to_epoch=False,
        to_date_str=None,
        str_date_format=None,
        auto_format=False,
    ):
        """Get and potentially format an attribute of the BaseResponse object.

        Args:
            key (str): The name of the attribute to retrieve.
            default: The default value to return if the attribute is not found.
            cast (type): The type to which the attribute should be cast.
            jsonify (bool): Whether to parse the attribute as JSON.
            to_epoch (bool): Whether to convert the attribute to an epoch timestamp.
            to_date_str (str): The date string format to use.
            str_date_format (str): The date string format to use.
            auto_format (bool): Whether to automatically format the attribute.

        Returns:
            The formatted attribute value.

        Raises:
            Exception: If an error occurs while retrieving or formatting the attribute.
        """
        try:
            value = rgetattr(self, key, default)
            value = value if value is not None else default
            if not value:
                return value
            if auto_format:
                if isinstance(value, (datetime, date)):
                    to_date_str = True
                if isinstance(value, (list, dict)):
                    jsonify = True
                if isinstance(value, str) and value.isdigit():
                    cast = int
            if cast:
                value = cast(value)
            if jsonify:
                value = ast.literal_eval(value)
            if to_date_str:
                str_date_format = str_date_format or "%Y-%m-%dT%H:%M:%S"
                value = value.strftime(str_date_format)
            if to_epoch:
                value = value.timestamp()
            return value
        except Exception as ex:
            raise Exception(f"Unable to get field attribute: `{key}` of {self} ex: {ex}")

    def styling(self, value, camel_case=False, dotted_key_merge=False):
        """Style a value according to specified formatting options.

        Args:
            value (str): The value to be styled.
            camel_case (bool): Whether to use camelCase formatting.
            dotted_key_merge (bool): Whether to merge keys separated by dots.

        Returns:
            The styled value.

        Raises:
            Exception: If an error occurs while styling the value.
        """
        try:
            if dotted_key_merge:
                value = value.replace(".", "_")
            if camel_case:
                tmp = value.replace("_", " ").title().replace(" ", "")
                return tmp[0].lower() + tmp[1:]
            return value
        except Exception as ex:
            raise Exception(f"Unable to set styling for value: {value}: {ex}")

    def to_dict(self, ignore_none=False, dotted_key_to_dict=False) -> dict:
        """Convert the BaseResponse object to a dictionary.

        Args:
            ignore_none (bool): Whether to exclude attributes with None values.
            dotted_key_to_dict (bool): Whether to convert dotted keys to nested dictionaries.

        Returns:
            A dictionary representation of the BaseResponse object.

        Raises:
            Exception: If an error occurs while converting the object to a dictionary.
        """
        returned_fields = self.fields()
        key_styling = functools.partial(self.styling, camel_case=False, dotted_key_merge=False)
        try:
            fields_data = {}
            for field in returned_fields:
                try:
                    fields_data[key_styling(field)] = self.attr(key=field)
                except Exception as ex:
                    logger.warning(f"Failed to get value for {field}: {ex}")
            if ignore_none:
                fields_data = {k: v for k, v in fields_data.items() if v is not None}
            if dotted_key_to_dict:
                new_fields_data = {}
                for key, value in fields_data.items():
                    items = key.split(".")
                    if len(items) > 1:
                        new_fields_data.setdefault(items[0], {})[items[1]] = value
                    else:
                        new_fields_data[key] = value
                fields_data = new_fields_data
        except Exception as ex:
            raise Exception(f"Unable to get fields: {returned_fields}, ex: {ex}")
        return fields_data

    def to_json(self) -> str:
        """Convert the object to a JSON-formatted string.

        Returns:
           str: The JSON-formatted string representation of the object.
        """
        return json.dumps(self.to_dict(), cls=ResponseJSONEncoder)
