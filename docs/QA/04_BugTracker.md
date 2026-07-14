# Bug Tracker & Resolutions

Selama fase QA & UAT WA-08, kami memantau ketat potensi celah yang tersisa sebelum sistem mengudara.

## Ditemukan (Resolved)
1. **[MEDIUM] TypeError in ReportEngine**: Terdapat referensi yang merujuk pada `Role.value` namun seharusnya `Role.name`. (Terselesaikan pada sprint sebelumnya).
2. **[LOW] ModuleNotFoundError saat Testing**: Path ke `app.main` tidak terbaca saat Pytest karena `PYTHONPATH` tidak di-set di `pytest.ini`. (Diselesaikan).
3. **[LOW] Frontend Import Error**: Missing eksport `useAuth` karena perubahan struktur `contexts`. (Terselesaikan).
4. **[HIGH] API 404 Not Found on Work Activities**: Frontend menerima 404 saat hit ke `/current` dan `/me/today`. Akar masalah adalah duplikasi `prefix` di `APIRouter()` dan `include_router()`. (Terselesaikan).
5. **[MEDIUM] API 500 TypeError on /me/today**: Terjadi error 500 karena perbandingan offset-aware datetime (`datetime.now(timezone.utc)`) dengan offset-naive datetime (`a.created_at`) dari database SQLite. (Terselesaikan).

**Status Saat Ini:**  
- Critical Bugs: 0  
- High Bugs: 0  
- Medium Bugs: 0  
- Low Bugs: 0  

Sistem dinyatakan bebas bug-kritis dan siap pakai.
