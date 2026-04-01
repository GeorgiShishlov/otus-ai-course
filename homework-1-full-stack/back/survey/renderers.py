import json
from datetime import datetime
from rest_framework.renderers import JSONRenderer


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class UTF8JSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        return json.dumps(data, cls=DateTimeEncoder, ensure_ascii=False, indent=2).encode('utf-8')
