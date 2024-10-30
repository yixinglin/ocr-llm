from urllib.parse import urlparse, urlunparse, quote


def encode_url(url):
    # 对URL的路径部分进行编码
    parsed_url = urlparse(url)
    encoded_path = quote(parsed_url.path)

    # 构造完整的URL
    encoded_url = urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        encoded_path,
        parsed_url.params,
        parsed_url.query,
        parsed_url.fragment
    ))
    return encoded_url