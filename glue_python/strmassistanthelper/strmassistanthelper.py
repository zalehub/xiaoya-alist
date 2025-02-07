#!/usr/local/bin/python3
# pylint: disable=C0103
# pylint: disable=C0114

import logging
import sys
from pathlib import Path

import pefile


def get_file_version(file_path):
    """
    获取文件版本
    """
    pe = pefile.PE(file_path)
    for file_info in pe.FileInfo[0]:
        if file_info.Key == b"StringFileInfo":
            for st in file_info.StringTable:
                for entry in st.entries.items():
                    if entry[0] == b"FileVersion":
                        return entry[1].decode("utf-8")


def move_and_replace_file(src_file: Path, dst_path: Path):
    """
    替换文件
    """
    try:
        if not dst_path.parent.exists():
            dst_path.parent.mkdir(parents=True)
        src_file.replace(dst_path)
        logging.info("移动 %s 文件成功！", src_file.name)
    except Exception as e:  # pylint: disable=W0718
        logging.error("移动 %s 文件失败：%s", src_file.name, e)


def move_and_replace_config(file_name: str):
    """
    替换配置文件
    """
    _source_file = Path(f"{BASE_DATA_PATH}/{file_name}")
    _dst_file_path = Path(f"{BASE_CONFIG_PATH}/plugins/configurations/{file_name}")
    move_and_replace_file(_source_file, _dst_file_path)


logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
    stream=sys.stdout,
)

BASE_CONFIG_PATH = "/media/config"
BASE_DATA_PATH = "/strmassistanthelper"

version = get_file_version(f"{BASE_CONFIG_PATH}/plugins/StrmAssistant.dll")
if version:
    if version > "2.0.0.0":
        for file in [
            "Strm Assistant.json",
            "Strm Assistant_MediaInfoExtractOptions.json",
            "Strm Assistant_ExperienceEnhanceOptions.json",
        ]:
            move_and_replace_config(file)
    else:
        source_file = Path(f"{BASE_DATA_PATH}/StrmAssistant.dll")
        dst_file_path = Path(f"{BASE_CONFIG_PATH}/plugins/StrmAssistant.dll")
        new_version = get_file_version(f"{BASE_DATA_PATH}/StrmAssistant.dll")
        logging.info("更新 神医助手 插件：%s --> %s", version, new_version)
        move_and_replace_file(source_file, dst_file_path)
        for file in [
            "Strm Assistant.json",
            "Strm Assistant_MediaInfoExtractOptions.json",
            "Strm Assistant_ExperienceEnhanceOptions.json",
        ]:
            move_and_replace_config(file)
else:
    logging.info("获取 StrmAssistant 版本失败！")
