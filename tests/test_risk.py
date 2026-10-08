from decimal import Decimal as D
from mfp_bot.config import Settings
from mfp_bot.risk import RiskEngine

def settings():
    return Settings('', '', '', '', False, ('BTCUSDT',), 'binance', D('5'),D('7.5'),D('15'),D('2440'),D('2425'),D('2725'),'15m','1h',D('1.8'))

def test_normal_trade_allowed():
    assert RiskEngine(settings()).gate(D('2500'),D('0'),0,0,D('5')).allowed

def test_emergency_stop():
    assert not RiskEngine(settings()).gate(D('2440'),D('0'),0,0,D('5')).allowed

def test_mll_stop():
    assert not RiskEngine(settings()).gate(D('2425'),D('0'),0,0,D('5')).allowed

def test_daily_stop():
    assert not RiskEngine(settings()).gate(D('2500'),D('-15'),0,0,D('5')).allowed

def test_position_size():
    assert RiskEngine.position_size(D('5'),D('100'),D('99.5')) == D('10')
