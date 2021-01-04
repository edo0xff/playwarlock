from . import _playwarez_cc, _serieshd_tv, _cuevana3_io, _www3_animeflv_net

playwarez_cc = _playwarez_cc.PlaywarezCC()
serieshd_tv = _serieshd_tv.SeriesHDTV()
cuevana3_io = _cuevana3_io.Cuevana3IO()
www3_animeflv_net = _www3_animeflv_net.WWW3AnimeFlvNET()

sites = [
    playwarez_cc,
    serieshd_tv,
    cuevana3_io,
    www3_animeflv_net
]
