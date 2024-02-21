from __future__ import annotations

import json
from io import BytesIO
from typing import Final
from urllib.parse import urljoin

from requests import Response

from ..base.entry import SignInEntry
from ..base.request import check_network_state, NetworkState
from ..base.reseed import ReseedPage
from ..base.sign_in import check_final_state, SignState, check_sign_in_state
from ..base.work import Work
from ..schema.nexusphp import NexusPHP
from ..utils import net_utils, baidu_ocr
from ..utils.net_utils import get_module_name

try:
    from PIL import Image
except ImportError:
    Image = None


class MainClass(NexusPHP, ReseedPage):
    URL: Final = 'https://hdsky.me/'
    IMAGE_HASH_URL: Final = '/image_code_ajax.php'
    IMAGE_URL: Final = '/image.php?action=regimage&imagehash={}'
    TORRENT_PAGE_URL: Final = '/details.php?id={torrent_id}&hit=1'
    DOWNLOAD_URL_REGEX: Final = '/download\\.php\\?id=\\d+&passkey=.*?(?=")'
    USER_CLASSES: Final = {
        'downloaded': [8796093022208, 10995116277760],
        'share_ratio': [5, 5.5],
        'days': [315, 455]
    }

    @classmethod
    def sign_in_build_schema(cls) -> dict:
        return {
            get_module_name(cls): {
                'type': 'object',
                'properties': {
                    'cookie': {'type': 'string'},
                    'join_date': {'type': 'string', 'format': 'date'}
                },
                'additionalProperties': False
            }
        }

    @classmethod
    def reseed_build_schema(cls) -> dict:
        return {
            get_module_name(cls): {
                'type': 'object',
                'properties': {
                    'cookie': {'type': 'string'}
                },
                'additionalProperties': False
            }
        }

    def sign_in_build_workflow(self, entry: SignInEntry, config: dict) -> list[Work]:
        return [
            Work(
                url='/',
                method=self.sign_in_by_get,
                succeed_regex=['已签到'],
                assert_state=(check_sign_in_state, SignState.NO_SIGN_IN),
                is_base_content=True,
            ),
            Work(
                url='/showup.php',
                method=self.sign_in_by_ocr,
                succeed_regex=['{"success":true,"message":\\d+}'],
                fail_regex='{"success":false,"message":"invalid_imagehash"}',
                assert_state=(check_final_state, SignState.SUCCEED),
            ),
        ]

    def sign_in_by_ocr(self, entry: SignInEntry, config: dict, work: Work, last_content: str) -> Response | None:
        data = {
            'action': (None, 'new')
        }
        image_hash_url = urljoin(entry['url'], self.IMAGE_HASH_URL)
        image_hash_response = self.request(entry, 'post', image_hash_url, files=data)
        image_hash_network_state = check_network_state(entry, image_hash_url, image_hash_response)
        if image_hash_network_state != NetworkState.SUCCEED:
            return None
        content = net_utils.decode(image_hash_response)

        if not (image_hash := json.loads(content)['code']):
            entry.fail_with_prefix('Cannot find: image_hash')
            return None
        image_url = urljoin(entry['url'], self.IMAGE_URL)
        img_url = image_url.format(image_hash)
        img_response = self.request(entry, 'get', img_url)
        img_network_state = check_network_state(entry, img_url, img_response)
        if img_network_state != NetworkState.SUCCEED:
            return None
        img = Image.open(BytesIO(img_response.content))
        code, img_byte_arr = baidu_ocr.get_ocr_code(img, entry, config)
        if code and len(code) == 6:
            data = {
                'action': (None, 'showup'),
                'imagehash': (None, image_hash),
                'imagestring': (None, code)
            }
            return self.request(entry, 'post', work.url, files=data)
        return None

    @property
    def details_selector(self) -> dict:
        selector = super().details_selector
        net_utils.dict_merge(selector, {
            'user_id': None,
            'detail_sources': {
                'default': {
                    'link': None,
                    'elements': {
                        'bar': '#info_block > tbody > tr > td > table > tbody > tr > td:nth-child(1) > span',
                        'table': None
                    }
                }
            },
            'details': {
                'join_date': None,
                'hr': None
            }
        })
        return selector
