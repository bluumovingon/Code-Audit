# FILE: registration_bad.py
from dataclasses import dataclass

@dataclass
class Mahasiswa:
    nama: str
    sks_diambil: int
    mata_kuliah_lulus: list[str]

class ValidatorManager:
    # Masalah: Melanggar SRP (Validasi + Logging), OCP (If/Else), DIP (Hard dependency)
    def validate_registration(self, mhs: Mahasiswa, validation_type: str, requirement: any):
        print(f"Memulai validasi untuk {mhs.nama}...")

        # PELANGGARAN OCP & DIP:
        # Menggunakan if/else. Jika ada aturan baru "Cek Uang Kuliah", harus edit kode ini.
        if validation_type == "sks":
            if mhs.sks_diambil > requirement: # requirement adalah max_sks
                print(f"GAGAL: SKS berlebih ({mhs.sks_diambil} > {requirement})")
                return False
            print("SUKSES: SKS aman.")
        
        elif validation_type == "prasyarat":
            if requirement not in mhs.mata_kuliah_lulus: # requirement adalah matkul prasyarat
                print(f"GAGAL: Belum lulus prasyarat {requirement}")
                return False
            print("SUKSES: Prasyarat terpenuhi.")
        
        else:
            print("Tipe validasi tidak dikenal.")
            return False

        # PELANGGARAN SRP:
        # Mencampur logika bisnis dengan logika pencatatan (logging)
        print(f"LOG SYSTEM: Validasi {validation_type} selesai untuk {mhs.nama}.")
        return True