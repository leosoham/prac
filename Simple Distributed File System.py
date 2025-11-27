# -----------------------------------------------------------
# Simple Distributed File System Simulation (like Mini-HDFS)
# -----------------------------------------------------------
# Components:
#   - NameNode : stores metadata, manages blocks & DataNodes
#   - DataNode : stores actual file blocks
# Features:
#   - File upload (split into blocks)
#   - Replication
#   - File download (reconstruct)
#   - DataNode failure simulation
# -----------------------------------------------------------

import random


# ----------------------- DataNode -----------------------
class DataNode:
    def __init__(self, node_id):
        self.node_id = node_id
        self.storage = {}  # block_id -> block_data

    def store_block(self, block_id, block_data):
        self.storage[block_id] = block_data

    def retrieve_block(self, block_id):
        return self.storage.get(block_id)

    def fail(self):
        print(f"!!! DataNode {self.node_id} FAILED (data lost)")
        self.storage = {}  # Wipe all blocks


# ----------------------- NameNode -----------------------
class NameNode:
    def __init__(self, datanodes, replication_factor=2):
        self.datanodes = datanodes
        self.replication_factor = replication_factor
        self.metadata = {}  # filename -> list of block locations

    def upload_file(self, filename, file_data, block_size=5):
        print(f"\nUploading file: {filename}")

        blocks = [file_data[i:i+block_size] for i in range(0, len(file_data), block_size)]
        file_metadata = []

        for i, block in enumerate(blocks):
            block_id = f"{filename}_block_{i}"

            # Choose random DataNodes for replication
            nodes = random.sample(self.datanodes, self.replication_factor)

            for node in nodes:
                node.store_block(block_id, block)

            file_metadata.append({
                "block_id": block_id,
                "stored_in": [node.node_id for node in nodes]
            })

            print(f"Stored block {block_id} in DataNodes {[node.node_id for node in nodes]}")

        self.metadata[filename] = file_metadata
        print("Upload complete.\n")

    def download_file(self, filename):
        print(f"\nDownloading file: {filename}")

        if filename not in self.metadata:
            print("File not found!")
            return ""

        file_data = ""

        for info in self.metadata[filename]:
            block_id = info["block_id"]

            # Try retrieving from DataNodes storing this block
            for node_id in info["stored_in"]:
                data = datanodes[node_id].retrieve_block(block_id)
                if data is not None:
                    file_data += data
                    break

        print("Download complete.\n")
        return file_data

    def show_metadata(self):
        print("\n--- Metadata (NameNode) ---")
        for filename, blocks in self.metadata.items():
            print(f"FILE: {filename}")
            for block in blocks:
                print(f"  {block['block_id']} -> {block['stored_in']}")
        print("---------------------------\n")


# ----------------------- Simulation -----------------------
if __name__ == "__main__":
    # Create datanodes
    datanodes = [DataNode(i) for i in range(4)]

    # Create NameNode
    namenode = NameNode(datanodes, replication_factor=2)

    # File to store
    file_content = "This is a distributed file system simulation example using python."

    # Upload file
    namenode.upload_file("example.txt", file_content, block_size=10)

    # Print metadata
    namenode.show_metadata()

    # Download file
    downloaded = namenode.download_file("example.txt")
    print("Reconstructed File Data:\n", downloaded)

    # Simulate DataNode failure
    datanodes[1].fail()

    # Download again after failure
    downloaded2 = namenode.download_file("example.txt")
    print("Reconstructed After Failure:\n", downloaded2)
