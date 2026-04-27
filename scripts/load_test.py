"""
load_test.py — Playwright load test za LegalTechSuite Pro

Pokrece N paralelnih virtualnih korisnika koji otvaraju lokalnu Streamlit
aplikaciju u Jednostavnom modu, kliknu prvu situacijsku karticu, i cekaju
da se prikazu detalji. Mjeri odzivna vremena u ms.

Setup (jednom):
    pip install playwright
    playwright install chromium

Pokretanje:
    # Terminal 1: pokreni app
    streamlit run LEGAL-SUITE.py

    # Terminal 2: load test
    python scripts/load_test.py -c 3        # 3 paralelna korisnika
    python scripts/load_test.py -c 10       # 10 paralelnih
    python scripts/load_test.py -c 5 --url http://localhost:8501
"""
from __future__ import annotations

import argparse
import asyncio
import statistics
import time

from playwright.async_api import async_playwright


DEFAULT_URL = "http://localhost:8501"


async def virtualni_korisnik(browser, korisnik_id: int, url: str, rezultati: dict) -> None:
    """Jedan virtualni korisnik: otvori app, klikni prvu karticu, cekaj detalje."""
    context = await browser.new_context()
    page = await context.new_page()
    pocetak = time.time()
    try:
        # 1. Otvori landing i cekaj da Jednostavni katalog renderira
        t0 = time.time()
        await page.goto(url, timeout=30_000)
        await page.wait_for_selector("text=Katalog blank obrazaca", timeout=25_000)
        rezultati["shell_load_ms"].append((time.time() - t0) * 1000)

        # 2. Klikni prvu "Odaberi" gumb (otvara detalje prve kartice u katalogu)
        t1 = time.time()
        await page.locator("button:has-text('Odaberi')").first.click(timeout=10_000)
        await page.wait_for_selector("text=Pravni temelj", timeout=15_000)
        rezultati["card_open_ms"].append((time.time() - t1) * 1000)

        rezultati["uspjesno"].append(True)
        rezultati["total_ms"].append((time.time() - pocetak) * 1000)
    except Exception as e:
        rezultati["uspjesno"].append(False)
        rezultati["greske"].append(f"K{korisnik_id}: {type(e).__name__}: {str(e)[:100]}")
    finally:
        await context.close()


def sazetak(naziv: str, vrijednosti: list[float]) -> None:
    """Print min/avg/p95/max ms vrijednosti."""
    if not vrijednosti:
        print(f"  {naziv}: nema podataka")
        return
    avg = statistics.mean(vrijednosti)
    p95 = sorted(vrijednosti)[max(0, int(0.95 * len(vrijednosti)) - 1)]
    print(f"  {naziv:22s} avg={avg:6.0f}ms  p95={p95:6.0f}ms  "
          f"min={min(vrijednosti):6.0f}ms  max={max(vrijednosti):6.0f}ms")


async def pokreni(konkurencija: int, url: str) -> None:
    rezultati = {
        "shell_load_ms": [],
        "card_open_ms": [],
        "total_ms": [],
        "uspjesno": [],
        "greske": [],
    }
    print(f"Load test: {konkurencija} paralelnih korisnika, URL={url}")
    print("Pokrecem virtualne korisnike...\n")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        pocetak_testa = time.time()
        await asyncio.gather(*[
            virtualni_korisnik(browser, i, url, rezultati)
            for i in range(konkurencija)
        ])
        ukupno = time.time() - pocetak_testa
        await browser.close()

    n = len(rezultati["uspjesno"])
    uspjesnih = sum(rezultati["uspjesno"])
    print("=" * 60)
    print(f"REZULTATI:  {uspjesnih}/{n} uspjesnih  ({uspjesnih/n*100:.0f}%)")
    print(f"Trajanje testa: {ukupno:.2f}s   Throughput: {n/ukupno:.2f} korisnika/s")
    print("\nVremena (ms):")
    sazetak("Shell load",            rezultati["shell_load_ms"])
    sazetak("Klik na karticu",       rezultati["card_open_ms"])
    sazetak("Total user journey",    rezultati["total_ms"])

    if rezultati["greske"]:
        print(f"\nGreske ({len(rezultati['greske'])}):")
        for g in rezultati["greske"][:10]:
            print(f"  - {g}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load test za LegalTechSuite Pro (lokalno)")
    parser.add_argument("-c", "--concurrency", type=int, default=3,
                        help="Broj paralelnih virtualnih korisnika (default: 3)")
    parser.add_argument("--url", default=DEFAULT_URL,
                        help=f"URL Streamlit aplikacije (default: {DEFAULT_URL})")
    args = parser.parse_args()
    asyncio.run(pokreni(args.concurrency, args.url))
