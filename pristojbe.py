# -----------------------------------------------------------------------------
# KALKULATOR SUDSKIH PRISTOJBI
# Prema Zakonu o sudskim pristojbama (NN 118/18) i Uredbi o tarifi (NN 129/19)
# Svi iznosi u EUR (konvertirani iz HRK po tecaju 7.53450)
# -----------------------------------------------------------------------------


def _zaokruzi_na_cente(iznos):
    """Zaokruzuje na 2 decimale."""
    return round(iznos, 2)


# =============================================================================
# TARIFNI BROJEVI - Pristojbe za parnicni postupak (Tbr. 1-5)
# =============================================================================

def pristojba_tuzba(vps):
    """Izracunava sudsku pristojbu za tuzbu prema VPS-u.
    Tbr. 1 Tarife sudskih pristojbi.
    vps: vrijednost predmeta spora u EUR
    """
    if vps <= 0:
        return 0.0

    # Tarifni razredi (konvertirani iz HRK)
    if vps <= 664.0:  # do 5.000 HRK
        return 13.27  # 100 HRK
    elif vps <= 1_327.0:  # 5.001 - 10.000 HRK
        return 26.54  # 200 HRK
    elif vps <= 3_318.0:  # 10.001 - 25.000 HRK
        return 53.09  # 400 HRK
    elif vps <= 6_636.0:  # 25.001 - 50.000 HRK
        return 79.63  # 600 HRK
    elif vps <= 13_272.0:  # 50.001 - 100.000 HRK
        return 119.45  # 900 HRK
    elif vps <= 26_544.0:  # 100.001 - 200.000 HRK
        return 199.08  # 1.500 HRK
    elif vps <= 66_361.0:  # 200.001 - 500.000 HRK
        return 398.17  # 3.000 HRK
    elif vps <= 132_722.0:  # 500.001 - 1.000.000 HRK
        return 663.61  # 5.000 HRK
    else:  # preko 1.000.000 HRK
        # 5.000 HRK + 1% na iznos iznad 1.000.000 HRK, max 33.180 HRK
        dodatno = (vps - 132_722.0) * 0.01
        ukupno = 663.61 + dodatno
        maks = 4_404.15  # 33.180 HRK
        return _zaokruzi_na_cente(min(ukupno, maks))


def pristojba_presuda(vps):
    """Pristojba za presudu = ista kao za tuzbu. Tbr. 2."""
    return pristojba_tuzba(vps)


def pristojba_zalba(vps):
    """Pristojba za zalbu = dvostruki iznos pristojbe za tuzbu. Tbr. 3."""
    return _zaokruzi_na_cente(pristojba_tuzba(vps) * 2)


def pristojba_revizija(vps):
    """Pristojba za reviziju = trostruki iznos pristojbe za tuzbu. Tbr. 4."""
    return _zaokruzi_na_cente(pristojba_tuzba(vps) * 3)


# =============================================================================
# OVRSNI POSTUPAK (Tbr. 10-14)
# =============================================================================

def pristojba_ovrha_jb(vps):
    """Pristojba za prijedlog za ovrhu na temelju vjerodostojne isprave.
    Tbr. 10 - polovica pristojbe za tuzbu, min 6.64 EUR (50 HRK).
    """
    iznos = pristojba_tuzba(vps) / 2
    return _zaokruzi_na_cente(max(iznos, 6.64))


def pristojba_ovrha_ovrsna_isprava(vps):
    """Pristojba za prijedlog za ovrhu na temelju ovrsne isprave.
    Tbr. 11 - polovica pristojbe za tuzbu, min 6.64 EUR.
    """
    iznos = pristojba_tuzba(vps) / 2
    return _zaokruzi_na_cente(max(iznos, 6.64))


def pristojba_prigovor_ovrhe(vps):
    """Pristojba za prigovor na rjesenje o ovrsi. Tbr. 12 - kao tuzba."""
    return pristojba_tuzba(vps)


# =============================================================================
# IZVANPARNICNI I ZK POSTUPAK (Tbr. 20-25)
# =============================================================================

def pristojba_zk_prijedlog():
    """Fiksna pristojba za ZK prijedlog (uknjizba, predzabilježba, zabiljezba).
    Tbr. 20 - 33.18 EUR (250 HRK).
    """
    return 33.18


def pristojba_zk_brisanje():
    """Pristojba za brisanje upisa u ZK.
    Tbr. 21 - 13.27 EUR (100 HRK).
    """
    return 13.27


def pristojba_zk_izvadak():
    """Pristojba za ZK izvadak.
    Tbr. 22 - 5.31 EUR (40 HRK).
    """
    return 5.31


# =============================================================================
# UPRAVNI SPOR (Tbr. 30)
# =============================================================================

def pristojba_upravni_spor():
    """Fiksna pristojba za tuzbu u upravnom sporu.
    Tbr. 30 - 26.54 EUR (200 HRK).
    """
    return 26.54


# =============================================================================
# OSTALE PRISTOJBE
# =============================================================================

def pristojba_punomoc():
    """Pristojba na punomoc za zastupanje.
    Tbr. 40 - 6.64 EUR (50 HRK).
    """
    return 6.64


def pristojba_prigovor_zup():
    """Pristojba na zalbu u upravnom postupku (ZUP) - bez pristojbe.
    Zalbe u upravnom postupku su oslobodene pristojbe.
    """
    return 0.0


# =============================================================================
# OSLOBODENJA OD PRISTOJBI
# =============================================================================

OSLOBODENJA = [
    "Radni sporovi (tuzitelj - radnik)",
    "Uzdrzavanje djece i bracnog druga",
    "Postupci iz Obiteljskog zakona",
    "Kazneni postupak (oštećenik)",
    "Upravni spor - socijalna prava",
    "Izvrsenje presude Europskog suda za ljudska prava",
    "Postupci zastite potrosaca do 1.327 EUR",
    "Stecajni postupak - prijava trazbine",
]


def provjeri_oslobodenje(vrsta_spora):
    """Provjerava je li postupak osloboden od sudskih pristojbi."""
    oslobodeni = {
        "radni_spor": True,
        "uzdrzavanje": True,
        "obiteljski": True,
        "kazneni_ostecenik": True,
        "upravni_socijalni": True,
        "stecaj_prijava": True,
    }
    return oslobodeni.get(vrsta_spora, False)


# =============================================================================
# POMOCNA FUNKCIJA - Ukupni izracun
# =============================================================================

def izracunaj_pristojbu(tip_postupka, vps=0.0, **kwargs):
    """Centralna funkcija za izracun pristojbe.
    tip_postupka: 'tuzba', 'zalba', 'ovrha_jb', 'ovrha_ovrsna', 'prigovor_ovrhe',
                  'zk_prijedlog', 'zk_brisanje', 'upravni_spor', 'punomoc'
    vps: vrijednost predmeta spora (za VPS-ovisne pristojbe)
    """
    kalkulatori = {
        'tuzba': lambda: pristojba_tuzba(vps),
        'presuda': lambda: pristojba_presuda(vps),
        'zalba': lambda: pristojba_zalba(vps),
        'revizija': lambda: pristojba_revizija(vps),
        'ovrha_jb': lambda: pristojba_ovrha_jb(vps),
        'ovrha_ovrsna': lambda: pristojba_ovrha_ovrsna_isprava(vps),
        'prigovor_ovrhe': lambda: pristojba_prigovor_ovrhe(vps),
        'zk_prijedlog': lambda: pristojba_zk_prijedlog(),
        'zk_brisanje': lambda: pristojba_zk_brisanje(),
        'zk_izvadak': lambda: pristojba_zk_izvadak(),
        'upravni_spor': lambda: pristojba_upravni_spor(),
        'punomoc': lambda: pristojba_punomoc(),
        'zalba_zup': lambda: pristojba_prigovor_zup(),
    }
    kalkulator = kalkulatori.get(tip_postupka)
    if kalkulator:
        return kalkulator()
    return 0.0
