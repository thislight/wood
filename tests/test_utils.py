
from unittest import mock
import wood.utils as t_utils

def test_can_make_uri_tuple():
    t = (r"/uri","back")
    
    t2 = t_utils.make_uri_tuple(*t)

    assert t == t2

@mock.patch('tornado.web.RequestHandler')
def test_can_get_info_from_handler_return_dict(mock_handler):
    info = t_utils.get_info(mock_handler)

    assert info.__class__ is dict


def test_uploaded_file_can_make():
    obj = t_utils.UploadedFile("name",b"text")

    assert obj.name and obj.body


@mock.patch('tornado.httputil.HTTPServerRequest')
def test_uploaded_file_can_make_from_request_files(mock_request):
    mock_request.files.returnvalue = [{'filename':'xxx.xxxx','body':b'xxxx'}]

    obj = t_utils.UploadedFile.from_reqfile(mock_request.files[0])

    assert obj.name and obj.body


def test_uploaded_file_can_get_one_name():
    obj = t_utils.UploadedFile("xxx",b"xxx")

    name = obj.one_name()

    assert name.__class__ is str

