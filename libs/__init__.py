from . import _playwarez_cc, _serieshd_tv

playwarez_cc = _playwarez_cc.PlaywarezCC()
serieshd_tv = _serieshd_tv.SeriesHDTV()

sites = [
    playwarez_cc,
    serieshd_tv
]
