# -*- coding=utf-8 -*-

import logging
import os
import re

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

REGEX = re.compile(r'!\[\[(Pasted image \d+\.png)\]\]')


def rename_attachments(file_path: str) -> int:

    def replacer(m: re.Match[str]) -> str:
        basename = context['basename']
        root = context['cwd']
        index = context['index']
        dst_filename = ''
        dst_path = ''
        while True:
            dst_filename = f'{basename}-{index:03d}.png'
            dst_path = os.path.join(root, 'attachments', dst_filename)
            if not os.path.exists(dst_path):
                break
            index += 1

        src_filename = m.group(1)
        src_path = os.path.join(root, 'attachments', src_filename)
        logger.info('rename %s to %s', src_path, dst_path)
        os.rename(src_path, dst_path)

        r = f'![[{dst_filename}]]'
        context.update(index=index)
        return r

    filename = os.path.basename(file_path)
    context = {
        'index': 1,
        'basename': filename.rsplit('.', 1)[0],
        'cwd': os.getcwd(),
    }

    logger.info('reading %s', file_path)
    with open(file_path, 'rb') as f:
        content = f.read().decode()
        content = REGEX.sub(replacer, content)
    with open(file_path, 'wb') as f:
        f.write(content.encode())
    logger.info('dump to %s', file_path)
    return context['index']
