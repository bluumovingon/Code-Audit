from abc import ABC, abstractmethod
from dataclasses import dataclass

# --- DATA MODEL ---
@dataclass
class Mahasiswa:
    nama: str
    sks_diambil: int
    mata_kuliah_lulus: list[str]
    status_bayar: str = "belum_lunas"

# --- 1. ABSTRAKSI (Solusi DIP & OCP) ---
class IValidator(ABC):
    """Kontrak: Semua jenis validasi harus punya method 'validate'."""
    @abstractmethod
    def validate(self, mhs: Mahasiswa, requirement: any) -> bool:
        pass

# --- 2. IMPLEMENTASI LOGIC (Solusi OCP) ---
class SksValidator(IValidator):
    def validate(self, mhs: Mahasiswa, max_sks: int) -> bool:
        if mhs.sks_diambil > max_sks:
            print(f"VALIDASI: Gagal. SKS ({mhs.sks_diambil}) melebihi batas {max_sks}.")
            return False
        print("VALIDASI: SKS Aman.")
        return True

class PrerequisiteValidator(IValidator):
    def validate(self, mhs: Mahasiswa, matkul_syarat: str) -> bool:
        if matkul_syarat not in mhs.mata_kuliah_lulus:
            print(f"VALIDASI: Gagal. Belum lulus {matkul_syarat}.")
            return False
        print(f"VALIDASI: Prasyarat {matkul_syarat} terpenuhi.")
        return True

# --- 3. PEMISAHAN LOGGING (Solusi SRP) ---
class ValidationLogger:
    """Class khusus yang HANYA mengurus logging/pencatatan."""
    def log_success(self, mhs_name: str, val_type: str):
        print(f"[LOG SYSTEM]: Validasi '{val_type}' BERHASIL untuk {mhs_name}.")
    
    def log_failure(self, mhs_name: str, val_type: str):
        print(f"[LOG SYSTEM]: Validasi '{val_type}' GAGAL untuk {mhs_name}.")

# --- 4. MANAGER / SERVICE (Penerapan DIP) ---
class RegistrationService:
    def __init__(self, validator: IValidator, logger: ValidationLogger):
        # Dependency Injection: Bergantung pada Abstraksi IValidator
        self.validator = validator
        self.logger = logger

    def process_validation(self, mhs: Mahasiswa, requirement: any):
        print(f"\n--- Memproses {mhs.nama} ---")
        is_valid = self.validator.validate(mhs, requirement)
        
        # Delegasi ke Logger (SRP)
        validator_name = self.validator.__class__.__name__
        if is_valid:
            self.logger.log_success(mhs.nama, validator_name)
        else:
            self.logger.log_failure(mhs.nama, validator_name)

# ==========================================
#       MAIN PROGRAM & CHALLENGE (OCP)
# ==========================================

# Setup Data Dummy
mhs_andi = Mahasiswa("Andi", 24, ["Algoritma"], "lunas") # SKS berlebih
mhs_budi = Mahasiswa("Budi", 20, ["Algoritma"], "belum_lunas") 
logger = ValidationLogger()

print("=== SKENARIO 1: Validasi SKS & Prasyarat (Fitur Dasar) ===")

# 1. Cek SKS Andi (Batas 22)
sks_validator = SksValidator()
service_sks = RegistrationService(sks_validator, logger)
service_sks.process_validation(mhs_andi, 22)

# 2. Cek Prasyarat Budi (Harus lulus Algoritma)
prereq_validator = PrerequisiteValidator()
service_prereq = RegistrationService(prereq_validator, logger)
service_prereq.process_validation(mhs_budi, "Algoritma")


print("\n=== SKENARIO 2: Challenge Pembuktian OCP (Fitur Baru) ===")
# Soal: Tambahkan validasi Pembayaran TANPA mengedit class RegistrationService!

# Kita buat class baru (Extension)
class PaymentValidator(IValidator):
    def validate(self, mhs: Mahasiswa, required_status: str) -> bool:
        if mhs.status_bayar != required_status:
            print(f"VALIDASI: Gagal. Status bayar '{mhs.status_bayar}', harus '{required_status}'.")
            return False
        print("VALIDASI: Pembayaran Lunas.")
        return True

# Inject validator baru ke Service lama
payment_validator = PaymentValidator()
service_payment = RegistrationService(payment_validator, logger)

# Jalankan validasi pembayaran untuk Budi
service_payment.process_validation(mhs_budi, "lunas")

print("\nKESIMPULAN: Validasi Pembayaran ditambahkan tanpa mengubah RegistrationService.")