# youtube - **Still under development**
Python Client for YouTube using Google's Private InnerTube API

## Installation
The `youtube` library uses [Poetry](https://github.com/python-poetry/poetry) and can easily be installed from source, or using *pip*

### From Source (using *pip*)
```console
$ pip install git+https://github.com/tombulled/youtube
Successfully installed youtube
$
```

## Usage
```python
>>> import youtube
>>>
>>> # ...
```

## Parsed Endpoints
|                                | Parsed  | Device Used |
| ------------------------------ | ------- | ----------- |
| config                         | &cross; |             |
| browse                         | &cross; |             |
| player                         | &check; | Android     |
| next                           | &check; | Web         |
| search                         | &cross; |             |
| guide                          | &check; | Android     |
| watch                          | &check; | Web         |
| get_video_info                 | &check; | Web         |
| comment_service_ajax           | &cross; |             |
