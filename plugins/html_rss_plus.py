from urllib.parse import urljoin

from flexget import plugin
from flexget.entry import Entry
from flexget.event import event
from flexget.task import Task
from flexget.utils.soup import get_soup
from loguru import logger
from requests import RequestException
import time

from .ptsites.utils import net_utils


class PluginHtmlRssPlus:
    schema = {
        'type': 'object',
        'properties': {
            'urls': {
                'type':'array',
                'items':{
                   'type': 'string',
                   'format': 'url',
                }
            },
            'user-agent': {'type': 'string'},
            'cookie': {'type': 'string'},
            'params': {'type': 'string'},
            'url_interval': {'type': 'integer'},
            "root_element_selector": {'type': 'string'},
            'fields': {
                'type': 'object',
                'properties': {
                    'title': {
                        'type': 'object',
                        'properties': {
                            'element_selector': {'type': 'string'},
                            'attribute': {'type': 'string'},
                        }
                    },
                    'url': {
                        'type': 'object',
                        'properties': {
                            'element_selector': {'type': 'string'},
                            'attribute': {'type': 'string'},
                        },
                    }
                },
                'required': ['title', 'url'],
            }
        },
        'required': ['urls', 'root_element_selector'],
        'additionalProperties': False
    }

    def prepare_config(self, config: dict) -> dict:
        config.setdefault('urls', '')
        config.setdefault('user-agent', '')
        config.setdefault('cookie', '')
        config.setdefault('params', '')
        config.setdefault('url_interval', 1)
        config.setdefault('root_element_selector', '')
        config.setdefault('fields', {})
        return config

    def on_task_input(self, task: Task, config: dict) -> list[Entry]:
        config = self.prepare_config(config)
        urls = config['urls']
        user_agent = config.get('user-agent')
        cookie = config.get('cookie')
        root_element_selector = config.get('root_element_selector')
        fields = config['fields']
        params = config['params']
        url_interval = config['url_interval']
        headers = {
            'accept-encoding': 'gzip, deflate, br',
            'user-agent': user_agent
        }
        entries: list[Entry] = []
        print("Urls:")
        print(*urls,sep='\n')
        for url in urls:
            try:
                task.requests.headers.update(headers)
                task.requests.cookies.update(net_utils.cookie_str_to_dict(cookie))
                response = task.requests.get(url, timeout=60)
                content = net_utils.decode(response)
            except RequestException as e:
                raise plugin.PluginError(
                    'Unable to download the Html for task {} ({}): {}'.format(task.name, url, e)
                )
            elements = get_soup(content).select(root_element_selector)
            total_torrents = len(elements)
            print(f"Total torrents: {total_torrents}!")
            if total_torrents == 0:
                logger.debug(f'no elements found in response: {content}')
                return entries

            for element in elements:
                logger.debug('element in element_selector: {}', element)
                entry = Entry()
                for key, value in fields.items():
                    entry[key] = ''
                    sub_element = element.select_one(value['element_selector'])
                    if sub_element:
                        if value['attribute'] == 'textContent':
                            sub_element_content = sub_element.get_text()
                        else:
                            sub_element_content = sub_element.get(value['attribute'], '')
                        entry[key] = sub_element_content
                    logger.debug('key: {}, value: {}', key, entry[key])
                if entry['title'] and entry['url']:
                    base_url = urljoin(url, entry['url'])
                    if params.startswith("&"):
                        entry['url'] = base_url + params
                    else:
                        entry['url'] = urljoin(base_url, params)
                    entry['original_url'] = entry['url']
                    entries.append(entry)
            time.sleep(url_interval)  
        return entries


@event('plugin.register')
def register_plugin() -> None:
    plugin.register(PluginHtmlRssPlus, 'html_rss_plus', api_ver=2)
