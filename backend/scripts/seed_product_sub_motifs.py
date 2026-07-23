import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database.session import SessionLocal
from app.models.product_master import ProductSubMotif

SUB_MOTIFS = [
    {"id": 1, "name": "GRANDMASTER SGE - COLOUR SERIES", "code": "GRSG_CS", "description": "GRANDMASTER SGE - COLOUR SERIES"},
    {"id": 2, "name": "GRANDMASTER SGE - BLACK SERIES", "code": "GRSG_BS", "description": "GRANDMASTER SGE - BLACK SERIES"},
    {"id": 3, "name": "GRANDMASTER SJL - COLOUR SERIES", "code": "GRSJ_CS", "description": "GRANDMASTER SJL - COLOUR SERIES"},
    {"id": 4, "name": "GRANDMASTER SJL - BLACK SERIES", "code": "GRSJ_BS", "description": "GRANDMASTER SJL - BLACK SERIES"},
    {"id": 5, "name": "GRANDMASTER SEI - COLOUR SERIES", "code": "GRSE_CS", "description": "GRANDMASTER SEI - COLOUR SERIES"},
    {"id": 6, "name": "GRANDMASTER SEI - BLACK SERIES", "code": "GRSE_BS", "description": "GRANDMASTER SEI - BLACK SERIES"},
    {"id": 7, "name": "FULL COLOUR", "code": "FC", "description": "FULL COLOUR"},
    {"id": 8, "name": "SOFT COLOUR", "code": "SC", "description": "SOFT COLOUR"},
    {"id": 9, "name": "BORDIR", "code": "BDR", "description": "BORDIR"},
    {"id": 10, "name": "BORDIR BLACK SERIES", "code": "BO_BS", "description": "BORDIR BLACK SERIES"},
    {"id": 11, "name": "FULL SERIES", "code": "FS", "description": "FULL SERIES"},
    {"id": 12, "name": "BLACK SERIES", "code": "BS", "description": "BLACK SERIES"},
    {"id": 13, "name": "SOFT SERIES", "code": "SS", "description": "SOFT SERIES"},
    {"id": 14, "name": "REALITY ELEGANT", "code": "REEL", "description": "REALITY ELEGANT"},
    {"id": 15, "name": "REALITY KRISTAL", "code": "REKR", "description": "REALITY KRISTAL"},
    {"id": 16, "name": "REALITY ORIENTAL", "code": "REOR", "description": "REALITY ORIENTAL"},
    {"id": 17, "name": "REALITY SERUMPUN", "code": "RESE", "description": "REALITY SERUMPUN"},
    {"id": 18, "name": "REALITY SERUMPUN WHITE SERIES", "code": "RESE_WS", "description": "REALITY SERUMPUN WHITE SERIES"},
    {"id": 19, "name": "REALITY TIGA DARA", "code": "RE_TD", "description": "REALITY TIGA DARA"},
    {"id": 20, "name": "REALITY TIGA DARA SERI HITAM", "code": "RETIDA_SH", "description": "REALITY TIGA DARA SERI HITAM"},
    {"id": 21, "name": "REALITY TIGA DARA SERI PUTIH", "code": "RETIDA_SP", "description": "REALITY TIGA DARA SERI PUTIH"},
    {"id": 22, "name": "REALITY BATIK BLACK SERIES", "code": "REBA_BS", "description": "REALITY BATIK BLACK SERIES"},
    {"id": 23, "name": "REALITY BATIK WHITE SERIES", "code": "REBA_WS", "description": "REALITY BATIK WHITE SERIES"},
    {"id": 24, "name": "SEA", "code": "SEA", "description": "SEA"},
    {"id": 25, "name": "SEA BLACK SERIES", "code": "SE_BS", "description": "SEA BLACK SERIES"},
    {"id": 26, "name": "SIA", "code": "SIA", "description": "SIA"},
    {"id": 27, "name": "SIA BLACK SERIES", "code": "SI_BS", "description": "SIA BLACK SERIES"},
    {"id": 28, "name": "SIC", "code": "SIC", "description": "SIC"},
    {"id": 29, "name": "SIC BLACK SERIES", "code": "SI_BS2", "description": "SIC BLACK SERIES"},
    {"id": 30, "name": "JIB", "code": "JIB", "description": "JIB"},
    {"id": 31, "name": "JIB BLACK SERIES", "code": "JI_BS", "description": "JIB BLACK SERIES"},
    {"id": 32, "name": "KAWUNG", "code": "KWG", "description": "KAWUNG"},
    {"id": 33, "name": "WD MASTER QUALITY GUS - BATIK GARUDA", "code": "WMQGBG", "description": "WD MASTER QUALITY GUS - BATIK GARUDA"},
    {"id": 34, "name": "WD MASTER QUALITY GUS - BATIK LASEMAN", "code": "WMQGBL", "description": "WD MASTER QUALITY GUS - BATIK LASEMAN"},
    {"id": 35, "name": "WD MASTER QUALITY GUS - BATIK SERIES", "code": "WMQGBS", "description": "WD MASTER QUALITY GUS - BATIK SERIES"},
    {"id": 36, "name": "WD MASTER QUALITY GUS - HITAM PUTIH", "code": "WMQGH_PTH", "description": "WD MASTER QUALITY GUS - HITAM PUTIH"},
    {"id": 37, "name": "WD MQ GUS - BATIK GODHONG", "code": "WMGBG", "description": "WD MQ GUS - BATIK GODHONG"},
    {"id": 38, "name": "WD MQ GUS - BATIK PRADAWITA", "code": "WMGBP", "description": "WD MQ GUS - BATIK PRADAWITA"},
    {"id": 39, "name": "WD MQ GUS - JENGGOLO", "code": "WDMQGUSJE", "description": "WD MQ GUS - JENGGOLO"},
    {"id": 40, "name": "WD MQ GUS - SATRIYA MUDA", "code": "WMGSM", "description": "WD MQ GUS - SATRIYA MUDA"},
    {"id": 41, "name": "DKI", "code": "DKI", "description": "DKI"},
    {"id": 42, "name": "DKI BLACK SERIES", "code": "DK_BS", "description": "DKI BLACK SERIES"},
    {"id": 43, "name": "SGE", "code": "SGE", "description": "SGE"},
    {"id": 44, "name": "SGE BLACK SERIES", "code": "SG_BS", "description": "SGE BLACK SERIES"},
    {"id": 45, "name": "KDT", "code": "KDT", "description": "KDT"},
    {"id": 46, "name": "NEW BALI PRINT SILKY", "code": "NBPS", "description": "NEW BALI PRINT SILKY"},
    {"id": 47, "name": "SERI WARNA", "code": "SW", "description": "SERI WARNA"},
    {"id": 48, "name": "BLACK EDITION", "code": "BE", "description": "BLACK EDITION"},
    {"id": 49, "name": "PINTO ACEH", "code": "PIA", "description": "PINTO ACEH"},
    {"id": 50, "name": "WARNA JINGGA", "code": "WAJI", "description": "WARNA JINGGA"},
    {"id": 51, "name": "WARNA KHUSUS", "code": "WAKH", "description": "WARNA KHUSUS"},
    {"id": 52, "name": "WHITE SERIES", "code": "WS", "description": "WHITE SERIES"},
    {"id": 53, "name": "TIMBUL POLOS TUMPAL PUTIH", "code": "TIPOTU_PTH", "description": "TIMBUL POLOS TUMPAL PUTIH"},
    {"id": 54, "name": "TIMBUL POLOS TUMPAL HITAM", "code": "TIPOTUHI", "description": "TIMBUL POLOS TUMPAL HITAM"},
    {"id": 55, "name": "TIMBUL KOTAK SERI HITAM", "code": "TIKO_SH", "description": "TIMBUL KOTAK SERI HITAM"},
    {"id": 56, "name": "TIMBUL KOTAK SERI PUTIH", "code": "TIKO_SP", "description": "TIMBUL KOTAK SERI PUTIH"},
    {"id": 57, "name": "WD JAWA BATIK - NYIUR", "code": "WDJABANY", "description": "WD JAWA BATIK - NYIUR"},
    {"id": 58, "name": "WD JAWA BATIK - ANYAM", "code": "WDJABAAN", "description": "WD JAWA BATIK - ANYAM"},
    {"id": 59, "name": "WD JAWA BATIK - BENGGOLO", "code": "WDJABABE", "description": "WD JAWA BATIK - BENGGOLO"},
    {"id": 60, "name": "WD JAWA BATIK - BERAS WUTAH", "code": "WDJABABEWU", "description": "WD JAWA BATIK - BERAS WUTAH"},
    {"id": 61, "name": "WD JAWA BATIK - BRASTAGI", "code": "WDJABABR", "description": "WD JAWA BATIK - BRASTAGI"},
    {"id": 62, "name": "WD JAWA BATIK - CEPLOKAN", "code": "WDJABACE", "description": "WD JAWA BATIK - CEPLOKAN"},
    {"id": 63, "name": "WD JAWA BATIK - GENTENGAN", "code": "WDJABAGE", "description": "WD JAWA BATIK - GENTENGAN"},
    {"id": 64, "name": "WD JAWA BATIK - HITAM PUTIH fx", "code": "WJBHPF", "description": "WD JAWA BATIK - HITAM PUTIH fx"},
    {"id": 65, "name": "WD JAWA BATIK - ILIR", "code": "WDJABAIL", "description": "WD JAWA BATIK - ILIR"},
    {"id": 66, "name": "WD JAWA BATIK - JAGAD", "code": "WDJABAJA", "description": "WD JAWA BATIK - JAGAD"},
    {"id": 67, "name": "WD JAWA BATIK - JOGJA", "code": "WDJABAJO", "description": "WD JAWA BATIK - JOGJA"},
    {"id": 68, "name": "WD JAWA BATIK - KAWUNG FX", "code": "WDJABAKAFX", "description": "WD JAWA BATIK - KAWUNG FX"},
    {"id": 69, "name": "WD JAWA BATIK - LIRIS ONDHO", "code": "WDJABALION", "description": "WD JAWA BATIK - LIRIS ONDHO"},
    {"id": 70, "name": "WD JAWA BATIK - LIRIS", "code": "WDJABALI", "description": "WD JAWA BATIK - LIRIS"},
    {"id": 71, "name": "WD JAWA BATIK - NAWASENA", "code": "WDJABANA", "description": "WD JAWA BATIK - NAWASENA"},
    {"id": 72, "name": "WD JAWA BATIK - NIRWANA", "code": "WDJABANI", "description": "WD JAWA BATIK - NIRWANA"},
    {"id": 73, "name": "WD JAWA BATIK - PRING", "code": "WDJABAPR", "description": "WD JAWA BATIK - PRING"},
    {"id": 74, "name": "WD JAWA BATIK - PRISAI", "code": "WDJABAPR2", "description": "WD JAWA BATIK - PRISAI"},
    {"id": 75, "name": "WD JAWA BATIK - PRIYANGAN", "code": "WDJABAPR3", "description": "WD JAWA BATIK - PRIYANGAN"},
    {"id": 76, "name": "WD JAWA BATIK - REMBANG", "code": "WDJABARE", "description": "WD JAWA BATIK - REMBANG"},
    {"id": 77, "name": "WD JAWA BATIK - SAMUDRA", "code": "WDJABASA", "description": "WD JAWA BATIK - SAMUDRA"},
    {"id": 78, "name": "WD JAWA BATIK - SEMI SENO", "code": "WDJABASESE", "description": "WD JAWA BATIK - SEMI SENO"},
    {"id": 79, "name": "WD JAWA BATIK - SENOTARUNG", "code": "WDJABASE", "description": "WD JAWA BATIK - SENOTARUNG"},
    {"id": 80, "name": "WD JAWA BATIK - SUKMO", "code": "WDJABASU", "description": "WD JAWA BATIK - SUKMO"},
    {"id": 81, "name": "WD JAWA BATIK - SULAM", "code": "WDJABASU2", "description": "WD JAWA BATIK - SULAM"},
    {"id": 82, "name": "WD JAWA BATIK - TERUMBU KARANG", "code": "WDJABATEKA", "description": "WD JAWA BATIK - TERUMBU KARANG"},
    {"id": 83, "name": "WD JAWA BATIK - TRESNO", "code": "WDJABATR", "description": "WD JAWA BATIK - TRESNO"},
    {"id": 84, "name": "WD JAWA BATIK - TRUNTUM RAJA", "code": "WDJABATRRA", "description": "WD JAWA BATIK - TRUNTUM RAJA"},
    {"id": 85, "name": "WD WAKANDA BATIK (PTB)", "code": "WDWABAPTB", "description": "WD WAKANDA BATIK (PTB)"},
    {"id": 86, "name": "WD BATIK JAWA KUNO - ARUTALA.pdf", "code": "WDBAJAKUAR", "description": "WD BATIK JAWA KUNO - ARUTALA.pdf"},
    {"id": 87, "name": "WD BATIK JAWA KUNO - CATUR MUKTI.pdf", "code": "WBJKCM", "description": "WD BATIK JAWA KUNO - CATUR MUKTI.pdf"},
    {"id": 88, "name": "WD BATIK JAWA KUNO - CEMORO.pdf", "code": "WDBAJAKUCE", "description": "WD BATIK JAWA KUNO - CEMORO.pdf"},
    {"id": 89, "name": "WD BATIK JAWA KUNO - DAHONO.pdf", "code": "WDBAJAKUDA", "description": "WD BATIK JAWA KUNO - DAHONO.pdf"},
    {"id": 90, "name": "WD BATIK JAWA KUNO - IKETAN.pdf", "code": "WDBAJAKUIK", "description": "WD BATIK JAWA KUNO - IKETAN.pdf"},
    {"id": 91, "name": "WD BATIK JAWA KUNO - MANGGARAN.pdf", "code": "WDBAJAKUMA", "description": "WD BATIK JAWA KUNO - MANGGARAN.pdf"},
    {"id": 92, "name": "WD BATIK JAWA KUNO - MAYANG.pdf", "code": "WDBAJAKUM2", "description": "WD BATIK JAWA KUNO - MAYANG.pdf"},
    {"id": 93, "name": "WD BATIK JAWA KUNO - NAWASENA.pdf", "code": "WDBAJAKUNA", "description": "WD BATIK JAWA KUNO - NAWASENA.pdf"},
    {"id": 94, "name": "WD BATIK JAWA KUNO - PUSPOWARNO.pdf", "code": "WDBAJAKUPU", "description": "WD BATIK JAWA KUNO - PUSPOWARNO.pdf"},
    {"id": 95, "name": "WD BATIK JAWA KUNO - RUPO TELU.pdf", "code": "WBJKRT", "description": "WD BATIK JAWA KUNO - RUPO TELU.pdf"},
    {"id": 96, "name": "WD BATIK JAWA KUNO - SEGARAN.pdf", "code": "WDBAJAKUSE", "description": "WD BATIK JAWA KUNO - SEGARAN.pdf"},
    {"id": 97, "name": "WD BATIK JAWA KUNO - SELARAS.pdf", "code": "WDBAJAKUS2", "description": "WD BATIK JAWA KUNO - SELARAS.pdf"},
    {"id": 98, "name": "WD BATIK JAWA KUNO - SEMILIR.pdf", "code": "WDBAJAKUS3", "description": "WD BATIK JAWA KUNO - SEMILIR.pdf"},
    {"id": 99, "name": "WD BATIK JAWA KUNO - SETYO.pdf", "code": "WDBAJAKUS4", "description": "WD BATIK JAWA KUNO - SETYO.pdf"},
    {"id": 100, "name": "WD BATIK JAWA KUNO - TANJUNG.pdf", "code": "WDBAJAKUTA", "description": "WD BATIK JAWA KUNO - TANJUNG.pdf"},
    {"id": 101, "name": "WD BATIK JAWA KUNO - TRITIS.pdf", "code": "WDBAJAKUTR", "description": "WD BATIK JAWA KUNO - TRITIS.pdf"},
    {"id": 102, "name": "WD BATIK JAWA KUNO - UKELAN.pdf", "code": "WDBAJAKUUK", "description": "WD BATIK JAWA KUNO - UKELAN.pdf"},
    {"id": 103, "name": "POLOS PUTIH", "code": "PLPT", "description": "POLOS PUTIH"},
    {"id": 104, "name": "HAWAI", "code": "HWI", "description": "HAWAI"},
    {"id": 105, "name": "LURIK", "code": "LRK", "description": "LURIK"},
    {"id": 106, "name": "MANIK-MANIK", "code": "MNK", "description": "MANIK-MANIK"},
    {"id": 107, "name": "MANISE", "code": "MNS", "description": "MANISE"},
    {"id": 108, "name": "POLOS FULLL COLOUR", "code": "PLFC", "description": "POLOS FULLL COLOUR"},
    {"id": 109, "name": "TIGA DARA", "code": "TD", "description": "TIGA DARA"},
    {"id": 110, "name": "HORIZON", "code": "HRZ", "description": "HORIZON"},
    {"id": 111, "name": "PUTIH", "code": "PTH", "description": "PUTIH"},
    {"id": 112, "name": "JOGAN (BLACK SERIES)", "code": "JOBLSE", "description": "JOGAN (BLACK SERIES)"},
    {"id": 113, "name": "JOGAN", "code": "JGN", "description": "JOGAN"},
    {"id": 114, "name": "KUTAI (BLACK SERIES) - (TRIPLE D)", "code": "KUBLSETRD", "description": "KUTAI (BLACK SERIES) - (TRIPLE D)"},
    {"id": 115, "name": "KUTAI - (TRIPLE D)", "code": "KUTRD", "description": "KUTAI - (TRIPLE D)"},
    {"id": 116, "name": "LIRIS - (TRIPLE C)", "code": "LITRC", "description": "LIRIS - (TRIPLE C)"},
    {"id": 117, "name": "MELAYU (TRIPLE F)", "code": "METRF", "description": "MELAYU (TRIPLE F)"},
    {"id": 118, "name": "MELAYU - (BLACK SERIES) - (TRIPLE F)", "code": "MEBLSETRF", "description": "MELAYU - (BLACK SERIES) - (TRIPLE F)"},
    {"id": 119, "name": "NEW - (BLACK SERIES)", "code": "NEWBLSE", "description": "NEW - (BLACK SERIES)"},
    {"id": 120, "name": "NEW - (COLOUR SERIES)", "code": "NEWCOSE", "description": "NEW - (COLOUR SERIES)"},
    {"id": 121, "name": "PENAJAM (TRIPLE E)", "code": "PETRE", "description": "PENAJAM (TRIPLE E)"},
    {"id": 122, "name": "PENAJAM - (BLACK SERIES) - (TRIPLE E)", "code": "PEBLSETRE", "description": "PENAJAM - (BLACK SERIES) - (TRIPLE E)"},
    {"id": 123, "name": "PINTO ACEH - (BLACK SERIES) - (TRIPLE A)", "code": "PASA", "description": "PINTO ACEH - (BLACK SERIES) - (TRIPLE A)"},
    {"id": 124, "name": "PINTO ACEH - (TRIPLE A)", "code": "PIACTRA", "description": "PINTO ACEH - (TRIPLE A)"},
    {"id": 125, "name": "SAWIT - (TRIPLE J)", "code": "SATRJ", "description": "SAWIT - (TRIPLE J)"},
    {"id": 126, "name": "SINGKAWANG - (BLACK SERIES) - (TRIPLE H)", "code": "SIBLSETRH", "description": "SINGKAWANG - (BLACK SERIES) - (TRIPLE H)"},
    {"id": 127, "name": "SINGKAWANG - (TRIPLE H)", "code": "SITRH", "description": "SINGKAWANG - (TRIPLE H)"},
    {"id": 128, "name": "SONGKET IKAT (TRIPLE B)", "code": "SOIKTRB", "description": "SONGKET IKAT (TRIPLE B)"},
    {"id": 129, "name": "TALAWANG (BLACK SERIES) - (TRIPLE G)", "code": "TABLSETRG", "description": "TALAWANG (BLACK SERIES) - (TRIPLE G)"},
    {"id": 130, "name": "TALAWANG - (TRIPLE G)", "code": "TATRG", "description": "TALAWANG - (TRIPLE G)"},
    {"id": 131, "name": "TIKARAN (BLACK SERIES)", "code": "TIBLSE", "description": "TIKARAN (BLACK SERIES)"},
    {"id": 132, "name": "TIKARAN", "code": "TKR", "description": "TIKARAN"},
]


def seed_product_sub_motifs():
    db = SessionLocal()

    try:
        for sub in SUB_MOTIFS:
            exists = db.query(ProductSubMotif).filter(
                (ProductSubMotif.code == sub["code"]) | (ProductSubMotif.name == sub["name"])
            ).first()

            if exists:
                if not exists.description and sub.get("description"):
                    exists.description = sub["description"]
                    print(f"  Updated description for {sub['code']}")
                else:
                    print(f"ProductSubMotif {sub['code']} already exists.")
                db.flush()
                continue

            sub_data = {k: v for k, v in sub.items() if k != "id"}
            db.add(ProductSubMotif(**sub_data))
            db.flush()

        db.commit()
        print("Product sub motifs seeded successfully.")

    except Exception as e:
        db.rollback()
        print(e)

    finally:
        db.close()


if __name__ == "__main__":
    seed_product_sub_motifs()
