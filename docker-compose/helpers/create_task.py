import yaml
import base64
import os
import hashlib
from cryptography.hazmat.primitives.asymmetric import x25519

def generate_key_pair():
    private_key = x25519.X25519PrivateKey.generate()
    public_key = private_key.public_key()
    return private_key, public_key

def encode_key(key):
    if isinstance(key, str):
        key = key.encode('utf-8')
    return base64.urlsafe_b64encode(key).decode('utf-8').rstrip('=')

assert encode_key("aggregator-235242f99406c4fd28b820c32eab0f68") == "YWdncmVnYXRvci0yMzUyNDJmOTk0MDZjNGZkMjhiODIwYzMyZWFiMGY2OA"

def generate_hash(value):
    if isinstance(value, str):
        value = value.encode('utf-8')
    return base64.urlsafe_b64encode(hashlib.sha256(value).digest()).decode('utf-8').rstrip('=')

task_id = encode_key(os.urandom(32))
assert len(task_id) == len("G9YKXjoEjfoU7M_fi_o2H0wmzavRb2sBFHeykeRhDMk")
print(task_id)

def create_task(role, peer_aggregator_endpoint, query_type, vdaf, vdaf_bits, vdaf_verify_key, task_id, auth_token, collector_token_hash, public_key, private_key):
    task = {
        'task_id': task_id,
        'peer_aggregator_endpoint': peer_aggregator_endpoint,
        'query_type': query_type,
        'vdaf': {vdaf: {'bits': vdaf_bits}} if role == 'Leader' else vdaf,
        'role': role,
        'vdaf_verify_key': vdaf_verify_key,
        'max_batch_query_count': 1,
        'task_expiration': 1704088800,
        'report_expiry_age': 7776000 if role == 'Leader' else None,
        'min_batch_size': 100,
        'time_precision': 1800 if role == 'Leader' else 300,
        'tolerable_clock_skew': 60,
        'collector_hpke_config': {
            'id': 183,
            'kem_id': 'X25519HkdfSha256',
            'kdf_id': 'HkdfSha256',
            'aead_id': 'Aes128Gcm',
            'public_key': public_key
        },
        'aggregator_auth_token': {
            'type': 'DapAuth',
            'token': auth_token
        } if role == 'Leader' else None,
        'collector_auth_token_hash': {
            'type': 'Bearer',
            'hash': collector_token_hash
        } if role == 'Leader' else None,
        'hpke_keys': [{
            'config': {
                'id': 164 if role == 'Leader' else 37,
                'kem_id': 'X25519HkdfSha256',
                'kdf_id': 'HkdfSha256',
                'aead_id': 'Aes128Gcm',
                'public_key': public_key
            },
            'private_key': private_key
        }],
        'aggregator_auth_token_hash': {
            'type': 'Bearer',
            'hash': generate_hash('aggregator-token')
        } if role == 'Helper' else None
    }
    
    # Remove None values for Helper role
    task = {k: v for k, v in task.items() if v is not None}
    
    return task

# Gather information from user
print("Let's create a task configuration for both Leader and Helper roles.")

# peer_aggregator_endpoint_leader = input("Enter peer aggregator endpoint for Leader (e.g., https://example.com/): ")
# peer_aggregator_endpoint_helper = input("Enter peer aggregator endpoint for Helper (e.g., https://example.org/): ")
# vdaf_leader = input("Enter VDAF for Leader (e.g., !Prio3Sum): ")
# vdaf_bits_leader = int(input("Enter VDAF bits for Leader (e.g., 16): "))
# vdaf_helper = input("Enter VDAF for Helper (e.g., Prio3Count): ")
# task_id = base64.urlsafe_b64encode(os.urandom(32)).decode('utf-8').rstrip('=')
# auth_token = input("Enter auth token for Leader: ")
# collector_token_hash = generate_hash(input("Enter collector token for Leader: "))

# # Generate keys
# private_key_leader, public_key_leader = generate_key_pair()
# private_key_helper, public_key_helper = generate_key_pair()

# encoded_public_key_leader = encode_key(public_key_leader.public_bytes())
# encoded_private_key_leader = encode_key(private_key_leader.private_bytes())
# encoded_public_key_helper = encode_key(public_key_helper.public_bytes())
# encoded_private_key_helper = encode_key(private_key_helper.private_bytes())

# vdaf_verify_key_leader = encode_key(os.urandom(32))
# vdaf_verify_key_helper = encode_key(os.urandom(32))

# Create tasks
# leader_task = create_task(
#     role='Leader',
#     peer_aggregator_endpoint=peer_aggregator_endpoint_leader,
#     vdaf=vdaf_leader,
#     vdaf_bits=vdaf_bits_leader,
#     vdaf_verify_key=vdaf_verify_key_leader,
#     task_id=task_id,
#     auth_token=auth_token,
#     collector_token_hash=collector_token_hash,
#     public_key=encoded_public_key_leader,
#     private_key=encoded_private_key_leader
# )

# helper_task = create_task(
#     role='Helper',
#     peer_aggregator_endpoint=peer_aggregator_endpoint_helper,
#     vdaf=vdaf_helper,
#     vdaf_bits=None,
#     vdaf_verify_key=vdaf_verify_key_helper,
#     task_id=task_id,
#     auth_token=None,
#     collector_token_hash=None,
#     public_key=encoded_public_key_helper,
#     private_key=encoded_private_key_helper
# )

# # Save tasks to YAML files
# with open('task_leader.yml', 'w') as leader_file:
#     yaml.dump([leader_task], leader_file, default_flow_style=False)

# with open('task_helper.yml', 'w') as helper_file:
#     yaml.dump([helper_task], helper_file, default_flow_style=False)

# print("Leader and Helper task files generated successfully.")
