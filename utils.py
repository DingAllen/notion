def page_id(source_id):
    return source_id[:8] + '-' + source_id[8:12] + '-' + source_id[12:16] + '-' + source_id[16:20] + '-' + source_id[20:]