import logging
import functools
from datetime import datetime

logger = logging.getLogger(__name__)


def rgetattr(obj, attr, *args):
    """Support getattr on nested subobjects / chained properties

    For example, for d = DotDict(aa={"bb": cc"})
    rgetattr(d, "aa.bb") will return "cc"
    """

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj] + attr.split("."))


def rsetattr(obj, attr, val):
    """Support setattr on nested subobjects / chained properties?"""
    pre, _, post = attr.rpartition(".")
    return setattr(rgetattr(obj, pre) if pre else obj, post, val)


class BaseResponse:
    def __init__(self, **kwargs):
        pass

    class Meta:
        abstract = True

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        main_field = getattr(self.Meta, "main_field", "")
        main_field_value = f" {getattr(self, main_field)}" if main_field else ""
        return f"<{self.__class__.__name__}{main_field_value}>"

    def fields(self):
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

    def styling(self, value, camel_case=False, dotted_key_merge=False, key_lstrip=None):
        try:
            if key_lstrip:
                if value.startswith(key_lstrip):
                    value = value[len(key_lstrip) :]
            if dotted_key_merge:
                value = value.replace(".", "_")
            if camel_case:
                tmp = value.replace("_", " ").title().replace(" ", "")
                return tmp[0].lower() + tmp[1:]
            return value
        except Exception as ex:
            raise Exception(f"Unable to set styling for value: {value}: {ex}")

    def to_dict(self, ignore_none=False, dotted_key_to_dict=False):
        returned_fields = self.fields()
        key_styling = functools.partial(self.styling, key_lstrip=None, camel_case=False, dotted_key_merge=False)
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


class SearchResponse(BaseResponse):
    def __init__(self, total_pages, total_count, per_page, page, data, query_string = None):
        self.total_pages = total_pages
        self.total_count = total_count
        self.per_page = per_page
        self.page = page
        self.data = [Subtitle(item) for item in data]
        self.query_string = query_string

    class Meta:
        main_field = "query_string"


class DiscoverLatestResponse(BaseResponse):
    def __init__(self, total_pages, total_count, page, data):
        self.total_pages = total_pages
        self.total_count = total_count
        self.page = page
        self.data = [Subtitle(item) for item in data]
        self.created_at = datetime.now()
        self.created_at_str = self.created_at.strftime("%Y-%m-%d %H:%M%z")

    class Meta:
        main_field = "created_at_str"


class DiscoverMostDownloadedResponse(DiscoverLatestResponse):
    pass


class DownloadResponse(BaseResponse):
    def __init__(self, response_data):
        self.link = response_data.get('link')
        self.file_name = response_data.get('file_name')
        self.requests = response_data.get('requests')
        self.remaining = response_data.get('remaining')
        self.message = response_data.get('message')
        self.reset_time = response_data.get('reset_time')
        self.reset_time_utc = response_data.get('reset_time_utc')
        self.uk = response_data.get('uk')
        self.uid = response_data.get('uid')
        self.ts = response_data.get('ts')


class Subtitle(BaseResponse):
    def __init__(self, data_dict):
        self.id = data_dict.get('id')
        self.type = data_dict.get('type')
        self.subtitle_id = data_dict.get('attributes', {}).get('subtitle_id')
        self.language = data_dict.get('attributes', {}).get('language')
        self.download_count = data_dict.get('attributes', {}).get('download_count')
        self.new_download_count = data_dict.get('attributes', {}).get('new_download_count')
        self.hearing_impaired = data_dict.get('attributes', {}).get('hearing_impaired')
        self.hd = data_dict.get('attributes', {}).get('hd')
        self.fps = data_dict.get('attributes', {}).get('fps')
        self.votes = data_dict.get('attributes', {}).get('votes')
        self.ratings = data_dict.get('attributes', {}).get('ratings')
        self.from_trusted = data_dict.get('attributes', {}).get('from_trusted')
        self.foreign_parts_only = data_dict.get('attributes', {}).get('foreign_parts_only')
        self.upload_date = data_dict.get('attributes', {}).get('upload_date')
        self.ai_translated = data_dict.get('attributes', {}).get('ai_translated')
        self.machine_translated = data_dict.get('attributes', {}).get('machine_translated')
        self.release = data_dict.get('attributes', {}).get('release')
        self.comments = data_dict.get('attributes', {}).get('comments')
        self.legacy_subtitle_id = data_dict.get('attributes', {}).get('legacy_subtitle_id')
        self.uploader_id = data_dict.get('attributes', {}).get('uploader', {}).get('uploader_id')
        self.uploader_name = data_dict.get('attributes', {}).get('uploader', {}).get('name')
        self.uploader_rank = data_dict.get('attributes', {}).get('uploader', {}).get('rank')
        self.feature_id = data_dict.get('attributes', {}).get('feature_details', {}).get('feature_id')
        self.feature_type = data_dict.get('attributes', {}).get('feature_details', {}).get('feature_type')
        self.year = data_dict.get('attributes', {}).get('feature_details', {}).get('year')
        self.title = data_dict.get('attributes', {}).get('feature_details', {}).get('title')
        self.movie_name = data_dict.get('attributes', {}).get('feature_details', {}).get('movie_name')
        self.imdb_id = data_dict.get('attributes', {}).get('feature_details', {}).get('imdb_id')
        self.tmdb_id = data_dict.get('attributes', {}).get('feature_details', {}).get('tmdb_id')
        self.season_number = data_dict.get('attributes', {}).get('feature_details', {}).get('season_number')
        self.episode_number = data_dict.get('attributes', {}).get('feature_details', {}).get('episode_number')
        self.parent_imdb_id = data_dict.get('attributes', {}).get('feature_details', {}).get('parent_imdb_id')
        self.parent_title = data_dict.get('attributes', {}).get('feature_details', {}).get('parent_title')
        self.parent_tmdb_id = data_dict.get('attributes', {}).get('feature_details', {}).get('parent_tmdb_id')
        self.parent_feature_id = data_dict.get('attributes', {}).get('feature_details', {}).get('parent_feature_id')
        self.url = data_dict.get('attributes', {}).get('url')
        self.related_links = data_dict.get('attributes', {}).get('related_links', [])
        self.files = data_dict.get('attributes', {}).get('files', [])

        self.file_id = self.files[0].get("file_id") if self.files else None
        self.file_name = self.files[0].get("file_name") if self.files else None

    class Meta:
        main_field = "release"
