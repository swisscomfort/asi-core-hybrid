"""
ASI-Core Storacha Integration
Automatisiert Uploads zu Storacha für dezentrale Speicherung
"""

import os
import subprocess
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional


class StorachaUploader:
    """Handles uploads to Storacha decentralized storage"""

    def __init__(self, log_file: str = "storacha-uploads.log"):
        self.log_file = log_file
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """Setup logging for upload operations"""
        logger = logging.getLogger("storacha_uploader")
        logger.setLevel(logging.INFO)

        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        return logger

    def check_cli_available(self) -> bool:
        """Check if Storacha CLI is available"""
        try:
            result = subprocess.run(
                ["storacha", "--version"], capture_output=True, text=True, check=True
            )
            self.logger.info("Storacha CLI verfügbar: %s", result.stdout.strip())
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            self.logger.error("Storacha CLI nicht verfügbar")
            return False

    def upload_file(self, file_path: str) -> Optional[str]:
        """Upload a single file to Storacha"""
        if not os.path.exists(file_path):
            self.logger.error("Datei nicht gefunden: %s", file_path)
            return None

        try:
            self.logger.info("Uploading %s...", file_path)
            result = subprocess.run(
                ["storacha", "up", file_path],
                capture_output=True,
                text=True,
                check=True,
            )

            # Extract URL from output
            for line in result.stdout.split("\n"):
                if "storacha.link" in line:
                    upload_url = line.strip().replace("🐔 ", "")
                    self.logger.info("Upload erfolgreich: %s", upload_url)
                    self._log_upload(file_path, upload_url)
                    return upload_url

        except subprocess.CalledProcessError as error:
            self.logger.error("Upload fehlgeschlagen: %s", error)
            self.logger.error("Output: %s", error.stdout)
            self.logger.error("Error: %s", error.stderr)

        return None

    def upload_directory(self, dir_path: str) -> Optional[str]:
        """Upload an entire directory to Storacha"""
        if not os.path.isdir(dir_path):
            self.logger.error("Verzeichnis nicht gefunden: %s", dir_path)
            return None

        try:
            self.logger.info("Uploading directory %s...", dir_path)
            result = subprocess.run(
                ["storacha", "up", dir_path], capture_output=True, text=True, check=True
            )

            # Extract URL from output
            for line in result.stdout.split("\n"):
                if "storacha.link" in line:
                    upload_url = line.strip().replace("🐔 ", "")
                    self.logger.info("Directory upload erfolgreich: %s", upload_url)
                    self._log_upload(dir_path, upload_url)
                    return upload_url

        except subprocess.CalledProcessError as error:
            self.logger.error("Directory upload fehlgeschlagen: %s", error)
            self.logger.error("Output: %s", error.stdout)
            self.logger.error("Error: %s", error.stderr)

        return None

    def upload_asi_core_snapshot(self) -> Optional[str]:
        """Upload a complete ASI-Core project snapshot"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_dir = f"asi-core-snapshot-{timestamp}"

        try:
            # Create snapshot directory
            os.makedirs(snapshot_dir, exist_ok=True)

            # Copy important files
            important_files = [
                "README.md",
                "main.py",
                "requirements.txt",
                "ASI_System_Dokumentation.md",
            ]

            for file in important_files:
                if os.path.exists(file):
                    subprocess.run(["cp", file, snapshot_dir], check=True)

            # Copy important directories
            important_dirs = ["src", "config"]
            for dir_name in important_dirs:
                if os.path.isdir(dir_name):
                    subprocess.run(["cp", "-r", dir_name, snapshot_dir], check=True)

            # Upload snapshot
            snapshot_url = self.upload_directory(snapshot_dir)

            # Cleanup
            subprocess.run(["rm", "-rf", snapshot_dir], check=True)

            return snapshot_url

        except subprocess.CalledProcessError as error:
            self.logger.error("Snapshot creation failed: %s", error)
            # Cleanup on error
            if os.path.exists(snapshot_dir):
                subprocess.run(["rm", "-rf", snapshot_dir], check=True)
            return None

    def _log_upload(self, path: str, upload_url: str):
        """Log upload details to file"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "path": path,
            "url": upload_url,
        }

        with open(self.log_file, "a", encoding="utf-8") as log_file:
            log_file.write(f"{json.dumps(log_entry)}\n")

    def list_uploads(self) -> List[Dict]:
        """List all previous uploads"""
        uploads = []
        if os.path.exists(self.log_file):
            with open(self.log_file, "r", encoding="utf-8") as log_file:
                for line in log_file:
                    line = line.strip()
                    if line:
                        try:
                            uploads.append(json.loads(line))
                        except json.JSONDecodeError:
                            # Handle old format (timestamp: url)
                            if ": " in line:
                                timestamp, upload_url = line.split(": ", 1)
                                uploads.append(
                                    {
                                        "timestamp": timestamp,
                                        "path": "unknown",
                                        "url": upload_url,
                                    }
                                )
        return uploads


# Usage example
if __name__ == "__main__":
    uploader = StorachaUploader()

    if not uploader.check_cli_available():
        print("❌ Storacha CLI nicht verfügbar")
        exit(1)

    print("🚀 ASI-Core Storacha Integration")
    print("1. Test upload")
    print("2. Upload README.md")
    print("3. Upload complete snapshot")
    print("4. List previous uploads")

    choice = input("Wähle eine Option (1-4): ")

    if choice == "1":
        # Create test file
        with open("test-python-upload.txt", "w", encoding="utf-8") as test_file:
            test_file.write(f"Python Storacha Integration Test - " f"{datetime.now()}")
        test_url = uploader.upload_file("test-python-upload.txt")
        if test_url:
            print(f"✅ Test upload erfolgreich: {test_url}")

    elif choice == "2":
        readme_url = uploader.upload_file("README.md")
        if readme_url:
            print(f"✅ README.md upload erfolgreich: {readme_url}")

    elif choice == "3":
        snapshot_url = uploader.upload_asi_core_snapshot()
        if snapshot_url:
            print(f"✅ Snapshot upload erfolgreich: {snapshot_url}")

    elif choice == "4":
        uploads = uploader.list_uploads()
        print(f"\n📋 Previous uploads ({len(uploads)}):")
        for upload in uploads[-10:]:  # Show last 10
            print(f"  {upload['timestamp']}: {upload['url']}")

    else:
        print("❌ Ungültige Option")
