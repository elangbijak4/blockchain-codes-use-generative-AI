# -*- coding: utf-8 -*-
"""Untitled145.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1hElzHNJPIs6efI-dKYyWQgSeOVEkgQUK

KODE BLOCKCHAIN PRIVATE SEDERHANA
"""

import hashlib
import json
from time import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Membuat blok genesis
        self.new_block(previous_hash="", proof=100)

    def new_block(self, proof, previous_hash=None):
        """
        Buat blok baru dalam blockchain

        :param proof: Bukti yang diperoleh melalui proses penambangan
        :param previous_hash: Hash dari blok sebelumnya
        :return: Blok baru
        """

        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]) if self.chain else None,
            'current_hash': None  # Inisialisasi current hash
        }

        # Menghitung hash dari blok itu sendiri
        block['current_hash'] = self.hash(block)

        # Reset transaksi saat ini
        self.current_transactions = []

        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        Tambahkan transaksi baru ke dalam daftar transaksi saat ini

        :param sender: Alamat pengirim
        :param recipient: Alamat penerima
        :param amount: Jumlah yang dikirim
        :return: Index dari blok yang akan menyimpan transaksi ini
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        Buat SHA-256 hash dari sebuah blok

        :param block: Blok
        :return: Hash dalam format string
        """

        # Pastikan dictionary diurutkan untuk memastikan konsistensi hash
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """
        Mengembalikan blok terakhir dalam blockchain
        """
        return self.chain[-1]

    def proof_of_work(self, last_proof):
        """
        Algoritma Proof of Work:
         - Cari bilangan p' sedemikian sehingga hash(p * p') memiliki 4 nol di depan.

        :param last_proof: Bukti dari blok sebelumnya
        :return: Bukti baru
        """
        proof = 0
        while self.valid_proof(last_proof, proof) is False:
            proof += 1

        return proof

    @staticmethod
    def valid_proof(last_proof, proof):
        """
        Validasi bukti: Apakah hash(last_proof * proof) memiliki 4 nol di depan?

        :param last_proof: Bukti sebelumnya
        :param proof: Bukti saat ini
        :return: True jika valid, False jika tidak
        """
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

"""PROSES RUNNING BLOCKHAIN"""

# Inisialisasi blockchain
blockchain = Blockchain()

# Tambahkan transaksi baru
blockchain.new_transaction("Arif", "Santi", 6)

# Mulai penambangan blok baru
last_block = blockchain.last_block
last_proof = last_block['proof']
proof = blockchain.proof_of_work(last_proof)

proof

# Hadiahkan penambang dengan 1 koin
blockchain.new_transaction(
    sender="0",
    recipient="Pembuat blok",
    amount=1,
)

# Buat blok baru
previous_hash = blockchain.hash(last_block)
block = blockchain.new_block(proof, previous_hash)

print("Blockchain:", json.dumps(blockchain.chain, indent=4))

