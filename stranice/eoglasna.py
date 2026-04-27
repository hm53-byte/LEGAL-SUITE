# =============================================================================
# STRANICE/EOGLASNA.PY - e-Oglasna ploca sudova (outbound link placeholder)
# =============================================================================
# Pristup javnoj e-Oglasnoj ploci nije podrzan u proizvodu zbog politike
# privatnosti tijela ("Ugradene su zastite od prikupljanja podataka Internet
# pretrazivaca s e-oglasne ploce"). Korisnik se preusmjerava na sluzbeni izvor.
import streamlit as st


def render_eoglasna():
    """Placeholder stranica koja preusmjerava na sluzbenu e-Oglasnu plocu."""
    st.header("Sudske objave (e-Oglasna ploca)")
    st.caption(
        "e-Oglasna ploca sudova je sluzbeni javni sustav Ministarstva pravosuda RH."
    )

    st.info(
        "**Pristup e-Oglasnoj ploci nije ugraden u proizvod.** "
        "Politika privatnosti sluzbenog sustava izricito navodi tehnicke zastite "
        "od automatskog dohvacanja podataka. Korisnici za vlastiti uvid u objave "
        "(dostave pismena, drazbe, stecajni postupci, ovrhe) mogu posjetiti "
        "izravno sluzbeni portal."
    )

    st.link_button(
        "Otvori e-Oglasnu plocu",
        "https://e-oglasna.pravosudje.hr/",
        type="primary",
        use_container_width=True,
    )

    st.markdown("---")
    st.caption(
        "Razdoblje cuvanja objava na sluzbenom sustavu: u pravilu 8 dana "
        "(cl. 145 Zakona o parnicnom postupku), do 60 dana za pojedine vrste "
        "objava (npr. cl. 25 Zakona o stecaju potrosaca)."
    )
