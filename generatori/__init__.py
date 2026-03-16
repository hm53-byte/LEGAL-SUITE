from generatori.ugovori import (
    generiraj_prilagodeni_ugovor,
    generiraj_ugovor_standard,
    generiraj_ugovor_o_radu,
    generiraj_otkaz,
    generiraj_aneks_ugovora_o_radu,
    generiraj_upozorenje_radniku,
    generiraj_ugovor_rad_na_daljinu,
    generiraj_sporazumni_prestanak,
    generiraj_zabranu_natjecanja,
    generiraj_potvrdu_o_zaposlenju,
)
from generatori.tuzbe import generiraj_tuzbu_pro, generiraj_brisovnu_tuzbu
from generatori.ovrhe import (
    generiraj_ovrhu_pro,
    generiraj_prigovor_ovrhe,
    generiraj_ovrhu_ovrsna_isprava,
    generiraj_ovrhu_na_nekretnini,
    generiraj_ovrhu_na_placi,
    generiraj_obustavu_ovrhe,
    generiraj_privremenu_mjeru,
)
from generatori.zalbe import generiraj_zalbu_pro
from generatori.zemljisne import (
    generiraj_tabularnu_doc,
    generiraj_zk_prijedlog,
    generiraj_zabilježbu,
    generiraj_predbiježbu,
    generiraj_upis_hipoteke,
    generiraj_brisanje_hipoteke,
    generiraj_upis_sluznosti,
)
from generatori.opomene import generiraj_opomenu
from generatori.punomoci import generiraj_punomoc
from generatori.trgovacko import (
    generiraj_drustveni_ugovor,
    generiraj_odluku_skupstine,
    generiraj_prijenos_udjela,
    generiraj_nda,
    generiraj_zapisnik_uprave,
)
from generatori.obvezno import (
    generiraj_darovanje,
    generiraj_cesiju,
    generiraj_kompenzaciju,
    generiraj_jamstvo,
    generiraj_ugovor_o_gradenju,
    generiraj_licenciju,
    generiraj_posredovanje,
    generiraj_sporazumni_raskid,
)
from generatori.obiteljsko import (
    generiraj_sporazum_razvod,
    generiraj_tuzbu_razvod,
    generiraj_bracni_ugovor,
    generiraj_roditeljsku_skrb,
    generiraj_ugovor_uzdrzavanje,
)
from generatori.upravno import (
    generiraj_zalbu_zup,
    generiraj_tuzbu_zus,
    generiraj_zahtjev_informacije,
    generiraj_prigovor_predstavku,
)
from generatori.kazneno import (
    generiraj_kaznenu_prijavu,
    generiraj_privatnu_tuzbu,
    generiraj_zalbu_kaznena_presuda,
)
from generatori.stecajno import (
    generiraj_prijedlog_stecaj,
    generiraj_prijavu_trazbine,
    generiraj_stecaj_potrosaca,
)
from generatori.potrosaci import (
    generiraj_reklamaciju,
    generiraj_jednostrani_raskid,
    generiraj_prijavu_inspekciji,
)
