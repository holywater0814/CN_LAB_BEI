import json
import sys
import hashlib
import bencodepy
import requests
import struct
import socket
import time
import math

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
    length = s.recv(4)
    while not length or not int.from_bytes(length):
        length = s.recv(4)
    message = s.recv(int.from_bytes(length))
    # If we didn't receive the full message for some reason, keep gobbling.
    while len(message) < int.from_bytes(length):
        message += s.recv(int.from_bytes(length) - len(message))
    return length + message

def recv_all(sock, length):
    data = b''
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        if not chunk:
            raise ConnectionError("Failed to receive data")
        data += chunk
    return data
def get_peerip(torrent):
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
        return ip, port

def get_peer_id(peer_ip, peer_port, info_hash,torrent):
    info = torrent["info"]
    info_hash = compute_info_hash2(torrent["info"])
    handshake = (
        b"\x13BitTorrent protocol\x00\x00\x00\x00\x00\x00\x00\x00"
        + info_hash
        + b"01234567890123456789"
    )
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
           s.settimeout(10)  # Set timeout to prevent hanging
           s.connect((peer_ip, int(peer_port)))
           s.send(handshake)
        #    print(f"Peer ID: {s.recv(68)[48:].hex()}")
           return s.recv(68)[48:].hex()
        finally:
            s.close()

def extract_pieces_hashes(pieces_hashes):
    index, result = 0, []
    while index < len(pieces_hashes):
        result.append(pieces_hashes[index : index + 20].hex())
        index += 20
    return result

def download_piece(torrent, piece_index, output_file):
    peer_ip,peer_port = get_peerip(torrent)
    print(peer_ip,peer_port)
    peer_id =get_peer_id(peer_ip, peer_port,compute_info_hash2(torrent["info"]),torrent)
    print(f"Peer ID:",peer_id)
    protocol_name_length = struct.pack(">B", 19)
    protocol_name = b"BitTorrent protocol"
    reserved_bytes = b"\x00" * 8
    peer_id = b"01234567890123456789"
    payload = (
        protocol_name_length + protocol_name + reserved_bytes + compute_info_hash2(torrent["info"])+ peer_id
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((peer_ip, peer_port))
        sock.sendall(payload)
        response = sock.recv(68)
        message = receive_message(sock)
        while int(message[4]) != 5:
            message = receive_message(sock)
        interested_payload = struct.pack(">IB", 1, 2)
        sock.sendall(interested_payload)
        message = receive_message(sock)
        while int(message[4]) != 1:
            message = receive_message(sock)
        file_length = torrent["info"]["length"]
        total_number_of_pieces = len(
            extract_pieces_hashes(torrent["info"]["pieces"])
            
        )
        print(extract_pieces_hashes(torrent["info"]["pieces"]))
        checkpieces = extract_pieces_hashes(torrent["info"]["pieces"])
        print(checkpieces[0])
        print("Total no of pieces:", total_number_of_pieces)
        default_piece_length = torrent["info"]["piece length"]
        if piece_index == total_number_of_pieces - 1:
            piece_length = file_length - (default_piece_length * piece_index)
        else:
            piece_length = default_piece_length
        number_of_blocks = math.ceil(piece_length / (16 * 1024))
        data = bytearray()
        for block_index in range(number_of_blocks):
            begin = 2**14 * block_index
            print(f"begin: {begin}")
            block_length = min(piece_length - begin, 2**14)
            print(
                f"Requesting block {block_index + 1} of {number_of_blocks} with length {block_length}"
            )
            request_payload = struct.pack(
                ">IBIII", 13, 6, piece_index, begin, block_length
            )
            print("Requesting block, with payload:")
            print(request_payload)
            print(struct.unpack(">IBIII", request_payload))
            print(int.from_bytes(request_payload[:4]))
            print(int.from_bytes(request_payload[4:5]))
            print(int.from_bytes(request_payload[5:9]))
            print(int.from_bytes(request_payload[17:21]))
            sock.sendall(request_payload)
            message = receive_message(sock)
            data.extend(message[13:])
            
        with open(output_file, "wb") as f:
            f.write(data)
    finally:
        sock.close()
    return True

def download(torrent, output_file):
    peer_ip,peer_port = get_peerip(torrent)
    print(peer_ip,peer_port)
    peer_id =get_peer_id(peer_ip, peer_port,compute_info_hash2(torrent["info"]),torrent)
    print(f"Peer ID:",peer_id)
    protocol_name_length = struct.pack(">B", 19)
    protocol_name = b"BitTorrent protocol"
    reserved_bytes = b"\x00" * 8
    peer_id = b"01234567890123456789"
    payload = (
        protocol_name_length + protocol_name + reserved_bytes + compute_info_hash2(torrent["info"])+ peer_id
    )
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((peer_ip, peer_port))
        sock.sendall(payload)
        response = sock.recv(68)
        message = receive_message(sock)
        while int(message[4]) != 5:
            message = receive_message(sock)
        interested_payload = struct.pack(">IB", 1, 2)
        sock.sendall(interested_payload)
        message = receive_message(sock)
        while int(message[4]) != 1:
            message = receive_message(sock)
        file_length = torrent["info"]["length"]
        total_number_of_pieces = len(
            extract_pieces_hashes(torrent["info"]["pieces"])
            
        )
        data = bytearray()
        for piece_index in range(0,total_number_of_pieces):
            print("Total no of pieces:", total_number_of_pieces)
            default_piece_length = torrent["info"]["piece length"]
            if piece_index == total_number_of_pieces - 1:
                piece_length = file_length - (default_piece_length * piece_index)
            else:
                piece_length = default_piece_length
            number_of_blocks = math.ceil(piece_length / (16 * 1024))
        
            for block_index in range(number_of_blocks):
                begin = 2**14 * block_index
                print(f"begin: {begin}")
                block_length = min(piece_length - begin, 2**14)
                print(
                f"Requesting block {block_index + 1} of {number_of_blocks} with length {block_length}"
                )
                request_payload = struct.pack(
                    ">IBIII", 13, 6, piece_index, begin, block_length
                )
                print("Requesting block, with payload:")
                print(request_payload)
                print(struct.unpack(">IBIII", request_payload))
                print(int.from_bytes(request_payload[:4]))
                print(int.from_bytes(request_payload[4:5]))
                print(int.from_bytes(request_payload[5:9]))
                print(int.from_bytes(request_payload[17:21]))
                sock.sendall(request_payload)
                message = receive_message(sock)
                data.extend(message[13:])
        with open(output_file, "wb") as f:
            f.write(data)
    finally:
        sock.close()
    return True




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
        if len(sys.argv) != 6:
            raise ValueError("Usage: download_piece <torrent file> <piece index> <output file>")
        file_name = sys.argv[4]
        piece_index = int(sys.argv[5])
        output_file = sys.argv[3]
        with open(file_name, "rb") as file:
            bencoded_content = file.read()
        torrent, _ = decode_bencode(bencoded_content)
        check = download_piece(torrent, piece_index, output_file)
        if check:
            print("Downloaded piece successfully")
        else:
            print("Failed to download piece")
    elif command == "download":
        if len(sys.argv) != 6:
            raise ValueError("Usage: download_piece <torrent file> <piece index> <output file>")
        file_name = sys.argv[4]
        output_file = sys.argv[3]
        with open(file_name, "rb") as file:
            bencoded_content = file.read()
        torrent, _ = decode_bencode(bencoded_content)
        check = download(torrent, output_file)
        if check:
            print("Downloaded piece successfully")
        else:
            print("Failed to download piece")


    else:
        raise NotImplementedError(f"Unknown command {command}")

if __name__ == "__main__":
    main()



            # # Send requests to all peers
            
            # try:
            #     download_piece(ip, port, file_name, piece_index, output_file)
            #     break
            # except Exception as e:
            #     print(f"Failed to download from peer {ip}:{port}: {e}")