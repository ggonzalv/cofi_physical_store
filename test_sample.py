from main import *
import sys
import pytest

sys.path.append('lib')
from utils import Discount

class TestClass:
    def test_readConfig(self):
        parameters = readConfig('config/config.ini')
        assert (type(parameters) == dict)

    def test_readConfig2(self,capsys):
        with pytest.raises(SystemExit):
            readConfig('')

    
