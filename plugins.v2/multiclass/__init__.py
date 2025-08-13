import random
import time
import shutil
import subprocess
import threading
from pathlib import Path
from typing import Any, List, Dict, Tuple

from app.core.config import settings
from app.core.context import MediaInfo
from app.core.event import eventmanager, Event
from app.log import logger
from app.plugins import _PluginBase
from app.schemas import TransferInfo
from app.schemas.file import FileItem
from app.schemas.types import ChainEventType, MediaType, NotificationType
from app.utils.system import SystemUtils

lock = threading.Lock()


class PlayletCategory(_PluginBase):
    # 插件名称
    plugin_name = "电影多级分类"
    # 插件描述
    plugin_desc = "支持电影按照年代和系列分类"
    # 插件图标
    plugin_icon = "Calibreweb_B.png"
    # 插件版本
    plugin_version = "1.0"
    # 插件作者
    plugin_author = "liuhangbin"
    # 作者主页
    author_url = "https://github.com/liuhangbin"
    # 插件配置项ID前缀
    plugin_config_prefix = "multiclass_"
    # 加载顺序
    plugin_order = 1
    # 可使用的用户级别
    auth_level = 1

    _enabled = False
    _notify = True

    def init_plugin(self, config: dict = None):

        if config:
            self._enabled = config.get("enabled")
            self._notify = config.get("notify")

    def get_state(self) -> bool:
        return True if self._enabled else False

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        pass

    def get_api(self) -> List[Dict[str, Any]]:
        pass

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
        """
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'year_class',
                                            'label': '按照年代分类',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'score_class',
                                            'label': '按照评分分类',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'series_class',
                                            'label': '按照系列分类',
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify',
                                            'label': '发送消息',
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '按评分分类，7-9 高分，4-6 一般，1-3 垃圾, 系列电影不参与评分.'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "notify": True,
            "year_class": False,
            "score_class": False,
            "series_class": False
        }

    def get_page(self) -> List[dict]:
        pass

    @eventmanager.register(ChainEventType.TransferRename)
    def category_handler(self, event: Event):
        """
        根据多级分类规则重新分类组装地址
        """
        logger.info(f"触发多级分类！")
        if not event:
            logger.info(f"多级分类异常：{event}")
            return
        if not self.get_state():
            logger.info(f"多级分类插件配置不完整！")
            return
        try:
            event_data = event.event_data
            path = Path(event_data.path)
            logger.info(f"event data is {event_data}")
            logger.info(f"event data: path {path}")
            event_data.updated = False
            event_data.source = "MultiClass"

            # 发送消息
            if self._notify:
                self.post_message(
                    mtype=NotificationType.Organize,
                    title="多级分类完成",
                    text=f"已重新分类xxx",
                )
        except Exception as e:
            logger.info(f"多级分类异常:{str(e)}")

    def stop_service(self):
    """
    停止服务
    """
    pass
