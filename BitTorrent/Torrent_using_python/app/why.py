import json
import sys
import hashlib
import bencodepy
import requests
import struct
import socket
import time

def decode_bencode(bencoded_value):
    if chr(bencoded_value[0]).isdigit():
        first_colon_index = bencoded_value.find(b":")
        if first_colon_index == -1:
            raise ValueError("Invalid encoded value")
        length = int(bencoded_value[:first_colon_index])
        return bencoded_value[first_colon_index + 1:first_colon_index + 1 + length], bencoded_value[first_colon_index + 1 + length:]
    
    elif chr(bencoded_value[0]) == "i" and chr(bencoded_value[-1]) == "e":
        end_index = bencoded_value.find(b"e")
        if end_index == -1:
            raise ValueError("Invalid encoded integer")
        return int(bencoded_value[1:end_index]), bencoded_value[end_index + 1:]
    
    elif chr(bencoded_value[0]) == "l":
        bencoded_value = bencoded_value[1:]  # Skip 'l'
        result = []
        while bencoded_value[0] != ord('e'):
            item, bencoded_value = decode_bencode(bencoded_value)
            result.append(item)
        return result, bencoded_value[1:]  # Skip 'e'
    
    elif chr(bencoded_value[0]) == "d":
        bencoded_value = bencoded_value[1:]  # Skip 'd'
        result = {}
        while bencoded_value[0] != ord('e'):
            key, bencoded_value = decode_bencode(bencoded_value)
            if not isinstance(key, bytes):
                raise ValueError("Dictionary key must be a byte string")
            value, bencoded_value = decode_bencode(bencoded_value)
            result[key.decode()] = value
        return result, bencoded_value[1:]  # Skip 'e'
    
    else:
        raise NotImplementedError("Unsupported Bencoded value")

def bytes_to_str(data):
    if isinstance(data, bytes):
        return data.decode()
    elif isinstance(data, list):
        return [bytes_to_str(item) for item in data]
    elif isinstance(data, dict):
        return {bytes_to_str(k): bytes_to_str(v) for k, v in data.items()}
    elif isinstance(data, int):
        return data
    raise TypeError(f"Type not serializable: {type(data)}")

def compute_info_hash(info):
    info_bencoded = bencodepy.encode(info)
    sha1_hash = hashlib.sha1(info_bencoded).digest()
    return sha1_hash.hex()

def compute_info_hash2(info):
    info_bencoded = bencodepy.encode(info)
    sha1_hash = hashlib.sha1(info_bencoded).digest()
    return sha1_hash

def send_message(s, message_id, payload=b''):
    message = struct.pack('>I', len(payload) + 1) + struct.pack('B', message_id) + payload
    print(f"Sending message: Length: {len(payload) + 1}, ID: {message_id}, Payload: {payload.hex()}")
    interested_payload = struct.pack(">IB", 1, 2)
    s.sendall(interested_payload)

def receive_message(s):
    length_prefix = recv_all(s, 4)
    length = struct.unpack('>I', length_prefix)[0]
    message_id = recv_all(s, 1)
    payload = recv_all(s, length - 1)
    print(f"Received message: Length: {length}, ID: {message_id[0]}, Payload: {payload.hex()}")
    return message_id[0], payload

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Failed to receive data")
        data += chunk
    return data

def download_piece(peer_ip, peer_port, torrent_file, piece_index, output_file):
    with open(torrent_file, 'rb') as f:
        torrent_data, _ = decode_bencode(f.read())
        info = torrent_data['info']
        piece_length = info['piece length']
        pieces = info['pieces']

    expected_hash = pieces[piece_index * 20:(piece_index + 1) * 20]
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(30)  # Set a longer timeout
        try:
            s.connect((peer_ip, peer_port))
        except socket.error as e:
            print(f"Failed to connect to peer {peer_ip}:{peer_port}: {e}")
            return

        # Send interested message
        send_message(s, 2)
        
        # Wait for unchoke message
        try:
            message_id, _ = receive_message(s)
            if message_id == 5:  # Choke message received
                print("Received choke message, retrying with another peer")
                return
            elif message_id != 1:
                print(f"Expected unchoke message but received: {message_id}")
                return
        except (ConnectionError, socket.error) as e:
            print(f"Error receiving unchoke message: {e}")
            return

        # Send request messages for each block of the piece
        num_blocks = (piece_length + 16383) // 16384  # Calculate number of blocks
        piece_data = bytearray(piece_length)
        for i in range(num_blocks):
            begin = i * 16384
            length = min(16384, piece_length - begin)
            payload = struct.pack('>I', piece_index) + struct.pack('>I', begin) + struct.pack('>I', length)
            send_message(s, 6, payload)
            
            # Receive piece message
            try:
                message_id, block_data = receive_message(s)
                if message_id != 7:
                    print(f"Expected piece message but received: {message_id}")
                    return
                
                block_index, block_begin = struct.unpack('>II', block_data[:8])
                block_content = block_data[8:]
                piece_data[block_begin:block_begin + len(block_content)] = block_content
            except (ConnectionError, socket.error) as e:
                print(f"Error receiving piece data: {e}")
                return
        
        # Verify the piece
        piece_hash = hashlib.sha1(piece_data).digest()
        if piece_hash != expected_hash:
            print(f"Piece hash does not match. Expected: {expected_hash.hex()}, Got: {piece_hash.hex()}")
            return

        # Save the piece
        with open(output_file, 'wb') as f:
            f.write(piece_data)
        
        print(f"Piece {piece_index} downloaded to {output_file}")


def main():
    command = sys.argv[1]
    
    if command == "decode":
        bencoded_value = sys.argv[2].encode()
        decoded_value, _ = decode_bencode(bencoded_value)
        print(json.dumps(decoded_value, default=bytes_to_str))
    
    elif command == "info":
        file_name = sys.argv[2]
        with open(file_name, "rb") as torrent_file:
            bencoded_content = torrent_file.read()
        torrent, _ = decode_bencode(bencoded_content)
        print("Tracker URL:", torrent["announce"].decode())
        print("Length:", torrent["info"]["length"])
        info_hash = compute_info_hash(torrent["info"])
        print("Info Hash:", info_hash)
        print("Piece Length:", torrent["info"]["piece length"])
        print("Piece Hashes:")
        for i in range(0, len(torrent["info"]["pieces"]), 20):
            print(torrent["info"]["pieces"][i:i + 20].hex())
    
    elif command == "peers":
        file_name = sys.argv[2]
        with open(file_name, "rb") as torrent_file:
            bencoded_content = torrent_file.read()
        torrent, _ = decode_bencode(bencoded_content)
        tracker_url = torrent.get("announce", "").decode()
        info_hash = compute_info_hash2(torrent["info"])
        dict_for_making_req = {
            "info_hash": info_hash,
            "peer_id": "01234567890123456789",
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": torrent.get("info", {}).get("length", 0),
            "compact": 1,
        }
        response = requests.get(tracker_url, params=dict_for_making_req)
        response_dict, _ = decode_bencode(response.content)
        peers = response_dict.get("peers", b"")
        for i in range(0, len(peers), 6):
            ip = ".".join(str(b) for b in peers[i:i + 4])
            port = struct.unpack("!H", peers[i + 4:i + 6])[0]
            print(f"Peer: {ip}:{port}")
    
    elif command == "handshake":
        file_name = sys.argv[2]
        (ip, port) = sys.argv[3].split(":")
        with open(file_name, "rb") as file:
            bencoded_content = file.read()
        torrent, _ = decode_bencode(bencoded_content)
        info = torrent["info"]
        info_hash = compute_info_hash2(torrent["info"])
        handshake = (
            b"\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00"
            + info_hash
            + b"01234567890123456789"
        )
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(10)  # Set timeout to prevent hanging
            s.connect((ip, int(port)))
            s.send(handshake)
            response = s.recv(68)
            print(f"Peer ID: {response[48:].hex()}")

    elif command == "download_piece":
        if len(sys.argv) != 5:
            raise ValueError("Usage: download_piece <torrent file> <piece index> <output file>")
        file_name = sys.argv[2]
        piece_index = int(sys.argv[3])
        output_file = sys.argv[4]
        with open(file_name, "rb") as file:
            bencoded_content = file.read()
        torrent, _ = decode_bencode(bencoded_content)
        tracker_url = torrent.get("announce", "").decode()
        info_hash = compute_info_hash2(torrent["info"])
        dict_for_making_req = {
            "info_hash": info_hash,
            "peer_id": "01234567890123456789",
            "port": 6881,
            "uploaded": 0,
            "downloaded": 0,
            "left": torrent.get("info", {}).get("length", 0),
            "compact": 1,
        }
        response = requests.get(tracker_url, params=dict_for_making_req)
        response_dict, _ = decode_bencode(response.content)
        peers = response_dict.get("peers", b"")
        
        # Fetch peers from the tracker
        with open(file_name, 'rb') as f:
            torrent_data, _ = decode_bencode(f.read())
            info = torrent_data['info']
            piece_length = info['piece length']
            pieces = info['pieces']
        
        expected_hash = pieces[piece_index * 20:(piece_index + 1) * 20]

        for i in range(0, len(peers), 6):
            ip = ".".join(str(b) for b in peers[i:i + 4])
            port = struct.unpack("!H", peers[i + 4:i + 6])[0]
            print(f"Peer: {ip}:{port}")
            # Send requests to all peers
            info = torrent["info"]
            info_hash = compute_info_hash2(torrent["info"])
            handshake = (
                b"\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00"
                + info_hash
                + b"01234567890123456789"
            )
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((ip, int(port)))
                s.send(handshake)
                print(f"Peer ID: {s.recv(68)[48:].hex()}")
                
            try:
                send_message(s, 2)
                
                # Wait for unchoke message
                try:
                    message_id, _ = receive_message(s)
                    if message_id == 5:  # Choke message received
                        print("Received choke message, retrying with another peer")
                        return
                    elif message_id != 1:
                        print(f"Expected unchoke message but received: {message_id}")
                        return
                except (ConnectionError, socket.error) as e:
                    print(f"Error receiving unchoke message: {e}")
                    return

                # Send request messages for each block of the piece
                num_blocks = (piece_length + 16383) // 16384  # Calculate number of blocks
                piece_data = bytearray(piece_length)
                for i in range(num_blocks):
                    begin = i * 16384
                    length = min(16384, piece_length - begin)
                    payload = struct.pack('>I', piece_index) + struct.pack('>I', begin) + struct.pack('>I', length)
                    send_message(s, 6, payload)
                    
                    # Receive piece message
                    try:
                        message_id, block_data = receive_message(s)
                        if message_id != 7:
                            print(f"Expected piece message but received: {message_id}")
                            return
                        
                        block_index, block_begin = struct.unpack('>II', block_data[:8])
                        block_content = block_data[8:]
                        piece_data[block_begin:block_begin + len(block_content)] = block_content
                    except (ConnectionError, socket.error) as e:
                        print(f"Error receiving piece data: {e}")
                        return
                
                # Verify the piece
                piece_hash = hashlib.sha1(piece_data).digest()
                if piece_hash != expected_hash:
                    print(f"Piece hash does not match. Expected: {expected_hash.hex()}, Got: {piece_hash.hex()}")
                    return

                # Save the piece
                with open(output_file, 'wb') as f:
                    f.write(piece_data)
                
                print(f"Piece {piece_index} downloaded to {output_file}")
                break

            except Exception as e:
                print(f"Failed to download from peer {ip}:{port}: {e}")

    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()
