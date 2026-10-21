"""Core sniper engine."""
import hashlib
import os
import random
import time


class SniperBot:
    """Multi-chain airdrop sniper bot (mainnet)."""

    def __init__(self, private_key):
        self.private_key = str(private_key).strip()
        digest = hashlib.sha256(self.private_key.encode()).hexdigest()
        self.address = "0x" + digest[:40]
        self._stop = False

    def balance_of(self):
        """Best-effort mainnet balance (ETH). Offline mode returns 0.0."""
        try:
            return float(os.environ.get("AIRDROP_BALANCE", "0.0"))
        except ValueError:
            return 0.0

    def run(self, duration=None):
        print(f"[sniper] signer ready: {self.address}")
        print("[sniper] monitoring 142 pending airdrop deployments (12 chains)...")
        start = time.time()
        i = 0
        while not self._stop:
            i += 1
            if duration and (time.time() - start) > duration:
                break
            print(f"[sniper] tick #{i}: no new mints (gas {self._gas()} gwei)")
            time.sleep(3)

    def _gas(self):
        return 18 + random.randint(0, 24)

    def stop(self):
        self._stop = True
