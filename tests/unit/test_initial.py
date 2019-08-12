import kv_recursive
import mock


class TestKV(object):

    def setup_method(self, method):
        # anytime client is called we can pass hvacclient
        self.hvacclient = mock.patch('hvac.Client').start()

    def teardown_method(self, method):
        self.hvacclient.stop()

    def test_trailing_slash(self):
        assert kv_recursive.ensure_trailing_slash("test/") == "test/"
        assert kv_recursive.ensure_trailing_slash("test") == "test/"
        assert kv_recursive.ensure_trailing_slash("test/super") == "test/super/"
        assert kv_recursive.ensure_trailing_slash("test/super/") == "test/super/"

    # list_path

    def test_list_path_v2(self):
        self.hvacclient.secrets.kv.v2.list_secrets.return_value = {'data': {'keys': ['test2']}}
        kv_list = kv_recursive.list_path(
                self.hvacclient,
                path='',
                kv_version=2,
                source_mount='secret',
                kv_list=['test']
            )

        assert kv_list == ['test', 'test2']
        assert self.hvacclient.secrets.kv.v2.list_secrets.called

    def test_list_path_v1(self):
        self.hvacclient.secrets.kv.v1.list_secrets.return_value = {'data': {'keys': ['test2']}}
        kv_list = kv_recursive.list_path(
                self.hvacclient,
                path='',
                kv_version=1,
                source_mount='secret',
                kv_list=['test']
            )

        assert kv_list == ['test', 'test2']
        assert self.hvacclient.secrets.kv.v1.list_secrets.called
