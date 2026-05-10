"""Bulanık sistemi Streamlit'siz hızlıca test et."""
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

# Antesedanlar
ic_sicaklik    = ctrl.Antecedent(np.arange(0, 41, 0.5),   'ic_sicaklik')
dis_sicaklik   = ctrl.Antecedent(np.arange(-10, 46, 0.5), 'dis_sicaklik')
nem            = ctrl.Antecedent(np.arange(0, 101, 1),    'nem')
kisi_sayisi    = ctrl.Antecedent(np.arange(0, 11, 1),     'kisi_sayisi')
saat           = ctrl.Antecedent(np.arange(0, 24, 1),     'saat')
fan_hizi       = ctrl.Consequent(np.arange(0, 101, 1),    'fan_hizi')
isi_guc        = ctrl.Consequent(np.arange(-100, 101, 1), 'isi_guc')

ic_sicaklik['soguk']  = fuzz.trapmf(ic_sicaklik.universe, [0, 0, 10, 16])
ic_sicaklik['serin']  = fuzz.trimf (ic_sicaklik.universe, [14, 18, 22])
ic_sicaklik['ideal']  = fuzz.trimf (ic_sicaklik.universe, [20, 23, 26])
ic_sicaklik['ilik']   = fuzz.trimf (ic_sicaklik.universe, [24, 28, 32])
ic_sicaklik['sicak']  = fuzz.trapmf(ic_sicaklik.universe, [30, 34, 40, 40])

dis_sicaklik['cok_soguk'] = fuzz.trapmf(dis_sicaklik.universe, [-10, -10, 0, 8])
dis_sicaklik['soguk']     = fuzz.trimf (dis_sicaklik.universe, [5, 12, 18])
dis_sicaklik['iliman']    = fuzz.trimf (dis_sicaklik.universe, [15, 22, 28])
dis_sicaklik['sicak']     = fuzz.trapmf(dis_sicaklik.universe, [25, 32, 45, 45])

nem['kuru']       = fuzz.trapmf(nem.universe, [0, 0, 25, 40])
nem['normal']     = fuzz.trimf (nem.universe, [35, 50, 65])
nem['nemli']      = fuzz.trimf (nem.universe, [60, 72, 85])
nem['cok_nemli']  = fuzz.trapmf(nem.universe, [80, 90, 100, 100])

kisi_sayisi['az']   = fuzz.trimf(kisi_sayisi.universe, [0, 0, 3])
kisi_sayisi['orta'] = fuzz.trimf(kisi_sayisi.universe, [2, 4, 6])
kisi_sayisi['cok']  = fuzz.trapmf(kisi_sayisi.universe, [5, 7, 10, 10])

saat['gece']  = fuzz.trapmf(saat.universe, [0, 0, 5, 7])
saat['sabah'] = fuzz.trimf (saat.universe, [6, 9, 12])
saat['oglen'] = fuzz.trimf (saat.universe, [11, 14, 17])
saat['aksam'] = fuzz.trapmf(saat.universe, [16, 19, 23, 23])

fan_hizi['kapali']   = fuzz.trimf(fan_hizi.universe, [0, 0, 15])
fan_hizi['dusuk']    = fuzz.trimf(fan_hizi.universe, [10, 25, 45])
fan_hizi['orta']     = fuzz.trimf(fan_hizi.universe, [35, 55, 70])
fan_hizi['yuksek']   = fuzz.trimf(fan_hizi.universe, [60, 75, 90])
fan_hizi['maksimum'] = fuzz.trapmf(fan_hizi.universe, [80, 92, 100, 100])

isi_guc['guclu_sogutma'] = fuzz.trapmf(isi_guc.universe, [-100, -100, -75, -50])
isi_guc['sogutma']       = fuzz.trimf (isi_guc.universe, [-65, -40, -15])
isi_guc['kapali']        = fuzz.trimf (isi_guc.universe, [-20, 0, 20])
isi_guc['isitma']        = fuzz.trimf (isi_guc.universe, [15, 40, 65])
isi_guc['guclu_isitma']  = fuzz.trapmf(isi_guc.universe, [50, 75, 100, 100])

rules = [
    ctrl.Rule(ic_sicaklik['sicak'] & dis_sicaklik['sicak'] & kisi_sayisi['cok'],     [fan_hizi['maksimum'], isi_guc['guclu_sogutma']]),
    ctrl.Rule(ic_sicaklik['sicak'] & nem['cok_nemli'],                                [fan_hizi['maksimum'], isi_guc['guclu_sogutma']]),
    ctrl.Rule(ic_sicaklik['sicak'] & dis_sicaklik['iliman'],                          [fan_hizi['yuksek'], isi_guc['sogutma']]),
    ctrl.Rule(ic_sicaklik['ilik'] & kisi_sayisi['cok'],                               [fan_hizi['yuksek'], isi_guc['sogutma']]),
    ctrl.Rule(ic_sicaklik['ilik'] & nem['nemli'],                                     [fan_hizi['yuksek'], isi_guc['sogutma']]),
    ctrl.Rule(ic_sicaklik['ilik'] & kisi_sayisi['az'] & saat['gece'],                 [fan_hizi['orta'], isi_guc['kapali']]),
    ctrl.Rule(ic_sicaklik['ideal'] & kisi_sayisi['orta'],                             [fan_hizi['dusuk'], isi_guc['kapali']]),
    ctrl.Rule(ic_sicaklik['ideal'] & kisi_sayisi['az'] & saat['gece'],                [fan_hizi['kapali'], isi_guc['kapali']]),
    ctrl.Rule(ic_sicaklik['ideal'] & nem['cok_nemli'],                                [fan_hizi['orta'], isi_guc['kapali']]),
    ctrl.Rule(ic_sicaklik['ideal'] & kisi_sayisi['cok'],                              [fan_hizi['orta'], isi_guc['kapali']]),
    ctrl.Rule(ic_sicaklik['serin'] & dis_sicaklik['cok_soguk'],                       [fan_hizi['dusuk'], isi_guc['isitma']]),
    ctrl.Rule(ic_sicaklik['serin'] & saat['sabah'],                                   [fan_hizi['dusuk'], isi_guc['isitma']]),
    ctrl.Rule(ic_sicaklik['serin'] & kisi_sayisi['az'],                               [fan_hizi['dusuk'], isi_guc['isitma']]),
    ctrl.Rule(ic_sicaklik['soguk'] & dis_sicaklik['cok_soguk'],                       [fan_hizi['orta'], isi_guc['guclu_isitma']]),
    ctrl.Rule(ic_sicaklik['soguk'] & dis_sicaklik['soguk'],                           [fan_hizi['dusuk'], isi_guc['guclu_isitma']]),
    ctrl.Rule(ic_sicaklik['soguk'] & saat['gece'],                                    [fan_hizi['dusuk'], isi_guc['guclu_isitma']]),
    ctrl.Rule(ic_sicaklik['soguk'] & kisi_sayisi['cok'],                              [fan_hizi['orta'], isi_guc['isitma']]),
    ctrl.Rule(nem['kuru'] & ic_sicaklik['ilik'],                                      [fan_hizi['orta'], isi_guc['sogutma']]),
    ctrl.Rule(saat['oglen'] & dis_sicaklik['sicak'] & ic_sicaklik['ilik'],            [fan_hizi['yuksek'], isi_guc['sogutma']]),
    ctrl.Rule(saat['aksam'] & ic_sicaklik['ideal'] & kisi_sayisi['orta'],             [fan_hizi['dusuk'], isi_guc['kapali']]),
]

hvac_ctrl = ctrl.ControlSystem(rules)
sim = ctrl.ControlSystemSimulation(hvac_ctrl)

test_cases = [
    ('Yaz ogleni kalabalik',  35, 38, 70, 8, 14),
    ('Kis gecesi az kisi',    12, -5, 40, 1, 2),
    ('Ideal bahar',           22, 20, 50, 3, 11),
    ('Tropikal',              32, 30, 92, 4, 15),
    ('Soguk sabah ofis',      15, 5,  45, 7, 8),
    ('Aksam ideal',           23, 22, 55, 4, 19),
    ('Buz gibi bos oda',      8,  -8, 35, 0, 4),
    ('Serin sabah',           18, 10, 50, 2, 7),
]

print(f"{'Senaryo':<25} {'Fan%':>8} {'Guc':>8} {'Mod':>12}")
print('-' * 60)
for ad, ics, diss, nms, kss, sts in test_cases:
    sim.input['ic_sicaklik']  = ics
    sim.input['dis_sicaklik'] = diss
    sim.input['nem']          = nms
    sim.input['kisi_sayisi']  = kss
    sim.input['saat']         = sts
    sim.compute()
    f = sim.output.get('fan_hizi', 0)
    g = sim.output.get('isi_guc', 0)
    mod = 'Sogutma' if g < -10 else ('Isitma' if g > 10 else 'Beklemede')
    print(f"{ad:<25} {f:>8.1f} {g:>+8.1f} {mod:>12}")

print()
print("OK - Tum senaryolar basariyla calisti!")
