# Optimeringskurs

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pyomo](https://img.shields.io/badge/Pyomo-6.x-orange?style=for-the-badge)
![Solver](https://img.shields.io/badge/Solver-GLPK%20%7C%20IPOPT-green?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-blue?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-In%20Progress-yellow?style=for-the-badge)

Oppgaver og modeller fra et kurs i matematisk optimering. Bruker **Pyomo** som modelleringsspråk og løsere som **GLPK** (lineære/heltallsproblemer) og **IPOPT** (ikke-lineære problemer).

---

## Innhold

| Fil | Type | Beskrivelse |
|-----|------|-------------|
| `fabrikk.py` | Lineær programmering (MIP) | Maksimerer profitt for en fabrikk som produserer to produkter under kostnads-, CO₂- og malingsrestriksjoner |
| `optimering.py` | Ikke-lineær optimering (NLP) | Finner optimal lokasjon for et nytt kontor basert på avstand og kostnad til eksisterende kontorer |
| `hydro.py` | Lineær programmering (LP) | Minimerer materialkostnad for aluminiumslegeringer (Hydro-oppgave) med kjemiske krav og lagerbegrensninger |

---

## Modeller

### Fabrikk (fabrikk.py)

Bestemmer hvor mange enheter av produkt **A** og **B** en fabrikk skal produsere for å maksimere nettoprofitten.

**Beslutningsvariabler:**
- $x_A$ — antall enheter av produkt A
- $x_B$ — antall enheter av produkt B

**Objektivfunksjon:**
$$\max \quad (p_A - k_A) \cdot x_A + (p_B - k_B) \cdot x_B$$

**Restriksjoner:**
| Restriksjon | Grense |
|-------------|--------|
| Total produksjonskostnad | ≤ 10 000 000 kr |
| CO₂-utslipp | ≤ 20 000 kg (20 tonn) |
| Malingstimer (5 FTE) | ≤ 8 750 timer |

---

### Kontorlokasjon (optimering.py)

Finner den optimale geografiske plasseringen $(x, y)$ for et nytt kontor slik at vektet avstand til eksisterende kontorer minimeres.

**Objektivfunksjon:**
$$\min \quad \sum_{k} c_k \cdot \sqrt{(x - x_k)^2 + (y - y_k)^2}$$

---

### Hydro — Aluminiumslegering (hydro.py)

Finner optimal blanding av råmaterialer for å produsere aluminiumslegeringer til minimalkostnad.

**Del 1** — Produksjonsplan for én charge (maks 25 tonn).
**Del 2** — Produksjonsplaner for alle ordre samtidig med delt lagerbeholdning.

**Beslutningsvariabler:**
- $x_i$ — antall tonn av råmateriale $i$ som brukes

**Objektivfunksjon:**
$$\min \quad \sum_{i} \text{kostnad}_i \cdot x_i$$

**Restriksjoner:**
| Restriksjon | Beskrivelse |
|-------------|-------------|
| Totalt vekt | = ordrevekt |
| Lagerbeholdning | $x_i \leq \text{stock}_i$ |
| Si, Fe, Mg | innenfor min/maks-prosent per ordre |
| Ovnskapasitet | ≤ 25 tonn per charge |

---

## Kom i gang

### Krav

```bash
pip3 install pyomo
brew install glpk          # GLPK-solver (MIP/LP)
brew install ipopt         # IPOPT-solver (NLP)
```

> Ingen eksterne Python-pakker utover Pyomo — CSV-lesing bruker innebygd `csv`-modul.

### Kjør modellene

```bash
python3 fabrikk.py
python3 optimering.py
python3 hydro.py
```

---

## Teknologi

| Verktøy | Rolle |
|---------|-------|
| [Pyomo](http://www.pyomo.org/) | Modelleringsspråk for optimering i Python |
| [GLPK](https://www.gnu.org/software/glpk/) | Løser for lineære og heltallsproblemer |
| [IPOPT](https://github.com/coin-or/Ipopt) | Løser for ikke-lineære problemer |

---

## Bidragsytere

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/sondreNodenes">
        <img src="https://github.com/sondreNodenes.png" width="80px" alt="sondreNodenes"/><br/>
        <sub><b>sondreNodenes</b></sub>
      </a>
    </td>
  </tr>
</table>
